from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from xac.api import ExplanationCategory as ExplanationCategory_
from xac.api import ExplanationType as ExplanationType_
from xac.api import ModelType as ModelType_
from xac.api.auth import auth as _auth
from xac.api.config_file import generate as _generate
from xac.api.resources.job import output as _job_output
from xac.api.resources.job import remove as job_remove
from xac.api.resources.job import submit as _job_submit
from xac.api.resources.session import init as _sess_init
from xac.api.resources.session import remove as sess_remove
from xac.qexplain import transformers as _transformers
from xac.utils.helpers import secho


class Transforms:
    GlobalImportances = _transformers.GlobalImportances
    GlobalAlignments = _transformers.GlobalAlignments
    GlobalRules = _transformers.GlobalRules
    LocalAttributions = _transformers.LocalAttributions
    LocalRules = _transformers.LocalRules
    CounterFactuals = _transformers.Counterfactuals
    Predictions = _transformers.Predictions
    ModelMetrics = _transformers.ModelMetrics


class ExplainPromise:
    __slots__ = (
        "job_id",
        "name",
        "explanation_types",
        "output_file",
        "raw",
        "quiet",
    )

    def __init__(
        self,
        job_id,
        name,
        explanation_types,
        output_file,
        raw=True,
        quiet=True,
    ):
        self.job_id = job_id
        self.name = name
        self.explanation_types = explanation_types
        self.output_file = output_file
        self.raw = raw
        self.quiet = quiet

    def __repr__(self):
        return (
            f"ExplainPromise[job_id={self.job_id}, name={self.name}, "
            f"output_file={self.output_file},"
            f"raw={self.raw}, quiet={self.quiet}]"
        )

    def _transform(self, json_out):
        if isinstance(self.explanation_types, ExplanationType_):
            exp_type = self.explanation_types
        elif len(self.explanation_types) == 1:
            exp_type = self.explanation_types[0]
        else:  # Multiple explanation types in one shot
            return json_out
        if exp_type == ExplanationType_.global_importances:
            return Transforms.GlobalImportances(json_out).to_df()
        if exp_type == ExplanationType_.global_alignments:
            return Transforms.GlobalAlignments(json_out).to_df()
        if exp_type == ExplanationType_.model_metrics:
            return Transforms.ModelMetrics(json_out).to_df()
        if exp_type == ExplanationType_.global_rules:
            return Transforms.GlobalRules(json_out).to_dict()
        if exp_type == ExplanationType_.local_attributions:
            if isinstance(json_out, list):
                return [Transforms.LocalAttributions(o).to_df() for o in json_out]
            else:
                return Transforms.LocalAttributions(json_out).to_df()
        if exp_type == ExplanationType_.local_rules:
            return Transforms.LocalRules(json_out).to_dict()
        if exp_type == ExplanationType_.counterfactuals:
            if isinstance(json_out, list):
                return [
                    Transforms.CounterFactuals(o).to_structured_dict() for o in json_out
                ]
            else:
                return Transforms.CounterFactuals(json_out).to_structured_dict()
        if exp_type == ExplanationType_.predictions:
            return Transforms.Predictions(json_out).predictions

    def get(self, raw: bool = True, quiet=False):
        """Generate explanations from promise as json/output_file

        Args:
            raw: if False, return appropriate transformed data structure
             (overridden if calling instance `explainer.raw` is False)
            quiet: no messages to stdout

        """
        raw = raw if self.raw else self.raw
        quiet = self.quiet or quiet
        json_out = _job_output(
            self.job_id,
            output_file=self.output_file,
            poll_till_complete=True,
            poll_every=10,
            quiet=quiet,
        )
        if isinstance(self.explanation_types, ExplanationType_):
            json_out = json_out[self.explanation_types.value]
        elif len(self.explanation_types) == 1:
            json_out = json_out[self.explanation_types[0].value]
        else:
            json_out = json_out
        if isinstance(json_out, list) and len(json_out) == 1:
            json_out = json_out[0]

        if raw:
            return json_out
        else:
            return self._transform(json_out)


class Explainer:
    ModelType = ModelType_
    ExplanationCategory = ExplanationCategory_
    ExplanationType = ExplanationType_

    @staticmethod
    def login(email):
        return _auth.login_with_email(email=email)

    def __init__(self, raw=True, quiet=False):
        """Create a new Explainer class

        Args:
            raw: if False, transform explanations to appropriate data structures
              other than default JSON deserialized server output (across all methods)
            quiet: suppress messages to stdout across all methods
        """
        self._session_id = None
        self.jobs = []
        self.promises = []
        self.quiet = quiet
        self.raw = raw

    def from_config(
        self,
        config_yaml: str,
        explanation_category: ExplanationCategory_ = ExplanationCategory.TABULAR,
        friendly_name: str = None,
        paths_relative_to_config=True,
        quiet=False,
    ):
        """Create a new explanation session from config

        Args:
            config_yaml: path to Xaipient yaml config file
            explanation_category: category of explanation outlined in
              `ExplanationCategory` .(Currently only ExplanationCategory.TABULAR is
               supported)
            friendly_name: optional friendly name for session
            paths_relative_to_config: if True, any relative paths specified in the
                config file ['model', 'coltrans', 'data', 'feature_grammar'] will
                be relative to the yaml file location.
                If False, will default relative to current working path location.
                Does not matter for absolute paths
            quiet: if True, no output is printed
        """
        quiet = self.quiet or quiet
        self._session_id = _sess_init(
            config_yaml=config_yaml,
            explanation_category=explanation_category,
            friendly_name=friendly_name,
            paths_relative_to_config=paths_relative_to_config,
            quiet=quiet,
        )

    def new(
        self,
        title: str,
        model_type: ModelType_,
        model: str,
        data: str,
        coltrans: str,
        explanation_category: ExplanationCategory_ = ExplanationCategory.TABULAR,
        friendly_name: Optional[str] = None,
        quiet=False,
        feature_grammar: str = None,
        classification: bool = None,
        scale_std: bool = False,
        scale_minmax: bool = False,
        threshold: float = 0.5,
        rule_space_max: int = 10000,
        cf_zoo: bool = True,
        cf_quantile: float = 0.5,
        cf_fixed_features: list = None,
        target_labels: dict = None,
        use_preprocessor_ordering: bool = None,
        is_rnn: bool = False,
        time_steps: int = None,
        vstacked: bool = None,
        groupby_columns: list = None,
        slice: str = None,
        n_inputs_torch_model: int = None,
        fairness_dropped_coltrans: list = None,
        fairness_gan_cfg_model_type: str = None,
        fairness_gan_cfg_model: str = None,
        fairness_protected_attr: str = None,
        fairness_in_set: Union[int, bool, str] = None,
        fairness_out_set: Union[int, bool, str] = None,
        fairness_in_label: str = None,
        fairness_out_label: str = None,
    ):
        """Create a new explanation session

        Args:
            title: A concise description of the task (e.g German Credit Data)
            model_type: Type of model to be explained (Explainer.ModelType)
            model: Path to a valid model file
            data: Path to a valid CSV file for computing features and global explns
            coltrans: Path to a scikit-learn column transformer pickle file
            explanation_category: Category of explanation
                [only Explainer.ExplanationCategory.TABULAR supported currently],
            friendly_name: Friendly name for explanation session,
            quiet: if True, no output is printed
            feature_grammar: Path to a .lark file for advanced parsing (WIP)
            classification: if true, whether this is a classification task
            scale_std: if true, apply standard scaling to numeric columns
            scale_minmax: if true, apply minmax scaling to numeric columns
            threshold: Threshold for binary classification (0.0 to 1.0)
            rule_space_max: Max set of examples to use for rules
            cf_zoo: If true, use zoo for counterfactuals
            cf_quantile: max quantile-change for counterfactual (0.0 to 1.0)
            cf_fixed_features: List of features to hold fixed for counterfactual
            target_labels: Map of target (int) ->labels (str), {0: 'Good', 1: 'Bad'}
            use_preprocessor_ordering:
                if true, respect preprocessor ordering in column transformer
            is_rnn: If true, model is a time-series (rnn) model
            time_steps: number of timesteps in an input seq for a rnn model
            vstacked: If true, rnn model the given dataframe has stacked sequences
            groupby_columns:
                for an rnn model, list of grouping columns for extracting sequences
            slice: dataframe query string to pre-slice the data
            n_inputs_torch_model:
                Number of inputs to model (only for pytorch models)
            fairness_dropped_coltrans:
                for fairness, columns to be dropped [optional, list of string]
            fairness_gan_cfg_model_type:
                for fairness, GAN model type
            fairness_gan_cfg_model:
                for fairness, GAN model path
            fairness_protected_attr: for fairness, protected attribute
            fairness_in_set: for fairness, protected group value input (class) to GAN
            fairness_out_set: for fairness, protected group value output (class) of GAN
            fairness_in_label: for fairness, label of in-set
            fairness_out_label: for fairness, label of out-set
        """
        quiet = self.quiet or quiet
        config_yaml_str = _generate(
            title=title,
            model_type=model_type.value,
            model=model,
            data=data,
            coltrans=coltrans,
            feature_grammar=feature_grammar,
            classification=classification,
            scale_std=scale_std,
            scale_minmax=scale_minmax,
            threshold=threshold,
            rule_space_max=rule_space_max,
            cf_zoo=cf_zoo,
            cf_quantile=cf_quantile,
            cf_fixed_features=cf_fixed_features,
            target_labels=target_labels,
            use_preprocessor_ordering=use_preprocessor_ordering,
            is_rnn=is_rnn,
            time_steps=time_steps,
            vstacked=vstacked,
            groupby_columns=groupby_columns,
            slice=slice,
            n_inputs_torch_model=n_inputs_torch_model,
            fairness_dropped_coltrans=fairness_dropped_coltrans,
            fairness_gan_cfg_model_type=fairness_gan_cfg_model_type,
            fairness_gan_cfg_model=fairness_gan_cfg_model,
            fairness_protected_attr=fairness_protected_attr,
            fairness_in_set=fairness_in_set,
            fairness_out_set=fairness_out_set,
            fairness_in_label=fairness_in_label,
            fairness_out_label=fairness_out_label,
        )
        self._session_id = _sess_init(
            config_yaml_str=config_yaml_str,
            explanation_category=explanation_category,
            friendly_name=friendly_name,
            quiet=quiet,
        )

    def _local_kwargs_mod(self, kwargs):
        kwargs.pop("self")
        kwargs.pop("config_options")
        raw = kwargs.pop("raw")
        raw = raw if self.raw else self.raw
        quiet = kwargs.get("quiet", False)
        quiet = self.quiet or quiet
        return kwargs, quiet, raw

    def ask_global_importances(self, **config_options):
        """Returns an explanation promise to generate global importances later
           using .get()

        Args:
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.global_importances
        return self.ask(**kwargs)

    def get_global_importances(self, raw=True, **config_options):
        """Returns global importances immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.transform_output` is True)
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed global importances

        """
        kwargs = dict(locals())
        kwargs, quiet, raw = self._local_kwargs_mod(kwargs)
        gi_promise = self.ask_global_importances(**kwargs)
        return gi_promise.get(raw=raw, quiet=quiet)

    def ask_global_alignments(self, **config_options):
        """Returns an explanation promise to generate global alignments later
           using .get()

        Args:
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.global_alignments
        return self.ask(**kwargs)

    def get_global_alignments(self, raw=True, **config_options):
        """Returns global alignments immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.transform_output` is True)
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed global importances

        """
        kwargs = dict(locals())
        kwargs, quiet, raw = self._local_kwargs_mod(kwargs)
        ga_promise = self.ask_global_alignments(**kwargs)
        return ga_promise.get(raw=raw, quiet=quiet)

    def ask_model_metrics(self, **config_options):
        """Returns an explanation promise to generate model metrics later
           using .get()

        Args:
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.model_metrics
        return self.ask(**kwargs)

    def get_model_metrics(self, raw=True, **config_options):
        """Returns model metrics immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.transform_output` is True)
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed model metrics

        """
        kwargs = dict(locals())
        kwargs, quiet, raw = self._local_kwargs_mod(kwargs)
        mm_promise = self.ask_model_metrics(**kwargs)
        return mm_promise.get(raw=raw, quiet=quiet)

    def ask_local_attributions(
        self,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns an explanation promise to generate local attributions later
           using .get()

        Args:
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.local_attributions
        return self.ask(**kwargs)

    def get_local_attributions(
        self,
        raw=True,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns local attributions immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.transform_output` is True)
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed local attributions

        """
        kwargs = dict(locals())
        kwargs, quiet, raw = self._local_kwargs_mod(kwargs)
        la_promise = self.ask_local_attributions(**kwargs)
        return la_promise.get(raw=raw, quiet=quiet)

    def ask_local_rules(
        self,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns an explanation promise to generate local rules later
           using .get()

        Args:
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.local_rules
        return self.ask(**kwargs)

    def get_local_rules(
        self,
        raw=True,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns local rules immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.transform_output` is True)
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed local rules

        """
        kwargs = dict(locals())
        kwargs, quiet, transform = self._local_kwargs_mod(kwargs)
        lr_promise = self.ask_local_rules(**kwargs)
        return lr_promise.get(raw=raw, quiet=quiet)

    def ask_counterfactuals(
        self,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns an explanation promise to generate counterfactuals later
           using .get()

        Args:
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object
        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.counterfactuals
        return self.ask(**kwargs)

    def get_counterfactuals(
        self,
        raw=True,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns counterfactuals immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.transform_output` is True)
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed counterfactuals

        """
        kwargs = dict(locals())
        kwargs, quiet, raw = self._local_kwargs_mod(kwargs)
        cf_promise = self.ask_counterfactuals(**kwargs)
        return cf_promise.get(raw=raw, quiet=quiet)

    def ask_predictions(
        self,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns an explanation promise to generate model predictions later
           using .get()

        Args:
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.predictions
        return self.ask(**kwargs)

    def get_predictions(
        self,
        raw=True,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        **config_options,
    ):
        """Returns model predictions immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.transform_output` is True)
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed model predictions

        """
        kwargs = dict(locals())
        kwargs, quiet, raw = self._local_kwargs_mod(kwargs)
        pred_promise = self.ask_predictions(**kwargs)
        return pred_promise.get(raw=raw, quiet=quiet)

    def ask_global_rules(self, **config_options):
        """Returns an explanation promise to generate global rules later
           using .get()

        Args:
            **config_options: Optional config_options. See `ask` for list of supported
                options

        Returns:
            `ExplainPromise` object

        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("config_options")
        kwargs["explanation_type"] = ExplanationType_.global_rules
        return self.ask(**kwargs)

    def get_global_rules(self, raw=True, **config_options):
        """Returns global rules immediately

        Args:
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.raw` is True)
            **config_options: Optional config_options. See `get` for list of supported
                options

        Returns:
            Raw or transformed global rules

        """
        kwargs = dict(locals())
        kwargs, quiet, raw = self._local_kwargs_mod(kwargs)
        gr_promise = self.ask_global_rules(**kwargs)
        return gr_promise.get(raw=raw, quiet=quiet)

    def ask(
        self,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        explanation_type: ExplanationType_ = ExplanationType.global_importances,
        friendly_name=None,
        output_file=None,
        quiet=False,
        classification: bool = None,
        scale_std: bool = None,
        scale_minmax: bool = None,
        threshold: float = None,
        rule_space_max: int = None,
        cf_zoo: bool = None,
        cf_quantile: float = None,
        cf_fixed_features: list = None,
        target_labels: dict = None,
        use_preprocessor_ordering: bool = None,
        is_rnn: bool = None,
        time_steps: int = None,
        vstacked: bool = None,
        groupby_columns: list = None,
        slice: str = None,
        n_inputs_torch_model: int = None,
    ):
        """Returns an explanation promise to generate explanations later for
        a given explanation type

        Args:
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            explanation_type: One of supported explanation type outlined in
              `Explainer.ExplanationType`. One of following
               ExplanationType.
                    counterfactuals
                    local_rules
                    local_attributions
                    predictions
                    global_rules
                    global_importances
                    global_alignments
                    model_metrics
            friendly_name: Friendly name for explanation job
            output_file: Path to a output file to save json
            quiet: if True, no output is printed
            classification: if true, whether this is a classification task
            scale_std: if true, apply standard scaling to numeric columns
            scale_minmax: if true, apply minmax scaling to numeric columns
            threshold: Threshold for binary classification (0.0 to 1.0)
            rule_space_max: Max set of examples to use for rules
            cf_zoo: If true, use zoo for counterfactuals
            cf_quantile: max quantile-change for counterfactual (0.0 to 1.0)
            cf_fixed_features: List of features to hold fixed for counterfactual
            target_labels: Map of target (int) ->labels (str), {0: 'Good', 1: 'Bad'}
            use_preprocessor_ordering:
                if true, respect preprocessor ordering in column transformer
            is_rnn: If true, model is a time-series (rnn) model
            time_steps: number of timesteps in an input seq for a rnn model
            vstacked: If true, rnn model the given dataframe has stacked sequences
            groupby_columns:
                for an rnn model, list of grouping columns for extracting sequences
            slice: dataframe query string to pre-slice the data
            n_inputs_torch_model: Number of inputs to model (only for pytorch models)

        Returns:
            A `Explainer.ExplainPromise` object used to generate explanations using
            `.get()`
        """
        kwargs = dict(locals())
        kwargs.pop("self")
        kwargs.pop("explanation_type")
        kwargs["wait_till_complete"] = False
        kwargs["quiet"] = self.quiet or quiet
        if not isinstance(explanation_type, ExplanationType_):
            raise ValueError(
                f"{explanation_type} must be on " f"instance Explainer.ExplanationType"
            )
        if explanation_type == ExplanationType_.all:
            raise ValueError(f"{explanation_type} not supported for this method.")
        kwargs["explanation_types"] = [explanation_type]
        return self._explain(**kwargs)

    def get(
        self,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        explanation_type: ExplanationType_ = ExplanationType.global_importances,
        friendly_name=None,
        output_file=None,
        raw=True,
        quiet=False,
        classification: bool = None,
        scale_std: bool = None,
        scale_minmax: bool = None,
        threshold: float = None,
        rule_space_max: int = None,
        cf_zoo: bool = None,
        cf_quantile: float = None,
        cf_fixed_features: list = None,
        target_labels: dict = None,
        use_preprocessor_ordering: bool = None,
        is_rnn: bool = None,
        time_steps: int = None,
        vstacked: bool = None,
        groupby_columns: list = None,
        slice: str = None,
        n_inputs_torch_model: int = None,
    ):
        """Generates an explanation immediately for given explanation type

        Args:
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            explanation_type: One of supported explanation type outlined in
              `Explainer.ExplanationType`. One of following
               ExplanationType.
                    counterfactuals
                    local_rules
                    local_attributions
                    predictions
                    global_rules
                    global_importances
                    global_alignments
                    model_metrics
            friendly_name: Friendly name for explanation job
            output_file: Path to a output file to save json
            raw: if False, return appropriate transformed data structure
                (overridden if instance `explainer.raw` is True)
            quiet: if True, no output is printed
            classification: if true, whether this is a classification task
            scale_std: if true, apply standard scaling to numeric columns
            scale_minmax: if true, apply minmax scaling to numeric columns
            threshold: Threshold for binary classification (0.0 to 1.0)
            rule_space_max: Max set of examples to use for rules
            cf_zoo: If true, use zoo for counterfactuals
            cf_quantile: max quantile-change for counterfactual (0.0 to 1.0)
            cf_fixed_features: List of features to hold fixed for counterfactual
            target_labels: Map of target (int) ->labels (str), {0: 'Good', 1: 'Bad'}
            use_preprocessor_ordering:
                if true, respect preprocessor ordering in column transformer
            is_rnn: If true, model is a time-series (rnn) model
            time_steps: number of timesteps in an input seq for a rnn model
            vstacked: If true, rnn model the given dataframe has stacked sequences
            groupby_columns:
                for an rnn model, list of grouping columns for extracting sequences
            slice: dataframe query string to pre-slice the data
            n_inputs_torch_model: Number of inputs to model (only for pytorch models)

        Returns:
            Dictionary of explanations for the requested explanation type
        """
        kwargs = dict(locals())
        kwargs.pop("self")
        raw = kwargs.pop("raw")
        raw = raw if self.raw else self.raw
        promise = self.ask(**kwargs)
        return promise.get(raw=raw)

    def _explain(
        self,
        feature_dict: Dict = None,
        input_file: str = None,
        feature_row: int = None,
        explanation_types: Union[
            ExplanationType_, List[ExplanationType_], Tuple[ExplanationType_]
        ] = (ExplanationType.global_importances,),
        friendly_name=None,
        wait_till_complete=True,
        output_file=None,
        quiet=False,
        classification: bool = None,
        scale_std: bool = None,
        scale_minmax: bool = None,
        threshold: float = None,
        rule_space_max: int = None,
        cf_zoo: bool = None,
        cf_quantile: float = None,
        cf_fixed_features: list = None,
        target_labels: dict = None,
        use_preprocessor_ordering: bool = None,
        is_rnn: bool = None,
        time_steps: int = None,
        vstacked: bool = None,
        groupby_columns: list = None,
        slice: str = None,
        n_inputs_torch_model: int = None,
    ):
        """Generate explanations with possible option overrides. Optionally
        if `wait_till_complete` is False, returns a promise to generate output

        Args:
            feature_dict: A dictionary of features to explain
            input_file: Optional, CSV file to explain
            feature_row: Row in the `input_file` to explain
            explanation_types: list of supported explanation types outlined in
              `xac.ExplanationType`. One or all of following
               ExplanationType.
                    counterfactuals
                    local_rules
                    local_attributions
                    global_rules
                    global_importances
                    global_alignments
                    model_metrics
                    all (a shortcut for all of the above)
            friendly_name: Friendly name for explanation job
            wait_till_complete: wait till this job completes, else returns a promise
                object `ExplainPromise` with a get method
            output_file: Path to a output file to save json
            quiet: if True, no output is printed
            classification: if true, whether this is a classification task
            scale_std: if true, apply standard scaling to numeric columns
            scale_minmax: if true, apply minmax scaling to numeric columns
            threshold: Threshold for binary classification (0.0 to 1.0)
            rule_space_max: Max set of examples to use for rules
            cf_zoo: If true, use zoo for counterfactuals
            cf_quantile: max quantile-change for counterfactual (0.0 to 1.0)
            cf_fixed_features: List of features to hold fixed for counterfactual
            target_labels: Map of target (int) ->labels (str), {0: 'Good', 1: 'Bad'}
            use_preprocessor_ordering:
                if true, respect preprocessor ordering in column transformer
            is_rnn: If true, model is a time-series (rnn) model
            time_steps: number of timesteps in an input seq for a rnn model
            vstacked: If true, rnn model the given dataframe has stacked sequences
            groupby_columns:
                for an rnn model, list of grouping columns for extracting sequences
            slice: dataframe query string to pre-slice the data
            n_inputs_torch_model: Number of inputs to model (only for pytorch models)

        Returns:
            Dictionary of possible explanations
        """
        quiet = self.quiet or quiet
        if feature_dict:
            if not isinstance(feature_dict, dict):
                secho(
                    "❌ `feature_dict` must be a dictionary of features",
                    err=True,
                )
                return None
        if feature_row:
            if not isinstance(feature_row, int):
                secho(
                    "❌ `feature_row` must be a integer",
                    err=True,
                )
                return None

        if self._session_id is None:
            secho(
                "❌ Explaining a non-existent session. "
                "Create a valid session with Explainer.new",
                err=True,
            )
            return None
        job_id = _job_submit(
            session_id=self._session_id,
            features_list=[feature_dict] if feature_dict else None,
            input_file=input_file,
            start=feature_row,
            end=feature_row + 1 if feature_row is not None else None,
            explanation_types=explanation_types,
            friendly_name=friendly_name,
            quiet=quiet,
            classification=classification,
            scale_std=scale_std,
            scale_minmax=scale_minmax,
            threshold=threshold,
            rule_space_max=rule_space_max,
            cf_zoo=cf_zoo,
            cf_quantile=cf_quantile,
            cf_fixed_features=cf_fixed_features,
            target_labels=target_labels,
            use_preprocessor_ordering=use_preprocessor_ordering,
            is_rnn=is_rnn,
            time_steps=time_steps,
            vstacked=vstacked,
            groupby_columns=groupby_columns,
            slice=slice,
            n_inputs_torch_model=n_inputs_torch_model,
        )
        self.jobs.append(job_id)
        if wait_till_complete:
            return _job_output(
                job_id,
                output_file=output_file,
                poll_till_complete=True,
                poll_every=10,
                quiet=quiet,
            )
        else:
            promise = ExplainPromise(
                job_id=job_id,
                name=friendly_name,
                explanation_types=explanation_types,
                output_file=output_file,
                raw=self.raw,
                quiet=self.quiet,
            )
            if not quiet:
                secho(
                    f" 🆀 Added {job_id} to pending promise queue. Use `get` "
                    f"with returned `ExplainPromise` object to get explanations"
                )
            self.promises.append(promise)
            return promise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def cleanup(self):
        """Force Cleanup resources on server"""
        for job in self.jobs:
            job_remove(job, quiet=self.quiet)
        if self._session_id:
            sess_remove(self._session_id, quiet=self.quiet)
