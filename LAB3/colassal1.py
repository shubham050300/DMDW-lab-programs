import csv

def load_data() :
    dset = []
    with open('Test2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0 :
                dset.append(row)
            line_count += 1
    return dset

def preprocessing(x,min_support,min_cardinality):

    for i in range(2):
        x=prunecol(min_support,x)   
        # print(x)  
        x=prunerow(min_cardinality,x)
        # print(x)
    print("Data after preprocessing:")
    for s in x:
        print(*s)
    print("Number of rows:",len(x))
    print("Number of columns:", len(x[0]))
    print()
    return x

def prunerow(mincar,x):
    i=0
    while i < (len(x)):
        car=0
        j=0
        while j < (len(x[0])-1):
            car+=(x[i][j])
            j+=1
        if car<mincar:
            x.pop(i)
        i+=1
    return x

def prunecol(minsup,x):
    j=0
    while j < (len(x[0])):
        sup=0
        i=0
        while i < (len(x)):
            sup+=(x[i][j])
            i+=1
        if sup<minsup:
            for k in x:
                del k[j]
        j+=1
    return x

def countSetBits(n): 
    count = 0
    while (n): 
        count += n & 1
        n >>= 1
    return count 

tt=0

def self_join(x,item_sets,i):
    min_cardinality=3

    global tt
    new_itemsets=[]
    for a in range(i+1,len(item_sets)):
        proposed_itemset = item_sets[i].copy()
        proposed_itemset.insert(-1,item_sets[a][-2])
        proposed_itemset[-1] = item_sets[i][-1] & x[item_sets[a][-2]][-1]

        if(countSetBits(proposed_itemset[-1])>=min_cardinality):
            new_itemsets.append(proposed_itemset)
            # print("#",new_itemsets)
            print("{:<20} {: <20}".format(bin(proposed_itemset[-1]), str(proposed_itemset[:-1])))

    # print("##",i,new_itemsets)
    if(len(new_itemsets)==0 and len(item_sets[0])>min_cardinality):
        tt+=1
    return new_itemsets


def colossal(x,x2):

    for i in range(len(x2)):
        colossal(x,self_join(x,x2,i))

    
def list_to_decimal(number):
    n = int(''.join(str(i) for i in number))
    n=str(n)
    return int(n,2)

def main():

    min_support=2
    min_cardinality=2
    x=load_data()
    print("Original data:")
    for s in x:
        print(*s)
    print("Number of rows:",len(x))
    print("Number of columns:", len(x[0]))
    print()

    for i in range(len(x)):
        for j in range(len(x[0])):
            x[i][j]=int(x[i][j])

    x = preprocessing(x,min_support,min_cardinality)

    dataset = []

    dash = '-' * 40
    print(dash)
    print("{:<20} {: <20}".format("binarized", "items(row no.)"))
    print(dash)

    for i in range(len(x)):
        dataset.append([i,list_to_decimal(x[i])])
        print("{:<20} {: <20}".format( bin(dataset[i][-1]), str(dataset[i][:-1])))

    colossal(dataset,dataset)
    
    print("Total number of itemsets are:",tt)



if __name__=='__main__':
    main()
