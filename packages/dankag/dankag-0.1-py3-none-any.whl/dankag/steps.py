"""
Step definitions for dankag kaggle script runner.
"""
from dataclasses import dataclass


@dataclass
class StateVal:
    """
    Indicates a value represented by 'state_key'.
    Used as a reference to the value stored in the state.
    """
    state_key: str  # key stored in the key


def sv(state_key: str) -> StateVal:
    """
    Create StateVal instance from string.
    """
    return StateVal(state_key)


class Step:
    """
    Single step within the kaggle script for running.
    """
    def __init__(self, name: str):
        self.name = name

    def run(self, state: dict):
        raise NotImplementedError

    @staticmethod
    def stateval_or(val, state: dict):
        if isinstance(val, StateVal):
            return state[val.state_key]

        return val

    @staticmethod
    def sv_or(val, state: dict):
        """
        Alias method for stateval_or
        """
        return Step.stateval_or(val, state)


class SequentialStep(Step):
    def __init__(self, steps, **kwargs):
        super().__init__(**kwargs)
        self.steps = steps

    def run(self, state):
        for s in self.steps:
            state = s.run(state)

        return state


class CSVDataReadStep(Step):
    """
    Step for reading CSV data.
    """
    def __init__(self, data_file: str, data_key: str, target_key: str = None,
                 target_col=None, name='data_read_step'):
        super().__init__(name=name)
        self.data_file = data_file
        self.data_key = data_key
        self.target_col = target_col
        self.target_key = target_key

    def run(self, state):
        data = pd.read_csv(self.stateval_or(self.data_file, state))

        if self.target_col is not None:
            if self.target_key is None:
                raise ValueError('target_key should not be None'
                        'when target_col is not None')

            data, target = detach_target(
                data, column_name=self.stateval_or(self.target_col, state))

            state[self.target_key] = target

        state[self.data_key] = data
        return state


class SklearnPreprocessorStep(Step):
    def __init__(self, data: str, preprocessor, data_out_key: str,
                 preprocessor_key='preprocessor', fit=True):
        super().__init__(name='preprocess')
        self.data = data
        self.preprocessor = preprocessor
        self.fit = fit
        self.preprocessor_key = preprocessor_key
        self.data_out_key = data_out_key

    def run(self, state):
        data = self.stateval_or(self.data, state)

        if self.fit:
            self.preprocessor = self.preprocessor.fit(data)

        state[self.data_out_key] = self.preprocessor.transform(data)
        state[self.preprocessor_key] = self.preprocessor
        return state


class SklearnTrainTestPreprocessorStep(Step):
    def __init__(self, train_data, test_data, preprocessor,
                 train_data_out_key='train_data', test_data_out_key='test_data',
                 preprocessor_key='preprocessor', name='sklearn_train_test_preprocess',
                 **kwargs):
        super().__init__(name)
        self.train_data = train_data
        self.test_data = test_data

        self.train_data_out_key = train_data_out_key
        self.test_data_out_key = test_data_out_key
        self.preprocessor = preprocessor
        self.preprocessor_key = preprocessor_key

    def run(self, state) -> dict:
        state = SklearnPreprocessorStep(
                self.train_data, self.preprocessor,
                self.train_data_out_key, self.preprocessor_key, fit=True).run(state)
        return SklearnPreprocessorStep(self.test_data, self.preprocessor,
                self.test_data_out_key, self.preprocessor_key).run(state)  # no fit


class ModelTrainStep(Step):
    def __init__(self, model, train_dataset, val_datasets=None,
                 model_key='model', name='model_train_step'):
        super().__init__(name)
        self.model = model
        self.train_dataset = train_dataset
        self.val_datasets = val_datasets
        self.model_key = model_key

    def run(self, state) -> dict:
        model = self.stateval_or(self.model, state)
        train_dataset = self.stateval_or(self.train_dataset, state)
        val_datasets = self.stateval_or(self.val_datasets, state) if self.val_datasets is not None else None

        # store the model to the state
        model.fit(train_dataset=train_dataset, val_datasets=val_datasets)

        state[self.model_key] = model
        return state


class MultipleModelTrainStep(Step):
    def __init__(self, models: list,
                 name='multiple_model_train_step'):
        """
        Train multiple models.
        models: list of (model, model_key, train_dataset, val_dataset) pairs
        """
        super().__init__(name)
        self.models = models

    def run(self, state) -> dict:
        for model, model_key, train_dataset, val_dataset in self.models:
            state = ModelTrainStep(
                    model,
                    train_dataset,
                    val_dataset,
                    model_key).run(state)

        return state


class CreateModelStep(Step):
    def __init__(self, model_cls, model_key: str,
                 name='create_model', **kwargs):
        super().__init__(name)
        self.model_cls = model_cls
        self.model_key = model_key
        self.kwargs = kwargs

    def run(self, state) -> dict:
        kwargs = self.kwargs.copy()
        print(kwargs)

        for arg_key, arg_val in kwargs.items():
            kwargs[arg_key] = self.stateval_or(arg_val, state)

        state[self.model_key] = self.model_cls(**kwargs)
        return state


class PredictStep(Step):
    def __init__(self, model, data, prediction_key: str, name='predict_step'):
        super().__init__(name=name)
        self.model = model
        self.data = data
        self.prediction_key = prediction_key

    def run(self, state):
        model = self.stateval_or(self.model, state)
        data = self.stateval_or(self.data, state)

        state[self.prediction_key] = model.predict(data)
        return state


class CSVOutputStep(Step):
    def __init__(self, out_data, file_name, name='csv_output'):
        super().__init__(name=name)
        self.out_data = out_data
        self.file_name = file_name

    def run(self, state):
        file_name = self.stateval_or(self.file_name, state)

        self.stateval_or(self.out_data, state).to_csv(file_name, index=False)

        print(f'Written csv output: {self.file_name}')
        return state


class BatchedTFDatasetConversionStep(Step):
    def __init__(self, data, target, batch_size, dataset_key: str,
                 name='tf_dataset_conversion'):
        super().__init__(name)
        self.data = data
        self.target = target
        self.batch_size = batch_size
        self.dataset_key = dataset_key

    def run(self, state):
        data = self.stateval_or(self.data, state)
        target = self.stateval_or(self.target, state)
        batch_size = self.stateval_or(self.batch_size, state)

        dataset = tf.data.Dataset.from_tensor_slices((data, target)).batch(batch_size)
        state[self.dataset_key] = dataset

        return state
