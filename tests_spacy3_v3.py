#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 11:44:48 2021
proves per a fer amb l'spacy3
Env: spacy_nou
@author: carme

ATENCIÓ!!!!!
cal haver-se intal·lat l'spacy i el deplacy:
    
  pip install -U pip setuptools wheel
  pip install spacy
  pip install deplacy
"""

import spacy
import deplacy

nlp = spacy.load("ca_core_web_trf")

# escriure aquí el text que es vol analitzar
doc = nlp("La Guàrdia Urbana de Barcelona (GUB) va desallotjar ahir dissabte a la nit una festa il·legal en un bar musical al districte de Ciutat Vella. Dins el local hi havia una cinquantena de persones que no respectaven cap de les mesures contra la Covid-19 i incomplien restriccions com el toc de queda nocturn.") 


# alternativament, podem obrir un fitxer de text per analitzar-lo
# doc = nlp(open('/tmp/text3.txt', 'r').read()) #posar el nom del fitxer que volem que analitzi

"""
 nlp processa el text. 
 El primer que fa és tokenitzar el text, de manera que doc és una llista de tokens amb propietats. 
 A partir d'aquí podem aplicar loops for per cada un dels tokens de doc.
"""


def segmentation(doc):  
    # segmenta el text en oracions i compta quants tokens té cada una
    print("SEGMENTACIÓ")
    print("Aquest text consta de", len(list(doc.sents)), "frases:")
    for sent in doc.sents:
        print("\t*", sent.text)
        print("\tAquesta frase té", len(sent), "tokens")
    print("")    

def semantics(doc):
    # per cada token, informa de si té vector, el vector i si és oov
   
    print("INFORMACIÓ SEMÀNTICA")
    print("token \t\t hasvector \tvector norm \tis oov")
    for token in doc:
       print(f'{token.text}\t\t{token.has_vector}\t\t{token.vector_norm}\t\t{token.is_oov}')
    
    print("")  
    
def pos_and_dep(doc):
    # per cada token, imprimeix el lema, POS, dep, el cap i la info morfològica disponible
    
    print("ANÀLISI POS, DEP I MORFO")
    print("token \t\tlema \tpos \tdep \thead \tmorph")
    for token in doc:
        print(f'{token.text}\t\t{token.lemma_}\t\t{token.pos_}\t\t{token.dep_}\t\t{token.head}\t\t{token.morph}')
    
    print("")

def dependencies(doc):
    deplacy.render(doc)  
    print("")
    
def entities(doc):
    # troba les name entities del text i les mostra amb la seva categoria
    print("NAMED ENTITIES")
    print("entity\tlabel")
    for ent in doc.ents:
        print(f'{ent.text}\t{ent.label_}')
    print("")
    

def chunks(doc):
    # imprimeix els chunks nominals i la seva arrel
    print("NOUN CHUNKS")    
    print("chunk \t\t\t\troot")
    for chunk in doc.noun_chunks:
        print(f'{chunk.text} --> {chunk.root.text}')
      
    print("")
 
    
def analyse(doc):
    # aplica totes les funcions, una després de l'altra
    segmentation(doc)
    semantics(doc)
    pos_and_dep(doc)
    dependencies(doc)
    entities(doc)
    chunks(doc)
    
analyse(doc)