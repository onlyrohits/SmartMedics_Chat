from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import csv
############################################################
def parse(words):
	word_list=[]
	stop_words = set(stopwords.words('english'))
	for element in words:
		if not (element == ',' or element =='.' or element ==':') :
			if element not in stop_words:
				if ":" in element:
					split_list=element.split(":")
					word_list.extend(split_list)
				else:
					word_list.append(element)
	return word_list

##################################
description=input("Enter String: ")
temp_words=word_tokenize(description)
word_list=parse(temp_words)
print(word_list)
##################################
male=[]
female=[]
filename='MaleFemale.csv'
dataset=pd.read_csv(filename)
array=dataset.values
for i in array:
	male.append(i[0])
	female.append(i[1])
#####################################################

gender=''
for sex in word_list:
	if sex in male:
		gender='Male'
		break
	elif sex in female:
		gender='Female'
		break

print(gender)




