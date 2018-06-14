import warnings
warnings.filterwarnings(action='ignore')
import pickle

import gensim
from gensim.models import Word2Vec
import pandas as pd
import matplotlib.pyplot as plt
#from nltk.stem import PorterStemmer
from sklearn.metrics import accuracy_score
import numpy as np
import math
import nltk
import itertools
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
#ps = PorterStemmer()

df1 = pd.read_csv(r"D:\kaggle\SMS SPAM\youtube\new.csv",encoding='latin-1')
df2 = pd.read_csv(r"D:\kaggle\SMS SPAM\spam_mod.csv",encoding='latin-1')

combined_data = df1.append(df2, ignore_index=True) 
ytrain = combined_data.CLASS

punctuations = [',','!',';',':','$','#','%','&','^','*','@','_','(',')','[',']','<','>','~','=','.','-','?']
punc = [',','!',';',':','$','#','%']
hyperlinks = ['http','.ly','www','/','href']

f1 = open(r"D:\main\features_list.pickle","rb")
features = pickle.load(f1)
f1.close()

f2 = open(r"D:\main\ham_model.pickle","rb")
model_ham = pickle.load(f2)
f2.close()

f3 = open(r"D:\main\spam_model.pickle","rb")
model_spam = pickle.load(f3)
f3.close()

f4 = open(r"D:\main\train_vector.pickle","rb")
train_vect = pickle.load(f4)
f4.close()

f5 = open(r"D:\main\ham_list.pickle","rb")
ham = pickle.load(f5)
f5.close()

f6 = open(r"D:\main\spam_list.pickle","rb")
spam = pickle.load(f6)
f6.close()

#spam_comments = pd.DataFrame(columns = ['comment', 'id'])
#count = 0
def hamOrSpam():
	n = 300
	count = 0
	com = pd.read_csv('com.csv')
	spam_comments = pd.DataFrame(columns = ['comment', 'id'])
	for x in range(len(com['comment'])):
		
	
		data_test = com['comment'].iloc[x]
		test_tokens = [nltk.word_tokenize(data_test)]

		mod_test_tokens = []

		for i in range(len(test_tokens)):
			temp = []
			for j in range(len(test_tokens[i])):
				test_tokens[i][j] = test_tokens[i][j].lower()
				test_tokens[i][j] = lemmatizer.lemmatize(test_tokens[i][j])
				if (test_tokens[i][j] not in stop_words) and (len(test_tokens[i][j])<=10):
					flag = 0
					for val in punctuations:
							if val in test_tokens[i][j]:
								flag = 1
					if flag == 0:
						try:
							v = int(test_tokens[i][j])
						except ValueError:
							temp.append(test_tokens[i][j])
			mod_test_tokens.append(temp)

		for i in range(len(mod_test_tokens)):
			for j in range(len(mod_test_tokens[i])):
				flag = 0
				for val in hyperlinks:
						if val in mod_test_tokens[i][j]:
							flag = 1
				if flag == 1:
						mod_test_tokens[i][j] = 'httplink'

		test_vect = np.empty([1,len(features)])
		for i in range(len(mod_test_tokens)):
			for j in range(len(features)):
				test_vect[i][j] = test_tokens[i].count(features[j])

		global embedding
		embedding = np.empty([1,2])

		for i in range(len(embedding)):

			ham_d = []
			c_ham = 0
			total_ham = 0
			
			centroid_ham = np.zeros((1,n))
			for j in range(len(test_vect[i])):
				if test_vect[i][j] > 0:
					total_ham += 1
					if features[j] in ham:
						try :
							t = model_ham[features[j]]
							centroid_ham = centroid_ham + t
							c_ham = c_ham + 1
						except KeyError:
							pass
			if c_ham == 0:        
					a = 1
			else:
				centroid_ham = centroid_ham/c_ham       
				for j in range(len(test_vect[i])):
					if test_vect[i][j] > 0:
						if features[j] in ham:
							try:
								t = model_ham[features[j]]
								val = 0
								for k in range(0,n):
									val += math.sqrt((centroid_ham[0][k]-t[k])**2)
								ham_d.append(val)
							except KeyError:
								pass
			spam_d = []  
			c_spam = 0
			total_spam = 0

			centroid_spam = np.zeros((1,n))
			for j in range(len(test_vect[i])):
				if test_vect[i][j] > 0:
					total_spam += 1
					if features[j] in spam:
						try :

							t = model_spam[features[j]]
							centroid_spam = centroid_spam + t
							c_spam = c_spam + 1
						except KeyError:
							pass
			if c_spam == 0:        
					 a = 1
			else:
				centroid_spam = centroid_spam/c_spam       
				for j in range(len(test_vect[i])):
					if test_vect[i][j] > 0:
						if features[j] in spam:
							try:
								t = model_spam[features[j]]
								val = 0
								for k in range(0,n):
									val += math.sqrt((centroid_spam[0][k]-t[k])**2)
								spam_d.append(val)
							except KeyError:
									pass

			if len(ham_d) != 0:
				if np.mean(ham_d) != 0:
					embedding[i][0] = 1/np.mean(ham_d)
				else:
					embedding[i][0] = 0   
			else:
				embedding[i][0] = 0   

			if len(spam_d) != 0:
				if np.mean(spam_d) != 0:
					embedding[i][1] = 1/np.mean(spam_d)
				else:
					embedding[i][1] = 0   
			else:
				embedding[i][1] = 0   

			del ham_d[:]
			del spam_d[:]
			del ham_d
			del spam_d



		global val1

		val1 = []
			
		class MultinomialNB(object):

				def __init__(self, alpha=1.0):
					self.alpha = alpha


				def fit(self, X, y):
					count_sample = X.shape[0]
					separated = [[x for x, t in zip(X, y) if t == c] for c in np.unique(y)]
					self.class_log_prior_ = [np.log(len(i) / count_sample) for i in separated]
					count = np.array([np.array(i).sum(axis=0) for i in separated]) + self.alpha
					self.feature_log_prob_ = np.log(count / count.sum(axis=1)[np.newaxis].T)
					return self

				def predict_log_proba(self, X):
					temp1 = [(self.feature_log_prob_ * X[x]).sum(axis=1) + self.class_log_prior_ 
							for x in range(len(X))]

					for i in range(len(temp1)):
						if abs(temp1[i][0]-temp1[i][1]) <= 1.0:
							temp1[i][0] = embedding[i][0]
							temp1[i][1] = embedding[i][1]

					list_temp1 = []
					for i in temp1:
						list_temp1.append(i.tolist())
					for i in list_temp1:
						val1.append(i)         

					return temp1

				def predict(self, X):
					return np.argmax(self.predict_log_proba(X), axis=1)



		nb = MultinomialNB()
		nb.fit(train_vect,ytrain)
		prediction = []
		prediction = nb.predict(test_vect)
		print(prediction)
		if prediction[0] == 1:
			spam_comments.loc[count] = [com['comment'].iloc[x], com['id'].iloc[x]]
			count += 1
	spam_comments.to_csv('spam_comments.csv', encoding='utf-8')
#hamOrSpam('subscribe my channel')
