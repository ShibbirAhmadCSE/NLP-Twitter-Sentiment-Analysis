# -*- coding: utf-8 -*-
"""NLP: Twitter Sentiment Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15cWL1vLh18aUtoTQGKclCWj5aUDsTY87
"""

from google.colab import drive
drive.mount('/content/drive/')

#IMPORT LIBRARIES

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from jupyterthemes import jtplot
jtplot.style(theme='monokai', context='notebook', ticks=True, grid=False)

df = pd.read_csv('/content/drive/MyDrive/Dataset/tweets.csv')
df.head()

df.drop(['textID','selected_text'], axis='columns',inplace=True)
df.head()

df.drop_duplicates(inplace = True)
df.head()

df.isnull().sum()

df[df['text'].isnull()]

#drop all Null values
data = df.dropna()
data.head()

data.isnull().sum()

sns.countplot(data['sentiment'], label = "Count") 
plt.show()

def label(x):
        if x=='positive': return 1
        if x=='neutral':   return 0
        if x=='negative': return -1

data['sentiment_label'] = data['sentiment'].apply(label)
data.head()

data.drop(['sentiment'], axis='columns',inplace=True)
data.head()

sentences = data['text'].tolist()
sentences

sentences_as_one_string = " ".join(sentences)

from wordcloud import WordCloud
plt.figure(figsize=(10,10))
plt.imshow(WordCloud().generate(sentences_as_one_string))
plt.show()

#DATA CLEANING - REMOVE PUNCTUATION FROM TEXT

import string
string.punctuation

Test = 'Good morning beautiful people :)... I am having fun learning Machine learning and AI!!'

Test_punc_removed = [ char for char in Test if char not in string.punctuation ]

Test_punc_removed

# Join the characters again to form the string.
Test_punc_removed_join = ''.join(Test_punc_removed)
Test_punc_removed_join

#DATA CLEANING - REMOVE STOPWORDS

import nltk # Natural Language tool kit 
nltk.download('stopwords')

# Download stopwords Package 
from nltk.corpus import stopwords
print(stopwords.words('english'))

Test_punc_removed_join_clean = [ word for word in Test_punc_removed_join.split() if word.lower() not in stopwords.words('english')]
print(Test_punc_removed_join_clean) # Only important (no so common) words are left

#PERFORM COUNT VECTORIZATION (TOKENIZATION)

from sklearn.feature_extraction.text import CountVectorizer
sample_data = ['This is the first paper.','This document is the second paper.','And this is the third one.','Is this the first paper?']

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sample_data)

print(vectorizer.get_feature_names())

print(X.toarray())

#CREATE A PIPELINE

def message_cleaning(message):
    Test_punc_removed = [char for char in message if char not in string.punctuation]
    Test_punc_removed_join = ''.join(Test_punc_removed)
    Test_punc_removed_join_clean = [word for word in Test_punc_removed_join.split() if word.lower() not in stopwords.words('english')]
    return Test_punc_removed_join_clean

# Let's test the newly added function
data_clean = data['text'].apply(message_cleaning)

print(data_clean[5]) # show the cleaned up version

print(data['text'][5]) # show the original version

from sklearn.feature_extraction.text import CountVectorizer

# Define the cleaning pipeline 
vectorizer = CountVectorizer(analyzer = message_cleaning, max_features=8000)
tweets_countvectorizer = vectorizer.fit_transform(data['text'])

print(vectorizer.get_feature_names())

print(tweets_countvectorizer.toarray())

tweets_countvectorizer.shape

X = pd.DataFrame(tweets_countvectorizer.toarray())
 X.head()

y = data['sentiment_label']

X.shape, y.shape

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#TRAIN MODEL

from sklearn.naive_bayes import MultinomialNB
classifier1 = MultinomialNB()
classifier1.fit(X_train, y_train)

#ASSESS TRAINED MODEL PERFORMANCE

from sklearn.metrics import classification_report, confusion_matrix

# Predicting the Test set results
y_predict_test1 = classifier1.predict(X_test)
cm = confusion_matrix(y_test, y_predict_test1)
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_predict_test1))

from sklearn.svm import LinearSVC
classifier2 = LinearSVC()
classifier2.fit(X_train, y_train)

# Predicting the Test set results
y_predict_test2 = classifier2.predict(X_test)
cm = confusion_matrix(y_test, y_predict_test2)
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_predict_test2))

from sklearn.linear_model import LogisticRegression
classifier3 = LogisticRegression(solver='lbfgs', max_iter=400)
classifier3.fit(X_train, y_train)

# Predicting the Test set results
y_predict_test3 = classifier3.predict(X_test)
cm = confusion_matrix(y_test, y_predict_test3)
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_predict_test3))

