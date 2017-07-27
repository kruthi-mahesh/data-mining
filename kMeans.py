from __future__ import division
import sys
import random
from random import randint
import math

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def display(self):
		print 'x:'+ str(self.x) + '\ty:'+ str(self.y)

	def find_min_i(self,mean):
		min_dis = sys.float_info.max
		for i in range(len(mean)):
			dis = find_dis(self,mean[i])
			if dis < min_dis:
				min_dis = dis
				min_i = i
		return min_i



def create(n):
	D = []
	for i in range(n):
		D.append(Point(randint(0,r),randint(0,r)))
	return D

def print_(D):
	for pt in D:
		pt.display() 

def find_dis(p1,p2):
	return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y) ** 2)

def find_mean(cl):
	if len(cl)==0:
		return -1,-1
	sum_x = 0
	sum_y = 0
	for pt in cl:
		sum_x += pt.x
		sum_y += pt.y
	x = sum_x/len(cl)
	y = sum_y/len(cl)
	return x,y

def isEqual(new,old):
	for i in range(k):
		if new[i].x != old[i].x or new[i].y != old[i].y:
			return False
	return True

def clustering(D,k):
	
	mean = []
	for i in range(k):
		mean.append(Point(randint(0,r),randint(0,r)))
	while True:
		cluster = []
		for i in range(k):
			cluster.append([])
		old = list(mean)
		for pt in D:			
			cluster[pt.find_min_i(mean)].append(pt)
		mean = []
		for i in range(k):
			x,y = find_mean(cluster[i])
			mean.append(Point(x,y))		
		if isEqual(mean,old):
			return mean
	






size = input("Enter number of points\n")
r = input("Enter max range of each point\n")
k = input("Enter number of clusters\n")
D = create(size)
#print 'Created Points are'
#print_(D)
mean = clustering(D,k)

print 'Means of ' + str(k) + ' clusters are'
print_(mean)
#print '(-1,-1) indicates no points for that cluster'






