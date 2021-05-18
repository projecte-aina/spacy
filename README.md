# Spacy 3.0 releases

Beta release for catalan Spacy 3.0 models (for testing purposes only)

https://spacy.io/usage/spacy-101

Demo at:
http://temu.bsc.es:8080


# Sources
Based on BERTa transformer, AnCora corpus annotations and UDEP treebanks, all merged into single training/dev corpora to enable simultaneous multi-task training.

## Transformer:

BERTa @ Hugging Face, a RoBERTa transformer from the 1.760 million token Catalan General Corpus (https://doi.org/10.5281/zenodo.4519348) 

## Dependency Treebank, XPOS, sentence segmentation

From version 3.6, with changes for pronouns and multi-word tokenization 

https://universaldependencies.org/ca/


## Lemmatization

Adaptation of French lemmatizer, using inhouse-developed word lists and corpus frequencies

## Named Entity Recognition

From original AnCora corpus (https://doi.org/10.5281/zenodo.4529299)

## Word vectors

From FAstText word embeddings: https://doi.org/10.5281/zenodo.4522040

## Text Classification (To come)

From TeCla corpus based on Agencia Catalana de Noticias Newswire
(https://doi.org/10.5281/zenodo.4627197)

# Installation:

pip install https://github.com/TeMU-BSC/spacy/releases/download/v1.3.2.3/ca_base_web_trf-3.2.3-py3-none-any.whl


# Includes:

* Noun Chunks

* NERC

* Fine-grained Parole-like POS tags (to come)

* Coarse XPOS tags

* Dependency parsing

* lookup-based lemmatization with POS disambiguation

* BERTa-based transformer

* tokenization and sentence segmentation

* Morphological analysis

* Text classification

* Static word vectors (in core model)
* 

# External evaluation on test split from UDEP corpus:
```
  "token_acc":1.0,
  "tag_acc":0.9899974352,
  "pos_acc":0.9897161029,
  "morph_acc":0.9810507962,
  "lemma_acc":0.9317458328,
  "dep_uas":0.9419736427,
  "dep_las":0.9186940555,
  "ents_p":0.9206049149,
  "ents_r":0.9145539906,
  "ents_f":0.9175694772,
  "sents_p":0.9938271605,
  "sents_r":0.9969040248,
  "sents_f":0.9953632148,
  "speed":4203.8544117436,
```
