import csv

# def conv_str_to_int(str_list) :
# 	for i in range(len(str_list)) :
# 		str_list[i] = int(str_list[i])
# 	return str_list

def read_dset() :
	dset = []
	with open('retail_dataset.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count != 0 :
				dset.append(row)
			line_count += 1
	return dset

def join_set(l, x) :
	# print(l)
	# l is a dict here and x is the number of items
	common_elements = x-1
	# To find c(x+1)
	c = {}
	dict_key = list(l.keys())
	for i in range(len(l.keys())) :
		for j in range(0, i) :
			# find the number common elements between l[i] and l[j]
			len_common = len(set(dict_key[i].split(',')[:common_elements]) & set(dict_key[j].split(',')[:common_elements]))
			if len_common == common_elements :
				# join
				# c[','.join(set(l[i].split(',')) | set(l[j].split(',')))] = 0
				new_element = list(set(dict_key[i].split(',')) & set(dict_key[j].split(',')))
				last_ele_i = dict_key[i].split(',')[-1]
				last_ele_j = dict_key[j].split(',')[-1]
				if last_ele_i > last_ele_j :
					new_element.append(last_ele_j)
					new_element.append(last_ele_i)
				else :
					new_element.append(last_ele_i)
					new_element.append(last_ele_j)
				c[','.join(new_element)] = 0
	return c

def apriori(dset, support) :
	step = 0
	c = {}
	for i in range(len(dset)) :
		for j in range(len(dset[i])) :
			try :
				c[dset[i][j]] += 1
			except :
				c[dset[i][j]] = 1
	while True :
		step += 1
		if step != 1 :
			for i in c.keys() :
				for j in range(len(dset)) :
					if set(i.split(',')) & set(dset[j]) == set(i.split(',')) :
						c[i] += 1

		# print(len(c))
		# Filter based on support value
		l = {}
		for i in c.keys() :
			if c[i] > support :
				# Add item to L
				l[i] = c[i]
			# else do not add to L
		print('c', step, ':', len(c))
		print('l', step, ':', len(l))
		print(l)
		# if step != 1 :
		# 	print(c)
		if len(l) == 0 :
			break
		# Join step
		c = join_set(l, step)
		if len(c) == 0 :
			break
		# print(c2)

apriori(read_dset(), 3000) 


			
