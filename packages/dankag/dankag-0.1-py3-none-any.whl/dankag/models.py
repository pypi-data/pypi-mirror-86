"""
Provides generalized definitions for multiple different packages,
used for kaggle competition scripts.
"""
from xgboost.sklearn import XGBClassifier


class Model:
    """
    Generalized model definition.
    """
    def predict(self, data, **kwargs):
        raise NotImplementedError

    def evaluate(self, dataset, **kwargs):
        raise NotImplementedError

    def fit(self, train_dataset, val_datasets: list = None, **kwargs):
        raise NotImplementedError


class XgbModel(Model):
    """
    Model definition for XGBoost model.
    """
    def __init__(self, n_estimators=520, learning_rate=0.05, gamma=0.03,
                 max_depth=8, min_child_weight=1.5, colsample_bytree=0.8,
                 subsample=0.8, nthread=4, verbosity=2,
                 objective='multi:softprob', early_stopping_rounds=10):
        super().__init__()
        self.model = XGBClassifier(
                learning_rate=learning_rate,
                gamma=gamma,
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_child_weight=min_child_weight,
                colsample_bytree=colsample_bytree,
                subsample=subsample,
                nthread=nthread,
                verbosity=verbosity,
                objective=objective)

        self.early_stopping_rounds = early_stopping_rounds

    def fit(self, train_dataset, val_datasets: list = None, **kwargs):
        train_data, train_targets = train_dataset

        eval_set = None
        if val_datasets is not None:
            eval_set = []
            for val_data, val_target in val_datasets:
                eval_set.append((val_data, val_target))

        return self.model.fit(train_data, train_targets,
                early_stopping_rounds=self.early_stopping_rounds,
                eval_set=eval_set)

    def evaluate(self, dataset):
        data, target = dataset
        return log_loss(target, self.model.predict_proba(data))

    def predict(self, data):
        return self.model.predict_proba(data)


class TensorflowModel(Model):
    """
    Model wrapper for tensorflow models.
    """
    def __init__(self, tf_model, optimizer, loss, metrics,
                 epochs: int, show_summary=True):
        super().__init__()
        self.model = tf_model
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        self.epochs = epochs

        if show_summary:
            self.model.summary()

    def fit(self, train_dataset, val_datasets: list = None):
        _ = self.model.fit(train_dataset, epochs=self.epochs)

    def evaluate(self, dataset, **kwargs):
        loss, acc = self.model.evaluate(dataset)
        print(f'loss: {loss}, acc: {acc}')
        return loss, acc

    def predict(self, data, **kwargs):
        return self.model.predict(data)


def from_tf_model(tf_model, *args, **kwargs):
    return TensorflowModel(tf_model, *args, **kwargs)
