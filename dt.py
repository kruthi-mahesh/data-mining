import sys
from collections import Counter

c_label = ['No', 'Yes']

class Record:
	def __init__(self,Tid,att_dict,className):
		self.id = Tid
		self.cl = className
		self.att = att_dict

class Node:
	def __init__(self):
		self.isLeaf = True
		
class Attribute:
	def __init__(self,name,type,outcomes):
		self.name = name
		self.type = type
		self.outcomes = outcomes

		
def find_best_label(D):
		cl_list =  []
		for i in range(len(D)):
			cl_list.append(D[i].cl)
		ct = Counter(cl_list)
		return ct.most_common()[0][0]

def find_gini(D):
	if len(D) == 0:
		print('cant find gini')
		return -1
	cl_list =  []
	for i in range(len(D)):
		cl_list.append(D[i].cl)
	sum =  0.0
	for i in range(len(c_label)):
		temp = cl_list.count(c_label[i]) / float(len(D))
		sum += ( temp ** 2)
	return (1 -  sum)

def find_weighted_sum(D,D1,D2):
	ans = (len(D1)/float(len(D))) * find_gini(D1)
	ans += (len(D2)/float(len(D))) * find_gini(D2)
	return ans

def find_gini_binary(D,attr):
	att_name = attr.name
	D1 = []
	D2 = []
	for d  in D:
		if (d.att[att_name]) in attr.outcomes[0]:
			D1.append(d)
		else:
			D2.append(d)
	gini = find_weighted_sum(D,D1,D2)
	return gini,D1,D2

def find_splitvalue(D,attr):
	hashmap = {}
	keylist = []
	for d in D:
		key = d.att[attr.name]
		keylist.append(key)
		val = d.cl
		hashmap[key] = val
	listof_values = list(hashmap.values())
	cl1 = listof_values.count(c_label[0])
	cl2 = listof_values.count(c_label[1])
	keylist.sort()
	#find split pos array
	split_pos = []
	temp = keylist[0] - 5
	split_pos.append(temp)
	length = len(keylist)
	for i in range(length-1):
		temp = int((keylist[i] + keylist[i+1])/float(2))
		split_pos.append(temp)
	temp = int(keylist[length-1] + 10)
	split_pos.append(temp)
	#end of find split pos array
	min_gini = sys.maxsize
	n = len(D)
	gini = 1- (cl1/float(n)) ** 2 - (cl2/float(n)) ** 2
	if gini < min_gini:
		min_gini = gini
		return_split_value = split_pos[0]
	#initializing some variables required to find gini
	len_left = 0
	len_right = 10
	len_left_class1 = 0
	len_left_class2 = 0
	len_right_class1 = cl1
	len_right_class2 = cl2
	for i in range(len(keylist)-1):
		len_left += 1
		len_right -= 1
		if hashmap[keylist[i]] == c_label[0]:
			len_left_class1 += 1
			len_right_class1 -= 1
		else:
			len_left_class2 += 1
			len_right_class2 -= 1
		gini = len_left/float(n) * (1 - (len_left_class1/float(len_left)) ** 2 - (len_left_class2/float(len_left)) ** 2)
		gini += len_right/float(n) * (1 - (len_right_class1/float(len_right)) ** 2 - (len_right_class2/float(len_right)) ** 2)

		if gini < min_gini:
			min_gini = gini
			return_split_value = split_pos[i+1]
	return min_gini,return_split_value

def  find_gini_cont(D,att):
	att_name = att.name
	D1 = []
	D2 = []
	gini,split = find_splitvalue(D,att)
	#partition D into D1(if <=splitval) and D2(if >splitvalue)
	for d in D:
		if (d.att[att_name] <= split):
			D1.append(d)
		else:
			D2.append(d)
	return gini,split,D1,D2


def find_best_split(D,att_list):
	if len(att_list)==0:
		return
	max = - sys.maxsize
	return_D1 = []
	return_D2 = []
	left_edge = []
	right_edge =[]
	impurity_parent = find_gini(D)
	for att in att_list : 
		if att.type == 'binary':
			gini,D1,D2 = find_gini_binary(D,att)
			diff = impurity_parent - gini
			if diff>max:
				max  = diff
				returnAttribute = att
				left_edge[:] = []
				right_edge[:] = []
				left_edge.append(att.outcomes[0])
				right_edge.append(att.outcomes[1])
				return_D1 = D1
				return_D2 = D2

		elif att.type == 'threeWay':
			outcomes = att.outcomes
			ct = 3
			while (ct):
				newOutcomes = []
				if ct == 3:
					l1 = [outcomes[0],outcomes[1]]
				elif ct == 2:
					l1 = [outcomes[0],outcomes[2]]
				else:
					l1 = [outcomes[1],outcomes[2]]
				newOutcomes.append(l1)
				if ct == 3:
					l2 = [outcomes[2]]
				elif ct == 2:
					l2 = [outcomes[1]]
				else:
					l2 = [outcomes[0]]
				newOutcomes.append(l2)
				newAttribute = Attribute(att.name,att.type,newOutcomes)
				gini,D1,D2 = find_gini_binary(D,newAttribute)
				diff = impurity_parent - gini
				if diff>max:
					max = diff
					returnAttribute = newAttribute
					left_edge[:] = []
					right_edge[:] = []
					left_edge.append(newAttribute.outcomes[0])
					right_edge.append(newAttribute.outcomes[1])
					return_D1 = D1
					return_D2 = D2
				ct -= 1

		elif att.type == 'continuous':
			gini,split,D1,D2 = find_gini_cont(D,att)
			split = int(split)
			diff = impurity_parent - gini
			if diff > max:
				max = diff
				returnAttribute = att 
				left_edge[:] = []
				right_edge[:] = []
				left_edge.append(['<=',split])
				right_edge.append(['>',split])
				return_D1 = D1
				return_D2 = D2
		else:
			print('Error')
			return


	return returnAttribute,left_edge,right_edge,return_D1,return_D2



def stopping_cond(D,att_list):
	if len(att_list) == 0:
		return True
	cl_list = []
	for i in range(len(D)):
		cl_list.append(D[i].cl)
	uniq = list(set(cl_list))
	if(len(uniq) == 1): #all rec belong to same class
		return True
	#check for identical attribute values(except cl)
	res = True
	for i in range(1,len(D)):
		res = res and D[0].att == D[i].att
	return res



def TreeGrowth  (E,F,parent_label):
	if(len(E) == 0):
		newNode = Node()
		newNode.label  = parent_label
		return newNode
	if stopping_cond(E,F) == True :
		leaf = Node()
		leaf.label = find_best_label(E)
		return leaf
	else:
		root = Node()
		root.isLeaf = False
		root.label = find_best_label(E)
		attr,left_edge,right_edge,D1,D2 = find_best_split(E,F)
		root.test_cond = attr.name
		root.leftEdge = left_edge
		root.rightEdge = right_edge
		for at in F:
			if at.name == attr.name:
				F.remove(at)
		parent_label = find_best_label(E)
		
		root.leftChild = TreeGrowth(D1,F,parent_label)
		root.rightChild = TreeGrowth(D2,F,parent_label)
		return root

def display(root):
	if root == None:
		return
	if root.isLeaf == True:
		print('Defaulted = ',root.label)
		return
	print(root.test_cond)
	print('Left Edge is ', root.leftEdge)
	print('Right Edge is',root.rightEdge)
	print('Left Child of ',root.test_cond,'is')
	display(root.leftChild)
	print('Right Child of ',root.test_cond,'is')
	display(root.rightChild)

D = []
d1  =  {'Home_Owner':'Yes' ,'Marital_Status': 'Single', 'Annual_Income':125}
D.append(Record(1,d1,'No'))
d2  =  {'Home_Owner':'No' ,'Marital_Status': 'Married', 'Annual_Income':100}
D.append(Record(2,d2,'No'))
d3  =  {'Home_Owner':'No' ,'Marital_Status': 'Single', 'Annual_Income':70}
D.append(Record(3,d3,'No'))
d4  =  {'Home_Owner':'Yes' ,'Marital_Status': 'Married', 'Annual_Income':120}
D.append(Record(4,d4,'No'))
d5  =  {'Home_Owner':'No' ,'Marital_Status': 'Divorced', 'Annual_Income':95}
D.append(Record(5,d5,'Yes'))
d6  =  {'Home_Owner':'No' ,'Marital_Status': 'Married', 'Annual_Income':60}
D.append(Record(6,d6,'No'))
d7  =  {'Home_Owner':'Yes' ,'Marital_Status': 'Divorced', 'Annual_Income':220}
D.append(Record(7,d7,'No'))
d8  =  {'Home_Owner':'No' ,'Marital_Status': 'Single', 'Annual_Income':85}
D.append(Record(8,d8,'Yes'))
d9  =  {'Home_Owner':'No' ,'Marital_Status': 'Married', 'Annual_Income':75}
D.append(Record(9,d9,'No'))
d10  =  {'Home_Owner':'No' ,'Marital_Status': 'Single', 'Annual_Income':90}
D.append(Record(10,d10,'Yes'))
attr_list = []
attr_list.append(Attribute('Home_Owner','binary',[['Yes'],['No']]))
attr_list.append(Attribute('Marital_Status','threeWay',['Single','Married','Divorced']))
attr_list.append(Attribute('Annual_Income','continuous',['<=','>']))



parent_label = find_best_label(D)
root =None
root = TreeGrowth(D,attr_list,parent_label)
display(root)

