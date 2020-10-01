import csv

# def load_data() :
# 	dset = []
# 	with open('test_dataset_1.csv') as csv_file:
# 		csv_reader = csv.reader(csv_file, delimiter=',')
# 		for row in csv_reader:
# 			dset.append(row)
# 	return dset

def load_data() :
	dset = []
	with open('retail_dataset.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count != 0 :
				dset.append(row)
			line_count += 1
	return dset

def self_join(l,epoch):
	c={}
	common_elements=epoch-1
	keys_list = []
	for i in l.keys():
		keys_list.append(list(i.split(",")))
	# print("\nkeys_list",keys_list)


	for i in range(len(l)):
		for j in range(i+1,len(l)):
			flag=1
			for z in range(common_elements):
				if(keys_list[i][z]!=keys_list[j][z]):
					flag=0
			if(flag==1):
				new_key=[]
				if(common_elements!=0):
					for z in range(common_elements):
						new_key.append(keys_list[i][z]) 
				new_key.append(keys_list[i][common_elements])
				new_key.append(keys_list[j][common_elements])
				
				c[','.join(new_key)] = 0
	# print("\n\n",c,"\n\n")
	return c


def apriori(x):
	min_support=3000
	epoch=0

	c={}
	for i in range(len(x)):
		for j in range(len(x[i])):
			if(x[i][j] not in c.keys()):
				c[x[i][j]]=1
			else:
				c[x[i][j]]+=1

	while(True):

		epoch+=1
		if(epoch!=1):
			for i in c.keys() :
					for j in range(len(x)) :
						if set(i.split(',')) & set(x[j]) == set(i.split(',')) :
							c[i] += 1

		print("Length of C",epoch,": ",len(c))
		# print(c)
		if(len(c)==0):
			break

		l={}
		for i in c.keys():
			if(c[i]>=min_support):
				l[i]=c[i]

		print("Length of L",epoch,": ",len(l))
		print("L",epoch,":",l,"\n")
		if(len(l)==0):
			break

		c = self_join(l,epoch)



def main():
	x=load_data()
	apriori(x)

if __name__=='__main__':
	main()