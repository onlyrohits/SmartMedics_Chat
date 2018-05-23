



sentence=input("Describe your problem: ")
sentence=sentence.lower()
filepath = '123.csv'
master_list=[]
with open(filepath) as fp:  
   line = fp.readline()
   while line:
       stripped_line=line.strip()
       stripped_line = stripped_line.lower()
       strip_list=stripped_line.split(",")
       master_list.append(strip_list)
       line = fp.readline()

sum_list={}

for element in master_list:
	if sentence.find(element[1]) >= 0 :
		if not (element[0] in sum_list.keys()):
			sum_list[element[0]]=float(element[2])
		else:
			value=sum_list[element[0]]+float(element[2])
			sum_list[element[0]]=value

total=0
for value in sum_list.values():
	total = total + value

for key in sum_list.keys():
	sum_list[key] = sum_list[key]*100/total

for key,value in sum_list.items():
	print("The probability of going to {} is {} percent".format(key,value))
