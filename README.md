# Spacy 3.0 releases

Beta release for catalan Spacy 3.0 models (for testing purposes only)

https://spacy.io/usage/spacy-101

Based on BERTa transformer, Ancora corpus annotations and UDEP

Demo at:
http://temu.bsc.es:8080

# Installation:

pip install https://github.com/TeMU-BSC/spacy/releases/download/v1.3.1.0/ca_base_web_trf-3.2.3-py3-none-any.whl


# Includes:

* Noun Chunks

* NERC

* Fine-grained Parole-like POS tags

* Coarse XPOS tags

* Dependency parsing

* lookup-based lemmatization with POS disambiguation


* BERTa-based transformer

* tokenization and sentence segmentation

* Morphological analysis

# Evaluation on test split from UDEP corpus:
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
