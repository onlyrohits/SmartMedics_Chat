# DOCUMENTATION:
'''
The funtions declared are as follows:
	correction(sentence,List) :- returns a string of corrected words after removing stopwords and implementing autocorrect.

The variables and their datatypes and structures are as follows:
	stop_words: 		a SET of stopwords in english.
	sentence: 			a STRING that the user inputs (query).
	word_tokens: 		a LIST of words that the user enters.
	symptom_list: 		LIST of symptoms as read from the csv file.
	disease_list: 		LIST of diseases as read from the csv file.
	psych_list: 		LIST of diseases that are only treated by a psychiatrist, this will be checked only if none of the other cases match.
	keyword_list: 		LIST containing the words of all the above 3 lists. If the user entered words match any of the keywords then it will not be autocorrected.
	male: 				LIST of all the words pointing to male user.
	female: 			LIST of all the words pointing to female user.
	symptom_dict: 		DICTIONARY containing the matched list of specialists and their total weights/values.
	dominany_key: 		empty STRING that will contain the name of specialist if any dominant keyword is present.
	psych_present: 		empty STRING that will contain psychiatrist if the co-dominant keywords match.
	primary: 			LIST containing the dominant keywords
	primary_indices: 	DICTIONARY containing dominant keywords found in the list as keys and their indexes in the sentence as values.
	disease: 			empty STRING which will store the disease if found in the sentence.
	specialist:	 		empty STRING which will store the corresponding specialist of the disease found in the sentence.
	flag: 				0 if no disease found, 1 if a disease is found.
	min_key: 			minimum indexed dominant keyword.
	value: 				INT or FLOAT variable storing total weight of a particular specialist based on the number of symptoms pertaining to that specialist. 
	new_list: 			LIST containing the dictionary values as elements of the list in descending order of weights.
	print_list: 		subLIST of the new_list containing only the first two elements.

The packages imported are as follows:
	nltk version 3.3
	pandas version 0.23.0
	autocorrect version 0.3.0
'''

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from autocorrect import spell

#################################################################

# To filter the unwanted words in the sentence and also apply autocorrect
def correction(sentence,List):
	stop_words=set(stopwords.words('english'))
	word_tokens = word_tokenize(sentence)
	stop_words.remove('a')
	stop_words.remove('and')
	stop_words.remove('are')
	stop_words.remove('the')
	stop_words.remove('to')
	stop_words.remove('in')
	stop_words.remove('of')
	stop_words.remove('on')
	stop_words.remove('for')
	stop_words.remove('at')
	stop_words.remove('from')
	stop_words.remove('up')
	print("\n")
	words=[]
	filtered_sentence = [w for w in word_tokens if not w in stop_words]
	symbols=["," , ":" , ".","-"]
	sent=[w for w in filtered_sentence if not w in symbols]
	for w in sent:
	 	if w in List:
	 		words.append(w)
	 	else:
	 		try:
	 			words.append(str(float(w)))
	 		except:
	 			m=spell(w)
	 			words.append(m.lower())
	x=" ".join(words)
	return(x)

########################################################################################################

# To read the files and append the keywords, diseases and symptoms in the respective lists
sentence=input("Describe your problem: ")
sentence=sentence.lower()
filepath = 'example2.csv'
symptom_list=[]
keyword_list=[]
disease_list=[]
psych_list=[]
short_disease_list=[]


with open(filepath) as fp:  
   line = fp.readline()
   while line:
       stripped_line=line.strip()
       stripped_line = stripped_line.lower()
       strip_list=stripped_line.split(",")
       a=strip_list[0].split(" ")
       b=strip_list[1].split(" ")
       keyword_list.extend(a)
       keyword_list.extend(b)
       symptom_list.append(strip_list)
       line = fp.readline()

with open('DiseasesData.csv') as fp:
	line = fp.readline()
	while line:
		stripped_line=line.strip()
		stripped_line=stripped_line.lower()
		strip_list=stripped_line.split(",")
		a=strip_list[0].split(" ")
		b=strip_list[1].split(" ")
		keyword_list.extend(a)
		keyword_list.extend(b)
		disease_list.append(strip_list)
		line=fp.readline()

with open('psychiatrist.csv') as fp:
	line = fp.readline()
	while line:
		stripped_line=line.strip()
		stripped_line=stripped_line.lower()
		strip_list=stripped_line.split(",")
		a=strip_list[0].split(" ")
		b=strip_list[1].split(" ")
		keyword_list.extend(a)
		keyword_list.extend(b)
		psych_list.append(strip_list)
		line=fp.readline()

with open('short_diseases.csv') as fp:
	line = fp.readline()
	while line:
		stripped_line=line.strip()
		stripped_line=stripped_line.lower()
		strip_list=stripped_line.split(",")
		a=strip_list[0].split(" ")
		b=strip_list[1].split(" ")
		keyword_list.extend(a)
		keyword_list.extend(b)
		short_disease_list.append(strip_list)
		line=fp.readline()

keyword_list=list(set(keyword_list))	
sentence=correction(sentence,keyword_list)


###############################################################################################

# To read the file and append the male and female words in their lists accordingly
male=[]
female=[]
filename='MaleFemale.csv'
dataset=pd.read_csv(filename)
array=dataset.values
for i in array:
	male.append(i[0])
	female.append(i[1])

gender=''
for sex in word_tokenize(sentence):
	if sex in male:
		gender='Male'
		break
	elif sex in female:
		gender='Female'
		break

#####################################################################################

# Step1: check if any disease is mentioned, if yes, send it to the specialist. If not, move to step 2
# Step2: check if anydominant keyword is present, if yes, send it to the specialist. If not, move to step 3
# Step3: check if symptoms match those in the symptom_list, if yes, calculate accordingly. If not, move to step 4
# Step4: check if any psychiatric symptoms are present, if yes, refer to a psychiatrist. End.
symptom_dict={}
dominant_key=''
psych_present=''
primary=['sex', 'cancer','abortion','penis','testes','testicles']
primary_indices={}
flag=0
disease=""
specialist=""
for elements in short_disease_list:
	if elements[1] in word_tokenize(sentence):
		specialist1=elements[0]
		print('In our opinion you should consult a '+specialist1)
		break
	else:
		for element in disease_list:
			if sentence.find(element[1])>=0:
				flag=1
				disease=element[1]
				specialist=element[0]
				break
		if flag==1:
			print("You should consult a {} for {}".format(specialist,disease))
			break
		elif flag==0:	
			for m in primary:
				if sentence.find(m)>=0:
					primary_indices[m]=sentence.find(m)

			min_key=''

			for key,value in primary_indices.items():
				if primary_indices[key]==min(primary_indices.values()):
					min_key=key

			if min_key=='sex':
				if gender=='Female' or sentence.find('pregnancy')>=0 or sentence.find('pregnant')>=0 or sentence.find('period')>=0 :
					if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
						dominant_key='gynaecologist'
						psych_present='psychiatrist'
						print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						break
					else:
						dominant_key='gynaecologist'
						print('There is a high probability that you should consult a '+dominant_key)
						break
				else:
					if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
						dominant_key='sexologist'
						psych_present='psychiatrist'
						print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						break
					elif sentence.find('period')>=0 or sentence.find('abortion')>=0:
						dominant_key='gynaecologist'
						print('There is a high probability that you should consult a '+dominant_key)
						break
					else:
						dominant_key='sexologist'
						print('There is a high probability that you should consult a '+dominant_key)
						break

			elif min_key=='penis':
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
						dominant_key='sexologist'
						psych_present='psychiatrist'
						print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						break

			elif min_key=='testicles':
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
						dominant_key='sexologist'
						psych_present='psychiatrist'
						print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						break

			elif min_key=='testes':
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
						dominant_key='sexologist'
						psych_present='psychiatrist'
						print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						break

			elif min_key=='cancer':
				dominant_key='oncologist'
				print('There is a high probability that you should consult a '+ dominant_key)
				break
			elif sentence.find('abortion')>=0 or sentence.find('period')>=0 :
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
					dominant_key='gynaecologist'
					psych_present='psychiatrist'
					print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
					break
				else:
					dominant_key='gynaecologist'
					print('There is a high probability that you should consult a '+dominant_key)
					break


			else:
				for element in symptom_list:
					if sentence.find(element[1]) >= 0 :
						if not (element[0] in symptom_dict.keys()):
							symptom_dict[element[0]]=float(element[2])
						else:
							value=symptom_dict[element[0]]+float(element[2])
							symptom_dict[element[0]]=value
				total=0
				for value in symptom_dict.values():
					total = total + value
				for key in symptom_dict.keys():
					symptom_dict[key] = symptom_dict[key]*100/total

				new_list=sorted(symptom_dict.items(), key = lambda t: t[1], reverse = True)
				print_list=[]
				flag1=0
				for item in new_list:
					flag1=flag1+1
					if flag1 < 3:
						print_list.append(item[0])
				if print_list!=[]:
					print('Based on the symptoms you should consult a '+' and '.join(print_list))	
					break
				if symptom_dict=={}:
					for element in psych_list:
						if sentence.find(element[1])>=0:
							print('You should visit a psychiatrist')
							break