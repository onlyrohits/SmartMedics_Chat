from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from autocorrect import spell

#################################################################

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

##########################################################################

sentence=input("Describe your problem: ")
sentence=sentence.lower()
filepath = '123.csv'
master_list=[]
Sym_list=[]



with open(filepath) as fp:  
   line = fp.readline()
   while line:
       stripped_line=line.strip()
       stripped_line = stripped_line.lower()
       strip_list=stripped_line.split(",")
       a=strip_list[0].split(" ")
       b=strip_list[1].split(" ")
       Sym_list.extend(a)
       Sym_list.extend(b)
       master_list.append(strip_list)
       line = fp.readline()

Sym_list=list(set(Sym_list))	
sentence=correction(sentence,Sym_list)

sum_list={}

for element in master_list:
	if sentence.find(element[1]) >= 0 :
		if not (element[0] in sum_list.keys()):
			sum_list[element[0]]=float(element[2])
			print(element[1])
			print(element[0])
		else:
			value=sum_list[element[0]]+float(element[2])
			sum_list[element[0]]=value
			print(element[1])
			print(element[0])

total=0

for value in sum_list.values():
	total = total + value

for key in sum_list.keys():
	sum_list[key] = sum_list[key]*100/total

for key,value in sum_list.items():
	print("The probability of going to {} is {} percent".format(key,value))
