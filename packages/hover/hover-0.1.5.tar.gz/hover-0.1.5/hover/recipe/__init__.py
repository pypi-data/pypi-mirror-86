"""
High-level workflows.
"""
import pandas as pd
from tqdm import tqdm
from hover import module_config
from hover.core.dataset import SupervisableTextDataset
from hover.core.neural import create_text_vector_net_from_module, TextVectorNet
from hover.utils.torch_helper import vector_dataloader, one_hot, label_smoothing
from .subroutine import link_plots
from wasabi import msg as logger
from wrappy import todo


class VisualAnnotation:
    """
    Using a vectorizer followed by dimensionality reduction,
    produce a 2-D visualization of the dataset, then annotate it.
    """

    def __init__(self, dataset, vectorizer):
        """
        """
        assert isinstance(dataset, SupervisableDataset)
        assert callable(vectorizer)
        self.dataset = dataset
        self.vectorizer = vectorizer
        self.flush()
        self.dataset.compute_2d_embedding(self.vectorizer, **kwargs)
        self.setup_explorers()

    def setup_explorers(self):
        """
        Determines which explorers are involved.
        """
        self.corpus_explorer = BokehCorpusExplorer(
            self.dataset.dfs["raw"], title="Corpus Explorer"
        )
        self.corpus_annotator = BokehCorpusAnnotator(
            self.dataset.dfs["raw"], title="Corpus Annotator"
        )

    @todo("Review this function")
    def flush(self, subset="train"):
        """
        Flush annotated pieces into train/dev/test, then re-create explorers.
        """
        # pick out the annotated slice
        annotated_df = self.corpus_annotator.df_raw
        annotated_slice = annotated_df[
            annotated_df["label"] != module_config.ABSTAIN_DECODED
        ]

        # append annotated slice to the designated subset, then deduplicate and find classes
        self.dataset.dfs[subset] = pd.concat(
            [self.dataset.dfs[subset], annotated_slice], axis=0
        )
        self.dataset.df_deduplicate()
        self.dataset.setup_label_coding()
        self.dataset.synchronize_df_to_dictl()

        # DF entries have now changed; reset the plots
        self.setup_explorers()

    def plots(self, **kwargs):
        """
        A list of plots to be shown.
        """
        return link_plots(self.corpus_explorer, self.corpus_annotator, **kwargs)


class TBD:
    """
    """

    @todo(
        "Think about what belongs in this class and what belongs in the core modules."
    )
    def __init__(self, dataset, vectorizer=None, model_module_name=None):
        """
        """
        assert isinstance(dataset, SupervisableDataset)
        self.dataset = dataset
        self.model_module_name = model_module_name

    def model_from_dev(self, **kwargs):
        """
        Train a Prodigy-compatible model from the dev set.
        """
        model = create_text_vector_net_from_module(
            TextVectorNet, self.model_module_name, self.dataset.classes
        )
        dev_loader = self.get_loader("dev", model.vectorizer, smoothing_coeff=0.1)
        train_info = model.train(dev_loader, dev_loader, **kwargs)
        return model, train_info
