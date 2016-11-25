# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 11:14:39 2016

@author: ap4409
"""

# ---------------------------------------------------------------------------
# HEADERS
# ---------------------------------------------------------------------------

import sys
sys.path.append('toolbox')
from nltkExtra import cleanText as clean
import gensim 
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# INPUTS
# ---------------------------------------------------------------------------

fname = 'testResults/bleh.csv';
N_ITER = 40;
NUM_TOPIC = 10;

# ---------------------------------------------------------------------------
# SIMULATION ENGINE
# ---------------------------------------------------------------------------

# Read and organising data
data = pd.read_csv(fname)

title = [term[0] for term in data.values];
abstract = [term[1] for term in data.values];

# Cleaning text
titleCln = clean(title,'en');
abstractCln = clean(abstract,'en');

textCln = titleCln;

# Bag of words
dictionary = gensim.corpora.Dictionary(textCln)

# Convert tokenized documents into a document-term matrix (bag of words)
corpus = [dictionary.doc2bow(text) for text in textCln]

# Generate LDA model
lda = gensim.models.LdaModel(corpus, num_topics=NUM_TOPIC, id2word = dictionary, passes=N_ITER)

# Print topics
topics = lda.show_topics(NUM_TOPIC)

# Generate visualisation (only for Ipython notebook)
#import pyLDAvis.gensim
#vis_data = pyLDAvis.gensim.prepare(lda,corpus,dictionary)
#pyLDAvis.save_html(vis_data,'LDA_VisualizationLitReview.html')

# Return all document topics
def get_doc_topics(lda, bow):
    gamma, _ = lda.inference([bow])
    topic_dist = gamma[0] / sum(gamma[0])  # normalize distribution
    return [(topicid, topicvalue) for topicid, topicvalue in enumerate(topic_dist)]

# Function that returns blueprint of each document
def returnBlueprint(lda,corpus):
    
    blueprint_per_doc = [];
    docID = 0;
    
    for text in corpus:

        currentTopList = get_doc_topics(lda,text);
        topArray = [];

        for currentTop in currentTopList:        
            
            topID = currentTop[0];
            score = currentTop[1];
        
            topArray.append(score);
            
        blueprint_per_doc.append(topArray);
        docID += 1;
        
    return blueprint_per_doc;

# Function for dimensionality reduction
def dimensionalityReduction(blueprint):
    
    model = TSNE(n_components=2,random_state=0);
    data = model.fit_transform(blueprint);
    
    X = [term[0] for term in data];
    Y = [term[1] for term in data]
    
    return X,Y
    
# Function for clustering
def cluster(data,N_GROUPS):
    model = KMeans(n_clusters = N_GROUPS);
    model.fit(data);
    
    return model.labels_

# Function for determining similarity between 2 data sets
# INSERT HERE JENSEN-SHANNON distance

  
# Return topic distribution for each document
blueprint =  returnBlueprint(lda,corpus)

# Return dimensionality reduction
[X,Y] = dimensionalityReduction(blueprint)

# Cluster the data
labels = cluster(blueprint,2)

# Plot results
plt.scatter(X,Y,s=40,c=labels)
plt.show()

'''

# OTHER THINGS TO CONSIDER
# Train LDA model
# Use titles or abstracts?
# Other algorithms for topic modelling?

# Finding main topic for each document
docID = 0;
topic_for_document = {};
for text in corpus:

    currentTopList = lda.get_document_topics(text);
    topic_for_document[docID] = 'N/A'
    
    for currentTop in currentTopList:
        topID = currentTop[0];
        score = currentTop[1];
        
        if score > 0.8:
            topic_for_document[docID] = topID
    
    docID += 1;
    
# Organising documents by topic
classDocuments = {k: [] for k in range(NUM_TOPIC)}
classDocuments['Not Clear Topic'] = [];

for docID in topic_for_document.keys():
    
    if topic_for_document[docID] != 'N/A':
        classDocuments[topic_for_document[docID]].append(title[docID]);
        
    else:
        classDocuments['Not Clear Topic'].append(title[docID])

'''