import pandas as pd
import tensorflow as tf
from sklearn.metrics import log_loss


def detach_target(data, copy=False, column_name: str = None):
    # NOTE: currently supports pandas.DataFrame only

    if copy:
        data = data.copy()

    if column_name is None:
        # detach the last column by default
        return data.drop(len(data.columns) - 1, axis=1), data.iloc[:, -1:]
    return data.drop([column_name], axis=1), data[column_name]


class KaggleRunner:
    """
    Main kaggle script runner that consists of multiple steps.
    """
    def __init__(self, config, steps):
        self.config = config
        self.steps = steps

    def run(self):
        state = self.config

        for s in self.steps:
            print(f'Executing step: {s.name}')
            state = s.run(state)

        return state


def run(config, steps):
    return KaggleRunner(config, steps).run()
