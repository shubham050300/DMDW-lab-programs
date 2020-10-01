import csv

pattern = {}
conditional = {}

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


def traverse_tree(tree, parents):
	level  = tree[:]
	for i in range(len(level)):
		
		if level[i][0][0] not in pattern.keys():
			pattern[level[i][0][0]] = []
			
		pattern[level[i][0][0]].append([parents[:],level[i][0][1]])
		parents.append(level[i][0][0])
		traverse_tree(level[i][1],parents)
		parents.pop()

def create_tree(tree,path):
	level = tree
	for i in range(len(path)):
		found = False
		for j in range(len(level)):
			if level[j][0][0] == path[i]:
				level[j][0][1]+=1
				found = True
				level = level[j][1]
				break
		if found == False:
			level.append(([path[i],1],[]))
			level = level[-1][1]
	return tree

def conditional_fp(min_support):
	for k,v in pattern.items():
		conditional[k] = []

	for k,vx in pattern.items():
		v = vx[:]
		temp = {}
		for i in range(len(v)):
			for j in range(0,len(v[i][0]),1):
			
				if v[i][0][j] not in temp.keys():
					temp[v[i][0][j]] = 0
				temp[v[i][0][j]]+=1
		print(temp)
		for kk,vv in temp.items():
			if vv>=min_support:
				conditional[k].append((kk,vv))

def add_node(tree,path):
    level = tree
    for i in range(len(path)):
        found = False
        for j in range(len(level)):
            if level[j][0][0] == path[i]:
                level[j][0][1]+=1
                found = True
                level = level[j][1]
                break
        if found == False:
            level.append(([path[i],1],[]))
            level = level[-1][1]
        print(level)
    return tree

def fp_tree(x):
	min_sup=2
	confidence=0.7
	tree=[]
	for i in range(len(x)):
		tree=create_tree(tree,x[i])
	# print(tree)
	print("tree created")

	#step 4: Mining FP tree
	traverse_tree(tree,[])
	#print(pattern)
	conditional_fp(min_sup)
	print(conditional)

	

def main():
	x=load_data()
	c={}
	for i in range(len(x)):
		for j in range(len(x[i])):
			if(x[i][j] not in c.keys()):
				c[x[i][j]]=1
			else:
				c[x[i][j]]+=1

	data2=[]
	for i in range(len(x)):
		data2_row=[]
		for j in range(len(x[i])):
			if(x[i][j] in c.keys()):
				data2_row.append([x[i][j],c[x[i][j]]])
		data2_row.sort(key=lambda x:x[1],reverse=True)
		data2_row_desc_order=[]
		for j in range(len(data2_row)):
			data2_row_desc_order.append(data2_row[j][0])
		data2.append(data2_row_desc_order)


	fp_tree(data2)

if __name__=='__main__':
	main()

