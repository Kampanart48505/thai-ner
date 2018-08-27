# -*- coding: utf-8 -*-
# เรียกใช้งานโมดูล
file_name="data"
import codecs
from pythainlp.tokenize import word_tokenize
#import deepcut
from pythainlp.tag import pos_tag
from nltk.tokenize import RegexpTokenizer
import glob
import nltk
import re
# thai cut
thaicut="newmm"

from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import sklearn_crfsuite
from pythainlp.corpus import stopwords
stopwords = stopwords.words('thai')


def isThai(chr):
 cVal = ord(chr)
 if(cVal >= 3584 and cVal <= 3711):
  return True
 return False
def isThaiWord(word):
 t=True
 for i in word:
  l=isThai(i)
  if l!=True:
   t=False
   break
 return t

def is_stopword(word):
    return word in stopwords
def is_s(word):
    if word == " " or word =="\t" or word=="":
        return True
    else:
        return False
def doc2features0(doc, i):
    word = doc[i][0]
    postag = doc[i][1]
    # Features from current word
    features={
        'word.word': word,
        'word.stopword': is_stopword(word),
        'word.isthai':isThaiWord(word),
        'postag':postag,
        'postag[:2]': postag[:2],
        'word.isdigit()': word.isdigit(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:]
    }
    # Features from previous word
    if i > 0:
        prevword = doc[i-1][0]
        postag1 = doc[i-1][1]
        features['word.prevword'] = prevword
        features['word.previsthai']=isThaiWord(prevword)
        features['word.prevstopword']=is_stopword(prevword)
        features['word.prepostag'] = postag1
        features['-1:postag[:2]']: postag1[:2]
        features['word.prevwordisdigit'] = prevword.isdigit()
    else:
        features['BOS'] = True # Special "Beginning of Sequence" tag
    # Features from next word
    if i < len(doc)-1:
        nextword = doc[i+1][0]
        postag1 = doc[i+1][1]
        features['word.nextword'] = nextword
        features['word.nextpostag'] = postag1
        features['word.nextisthai']=isThaiWord(nextword)
        features['word.nextstopword']=is_stopword(nextword)
        features['word.nextwordisdigit'] = nextword.isdigit()
        features['+1:postag[:2]']: postag1[:2]
    else:
        features['EOS'] = True # Special "End of Sequence" tag
    return features
def extract_features0(doc):
    return [doc2features0(doc, i) for i in range(len(doc))]

def get_labels(doc):
    return [tag for (token,postag,tag) in doc]

crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=500,
    all_possible_transitions=True,
    model_filename=file_name+"-pos-new.model2"
)
def get_ner(text):
    word_cut=word_tokenize(text,engine=thaicut)
    list_word=pos_tag(word_cut,engine='perceptron')
    #print(list_word)
    X_test = extract_features0([(data,list_word[i][1]) for i,data in enumerate(word_cut)])
    y_=crf.predict_single(X_test)
    return [(word_cut[i],list_word[i][1],data) for i,data in enumerate(y_)]


while True:
    t=input("Text : ")
    print(get_ner(t))