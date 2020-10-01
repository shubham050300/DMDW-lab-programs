import pandas
import numpy as np

def loaddata():
	datas=pandas.read_csv("Test.csv")
	x=datas.values
	data=[]
	for i in range(len(x)):
		a=[]
		for j in range(len(x[i])):
		    if x[i][j]==x[i][j]:
		          a.append(x[i][j])
		a.append(str(i))
		data.append(a)
	# print(data)
	return data

def prunerow(mincar,x):
	i=0
	while i < (len(x)):
		car=0
		j=0
		while j < (len(x[0])-1):
			car+=x[i][j]
			j+=1
		if car<mincar:
			x.pop(i)
		i+=1
	return x

def prunecol(minsup,x):
	j=0
	while j < (len(x[0])-1):
		sup=0
		i=0
		while i < (len(x)):
			sup+=x[i][j]
			i+=1
		if sup<minsup:
			for k in x:
				del k[j]
		j+=1
	return x

def rowenuml2(x):
	l1=[]
	for i in range(len(x)):
		for j in range(i+1,len(x)):
			l=[]
			for k in range(len(x[0])-1):
				if i!=j:
					l.append(x[i][k] and x[j][k])
			l.append(str(i)+str(j))
			l1.append(l)
	return l1

def rowenuml3(x):
	l1=[]
	for i in range(len(x)):
		for j in range(i+1,len(x)):
			l=[]
			for k in range(len(x[0])-1):
				if i!=j and x[i][len(x[0])-1][0]==x[j][len(x[0])-1][0]:
					l.append(x[i][k] and x[j][k])
			if l==[]:
				continue
			l.append(str(x[i][len(x[0])-1][0])+str(x[i][len(x[0])-1][1])+str(x[j][len(x[0])-1][1]))
			l1.append(l)
	return l1

def rowenum(x):
	l1=[]
	for i in range(len(x)):
		for j in range(i+1,len(x)):
			l=[]
			n=len(x[0][len(x[0])-1])-1
			# print(x[i][len(x[0])-1][:n]," ",x[i][len(x[0])-1])
			x1=x[i][len(x[0])-1][:n]
			x2=x[j][len(x[0])-1][:n]

			if x1==x2:
				for k in range(len(x[0])-1):
					if i!=j:
						l.append(x[i][k] and x[j][k])
			if l==[]:
				continue
			l.append(str(x1)+str(x[i][len(x[0])-1][n])+str(x[j][len(x[0])-1][n]))
			l1.append(l)
	return l1

def printx(x):
	for i in range(len(x)):
		if len(x[0])==1:
			continue
		for j in range(len(x[0])):
			print(x[i][j]," ",end='')
		print()

def colo(x):
	minsup=2
	mincar=2

	print("initial")
	printx(x)

	for i in range(5):
		if x==[]:
			break
		x=prunerow(mincar,x)
		if x==[]:
			break
		x=prunecol(minsup,x)
	print("l1")
	print(x)
	printx(x)
	print("Number of colossal itemsets in l1: ",len(x))

	l2=rowenuml2(x)
	print("l2")
	for i in range(5):
		if l2==[]:
			break
		l2=prunerow(mincar,l2)
		if l2==[]:
			break
		l2=prunecol(minsup,l2)
	printx(l2)
	print("Number of colossal itemsets in l2: ",len(l2))

	l3=rowenuml3(l2)
	print("l3")
	for i in range(5):
		if l3==[]:
			break
		l3=prunerow(mincar,l3)
		if l3==[]:
			break
		l3=prunecol(minsup,l3)
	printx(l3)
	print("Number of colossal itemsets in l3: ",len(l3))

	l4=rowenum(l3)
	print("l4")
	for i in range(5):
		if l4==[]:
			break
		l4=prunerow(mincar,l4)
		if l4==[]:
			break
		l4=prunecol(minsup,l4)
	printx(l4)
	print("Number of colossal itemsets in l4: ",len(l4))

def main():
	x=loaddata()
	colo(x)

if __name__=='__main__':
	main()