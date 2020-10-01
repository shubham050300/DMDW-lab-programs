import pandas
import numpy as np

def loaddata():
	datas=pandas.read_csv("retail_dataset.csv")
	x=datas.values
	data=[]
	for i in range(len(x)):
	  a=[]
	  for j in range(len(x[i])):
	      if x[i][j]==x[i][j]:
	          a.append(x[i][j])
	  data.append(a)
	return data

def sameitemset(i1,i2):
	i1.sort()
	i2.sort()
	if i1==i2:
		return True
	return False

def ispresent(c,x):
	if(all(a in x for a in c)):
		return True
	return False

def findfreq(c,x):
	res=[]
	for i in range(len(c)):
		count=0
		for j in range(len(x)):
			if ispresent(c[i],x[j]):
				count+=1
		res.append([c[i],count])
	return res

def find_l(x,min_sup):
	l=[]
	for i in range(len(x)):
		if x[i][1]>=min_sup:
			l.append(x[i][0])
	return l

def self_join_l(l):
	for i in range(len(l)):
		l[i].sort()
	#print(l)
	res=[]

	for i in range(len(l)):
		for j in range(len(l)):
			if i!=j:
				n=len(l[i])-1
				l1=l[i][:n]
				l2=l[j][:n]
				#print(l1)
				#print(l2)
				if l1==l2:
					l3=l[i][:]
					l3.append(l[j][len(l[j])-1])
					res.append(l3)
	i=0
	while i<len(res):
		j=0
		while j<len(res):
			if i==j:
				j+=1
			elif i!=j and sameitemset(res[i],res[j]):
				res.pop(j)
			else:
				j+=1
		i+=1

	return res

def apriori(x):
	min_sup=3000

	#step 1: find frequency of itemset and create C
	freq={}
	for i in range(len(x)):
		for j in range(len(x[i])):
			if (x[i][j] not in freq.keys()):
				freq[x[i][j]] = 1
			else:
				freq[x[i][j]] += 1
	# for key,value in freq.items():
	#   print(key," ",value)

	#step 2: find frequent itemsets and form L
	l1=[]
	for key,value in freq.items():
		if value>=min_sup:
			l1.append(key)
	print("The number of elements in L1 is : ",len(l1))
	#print(l1)

	#step 3: self join L1 to find the elements in C for the next iteration
	c2=[]
	for i in range(len(l1)):
		for j in range(len(l1)):
			if i!=j:
				c2.append([l1[i],l1[j]])

	i=0
	while i<len(c2):
		j=0
		while j<len(c2):
			if i==j:
				j+=1
			elif i!=j and sameitemset(c2[i],c2[j]):
				c2.pop(j)
			else:
				j+=1
		i+=1

	#print(c2)

	#step 4:Find L2
	freq=findfreq(c2,x)
	l2=find_l(freq,min_sup)
	print("The number of elements in L2 is : ",len(l2))
	#print(l2)

	#step 5:generate C's and L's in a general way
	for i in range(100):
		if i==0:
			c=c2[:]
			l=l2[:]
		else:
			l=l3[:]
		l.sort()
		#print(l)
		c=self_join_l(l)
		#print(c)
		fr=findfreq(c,x)
		l=find_l(fr,min_sup)
		#print(fr)
		l3=l[:]
		if l==[]:
			break
		print("The number of elements in L",(i+3),"is: ",len(l))
		#print(l)
		if len(c)<=1:
			break

def main():
	x=loaddata()
	apriori(x)

if __name__=='__main__':
	main()