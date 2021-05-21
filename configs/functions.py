#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 10:10:32 2021

@author: carlos.rodriguez1@bsc.es asier.gutierrez@bsc.es carme.armentano@bsc.es
"""

import spacy
import os
import json
from typing import List, Tuple, Optional
from thinc.api import Model
from spacy.pipeline import Lemmatizer
from spacy.tokens import Token
from spacy.language import Language
from spacy.lang.ca import Catalan


@spacy.registry.callbacks("before_callback")
def create_callback():
    from typing import Union, Iterator
    from spacy.symbols import NOUN, PROPN, PRON
    from spacy.errors import Errors
    from spacy.tokens import Doc, Span
    import re

    def before_callback(nlp):
        def _noun_chunks(doclike):
            """Detect base noun phrases from a dependency parse. Works on Doc and Span."""
            # fmt: off
            labels = ["nsubj", "nsubj:pass", "obj", "obl", "iobj", "ROOT", "appos", "nmod", "nmod:poss"]
            # fmt: on
            doc = doclike.doc  # Ensure works on both Doc and Span.
            if not doc.has_annotation("DEP"):
                raise ValueError(Errors.E029)
            np_deps = [doc.vocab.strings[label] for label in labels]
            conj = doc.vocab.strings.add("conj")
            np_label = doc.vocab.strings.add("NP")
            prev_end = -1
            for i, word in enumerate(doclike):
                if word.pos not in (NOUN, PROPN):
                    continue
                # Prevent nested chunks from being produced
                if word.left_edge.i <= prev_end:
                    continue
                if word.dep in np_deps:
                    left = word.left_edge.i
                    right = word.right_edge.i + 1
                # leave prepositions and punctuation out of the left side of the chunk
                    if word.left_edge.pos_ == "ADP" or word.left_edge.pos_ == "PUNCT":
                        left = word.left_edge.i + 1
                    prev_end = word.right_edge.i
                # leave subordinated clauses and appositions out of the chunk     
                    a = word.i + 1
                    while a < word.right_edge.i:
                        paraula = doc[a]
                        if paraula.pos_ == "VERB":
                            right = paraula.left_edge.i 
                            prev_end = paraula.left_edge.i -1
                        elif paraula.dep_ == "appos":
                            right = paraula.left_edge.i + 1
                            prev_end = paraula.left_edge.i -1
                        a += 1
              # leave punctuation out of the right side of the chunk                        
                    if word.right_edge.pos_ == "PUNCT":
                        right = right - 1
                    yield left, right, np_label
            
        nlp.Defaults.syntax_iterators = {"noun_chunks": _noun_chunks}
        nlp.Defaults.infixes.insert(3, "('ls|'ns|'t|'m|'n|-les|-la|-lo|-los|-me|-nos|-te|-vos|-se|-hi|-ne|-ho)(?![A-Za-z])|(-l'|-n')")
        nlp.Defaults.prefixes.insert(0, "-")
        nlp.Defaults.suffixes.insert(0, "-")
        return nlp
    return before_callback


@spacy.registry.misc("ca_lookups_loader")
def load_lookups(data_path):
    from spacy.lookups import Lookups
    lookups = Lookups()
    # "lemma_lookup", "lemma_rules", "lemma_exc", "lemma_index"
    with open(os.path.join(data_path, 'ca_lemma_lookup.json'), 'r') as lemma_lookup, \
         open(os.path.join(data_path, 'ca_lemma_rules.json'), 'r') as lemma_rules, \
         open(os.path.join(data_path, 'ca_lemma_exc.json'), 'r') as lemma_exc, \
         open(os.path.join(data_path, 'ca_lemma_index.json'), 'r') as lemma_index:
        lookups.add_table('lemma_lookup', json.load(lemma_lookup))
        lookups.add_table('lemma_rules', json.load(lemma_rules))
        lookups.add_table('lemma_exc', json.load(lemma_exc))
        lookups.add_table('lemma_index', json.load(lemma_index))
    return lookups


@Catalan.factory(
    "lemmatizer",
    assigns=["token.lemma"],
    default_config={"model": None, "mode": "rule", "overwrite": False},
    default_score_weights={"lemma_acc": 1.0},
)
def make_lemmatizer(
    nlp: Language, model: Optional[Model], name: str, mode: str, overwrite: bool = False
):
    return CatalanLemmatizer(nlp.vocab, model, name, mode=mode, overwrite=overwrite)


class CatalanLemmatizer(Lemmatizer):
    """
    Copied from French Lemmatizer
    Catalan language lemmatizer applies the default rule based lemmatization
    procedure with some modifications for better Catalan language support.

    The parts of speech 'ADV', 'PRON', 'DET', 'ADP' and 'AUX' are added to use
    the rule-based lemmatization. As a last resort, the lemmatizer checks in
    the lookup table.
    """

    @classmethod
    def get_lookups_config(cls, mode: str) -> Tuple[List[str], List[str]]:
        if mode == "rule":
            required = ["lemma_lookup", "lemma_rules", "lemma_exc", "lemma_index"]
            return (required, [])
        else:
            return super().get_lookups_config(mode)

    def rule_lemmatize(self, token: Token) -> List[str]:
        cache_key = (token.orth, token.pos)
        if cache_key in self.cache:
            return self.cache[cache_key]
        string = token.text
        univ_pos = token.pos_.lower()
        if univ_pos in ("", "eol", "space"):
            return [string.lower()]
        elif "lemma_rules" not in self.lookups or univ_pos not in (
            "noun",
            "verb",
            "adj",
            "adp",
            "adv",
            "aux",
            "cconj",
            "det",
            "pron",
            "punct",
            "sconj",
        ):
            return self.lookup_lemmatize(token)
        index_table = self.lookups.get_table("lemma_index", {})
        exc_table = self.lookups.get_table("lemma_exc", {})
        rules_table = self.lookups.get_table("lemma_rules", {})
        lookup_table = self.lookups.get_table("lemma_lookup", {})
        index = index_table.get(univ_pos, {})
        exceptions = exc_table.get(univ_pos, {})
        rules = rules_table.get(univ_pos, [])
        string = string.lower()
        forms = []
        if string in index:
            forms.append(string)
            self.cache[cache_key] = forms
            return forms
        forms.extend(exceptions.get(string, []))
        oov_forms = []
        if not forms:
            for old, new in rules:
                if string.endswith(old):
                    form = string[: len(string) - len(old)] + new
                    if not form:
                        pass
                    elif form in index or not form.isalpha():
                        forms.append(form)
                    else:
                        oov_forms.append(form)
        if not forms:
            forms.extend(oov_forms)
        if not forms and string in lookup_table.keys():
            forms.append(self.lookup_lemmatize(token)[0])
        if not forms:
            forms.append(string)
        forms = list(set(forms))
        self.cache[cache_key] = forms
        return forms

