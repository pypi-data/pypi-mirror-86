"""Transform raw explanations to structured objects"""
import pandas as pd
from munch import Munch


class GlobalImportances:
    def __init__(self, global_importances):
        self.global_importances = Munch(global_importances)

    def to_df(self):
        return pd.DataFrame.from_dict(self.global_importances).T


class GlobalAlignments:
    def __init__(self, global_alignments):
        self.global_alignments = Munch(global_alignments)

    def to_df(self):
        return pd.DataFrame.from_dict(self.global_alignments).T


class ModelMetrics:
    def __init__(self, model_metrics):
        self.model_metrics = Munch({"Metrics": model_metrics})

    def to_df(self):
        return pd.DataFrame.from_dict(self.model_metrics, orient="columns").T


class GlobalRules:
    def __init__(self, global_rules):
        self.global_rules = global_rules

    def to_dict(self):
        return self.global_rules


class LocalAttributions:
    def __init__(self, local_attributions):
        self.local_attributions = Munch(local_attributions)

    def to_df(self):
        indices = list(self.local_attributions.keys())
        la_df = pd.DataFrame.from_dict(list(self.local_attributions.values()))
        la_df.index = indices
        return la_df


class Counterfactuals:
    def __init__(self, counter_factuals):
        self.counter_factuals = Munch(counter_factuals)

    def to_structured_dict(self):
        self.counter_factuals["table"] = pd.DataFrame(self.counter_factuals["table"]).T
        return self.counter_factuals


class LocalRules:
    def __init__(self, local_rules):
        self.local_rules = local_rules

    def to_dict(self):
        return self.local_rules


class Predictions:
    def __init__(self, predictions):
        self.predictions = Munch(predictions)
