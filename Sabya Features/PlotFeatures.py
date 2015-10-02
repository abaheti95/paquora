#author : Rahul
import time
import numpy as np
import matplotlib.pyplot as plt

""" an object of this class is a Plot that you can use for your feature analysis """
class Plotfeatures(object):
	"""
		data is assumed to be a list of tuples such that (a, b, c) is a tuple in it then a is the essay id and b is the value of the feature c is the class in which the person falls
		choose label to be the feature that you are plotting
	"""
	def __init__(self, data = [], label = "none"):
		self.data = data
		self.label = label
		self.figure = plt.figure()
	""" this function plots the data for the graph 
		size is the size of each point you want in the plot
	"""
	def plot_data(self, size = 100):
		self.data.sort(key=lambda tup: tup[1])  # sorts in place
		data_list = map(list, zip(*self.data))
		class1 = dict()
		class2 = dict()
		class1['x'] = list()
		class1['y'] = list() 
		class2['x'] = list()
		class2['y'] = list()
		
		for i in range(0, len(data_list[2])):
			if data_list[2][i] == 1:
				class1['x'].append(i)
				class1['y'].append(data_list[1][i])
			else:
				class2['x'].append(i)
				class2['y'].append(data_list[1][i])

		self.figure.canvas.set_window_title(self.label)
		plt.scatter(class1['x'], class1['y'], s=size, c= ['Red']*len(class1['x']), alpha=0.5, marker= 'v')
		plt.scatter(class2['x'], class2['y'], s=size, c= ['Blue']*len(class2['x']), alpha=0.5, marker= 'o')
		plt.xlabel("Essay")
		plt.ylabel(self.label + " value")
	"""
		the following function shows the user a the figure
	"""
	def show_fig(self):
		self.figure.show()

	"""
		the following function saves figure
	"""
	def save_fig(self, path= "plots/"):
		self.figure.savefig(path+self.label+".png")

""" below is an example code to demonstrate the above class """
# a = [(1,2,0), (2,3,1)]
# p1 = Plotfeatures(a, "1")
# p1.plot_data(10)
# p1.show_fig()
# p1.save_fig()

# b = [(7, 8, 1), (4, 10, 0), (6, 11, 1)]
# p2 = Plotfeatures(b, "2")
# p2.plot_data()
# p2.show_fig()
# p2.save_fig()
