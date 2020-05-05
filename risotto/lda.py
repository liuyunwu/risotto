# AUTOGENERATED! DO NOT EDIT! File to edit: 02_representations_and_lda.ipynb (unless otherwise specified).

__all__ = ['nlp', 'process_papers_file_contents', 'tokenizer']

# Cell
from .references import load_papers_from_metadata_file, build_papers_reference_graph, paper_as_markdown
from fastprogress.fastprogress import progress_bar

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from pathlib import Path

import scispacy
import en_core_sci_sm
import networkx as nx
from collections import defaultdict
import numpy as np

# Cell
nlp = en_core_sci_sm.load()

# Cell
def process_papers_file_contents(papers):
    texts = []
    nlp = en_core_sci_sm.load()
    for paper in progress_bar(papers):
        text = " \n ".join([ paragraph["text"] for paragraph in paper._file_contents["body_text"]])
        """
        NB.: for development speed purposes, the only document's attributes
        considered for the topic modelling were the title and the abstract.
        Should the text be included in other experiments, the following line
        should be modified to include `{paper.text}`.
        """
        texts.append(f"{paper.title} \n {paper.abstract}")
    return texts

# Cell
def tokenizer(sentence):
    tokens = []
    for token in nlp(sentence, disable=["tagger", "parser", "ner"]):
        # Se descartan números, stopwords, puntuación, espacio y tokens de largo 1
        if not (token.like_num or token.is_stop or token.is_punct
                or token.is_space or len(token) == 1):
            tokens.append(token.lemma_)
    return tokens