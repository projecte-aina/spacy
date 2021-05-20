# Spacy 3.0 releases

Public release for catalan Spacy 3.0 models

Spacy usage basics: https://spacy.io/usage/spacy-101

Demo at: http://temu.bsc.es:8080

# Versions

- **ca_base_web_trf** & **ca_core_web_trf** contain a Catalan RoBERTa-based transformer as a common backbone for multitask training of the different components. The latter one ("core") also contains FastText embeddings to measure lexical similarity, although the "base" version can also measure semantic similarity, but using NER, dependency and other information, not directly on a dedicated distance matrix.

- **ca_core_web_lg**, on the other hand, uses FastText embeddings as a training backbone, so it doesn't need transformers or GPUs.

This is the pre-production releases, and a spacy "official" release will be forthcoming.


# Installation:

## base model without word vectors:

pip install https://github.com/TeMU-BSC/spacy/releases/download/v3.2.4/ca_base_web_trf-3.2.4-py3-none-any.whl

## core model with word embeddings for lexical similarity

pip install https://github.com/TeMU-BSC/spacy/releases/download/v3.2.4.core/ca_core_web_trf-3.2.4-py3-none-any.whl

## core model without BERTa transformer, but with Fasttext embeddings

pip install https://github.com/TeMU-BSC/spacy/releases/download/v3.2.4lg/ca_core_web_lg-3.2.4-py3-none-any.whl

# Sources
Based on BERTa transformer, AnCora corpus annotations and UDEP treebanks, all merged into single training/dev corpora to enable simultaneous multi-task training.
https://github.com/TeMU-BSC/spacy/releases/download/3.2.4/ANCORA_ca.zip

## Transformer:

BERTa @ Hugging Face, a RoBERTa transformer from the 1.760 million token Catalan Text Corpus (https://doi.org/10.5281/zenodo.4519348) 

## Dependency Treebank, XPOS, sentence segmentation

From version 3.6 of the Catalan Universal Dependencies (https://universaldependencies.org/ca/) project treebank, with changes for pronouns and multi-word tokenization 


## Lemmatization

Adaptation of French lemmatizer, using  word lists and corpus frequencies developed in house.

## Named Entity Recognition

From original AnCora corpus (https://doi.org/10.5281/zenodo.4529299)

## Word vectors ("core" model only)

From FastText word embeddings: https://doi.org/10.5281/zenodo.4522040


# External evaluation on test split for ca_base_web_trf:
```
  "token_acc":1.0,
  "tag_acc":0.9897155754,
  "pos_acc":0.9891000487,
  "morph_acc":0.9807149818,
  "lemma_acc":0.9307432009,
  "dep_uas":0.9424871508,
  "dep_las":0.9204281328,
  "ents_p":0.9226415094,
  "ents_r":0.9183098592,
  "ents_f":0.9204705882,
  "sents_p":0.9953488372,
  "sents_r":0.9938080495,
  "sents_f":0.9945778466,
  "speed":4177.1171988569,
```
<!---## Text Classification (To come)

From TeCla corpus based on Agencia Catalana de Noticias Newswire
(https://doi.org/10.5281/zenodo.4627197)-->


<!---
# Includes:

* Noun Chunks

* NERC

* Coarse XPOS tags

* Dependency parsing

* lookup-based lemmatization with POS disambiguation

* BERTa-based transformer

* tokenization and sentence segmentation

* Morphological analysis

* Static word vectors (in core models)

## To come:
* Fine-grained Parole/Eagles POS tags

* Text classification  


