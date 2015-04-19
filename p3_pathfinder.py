
import math
from heapq import heappush, heappop


def find_path(source, destination, mesh):
	prev = {}
	queue = []
	path = []
	visited_nodes = []
	print(source)
	print(destination)
	for box in mesh['boxes']:
		if source[0] > box[0] and source[0] < box[1] and source[1] > box[2] and source[1] < box[3]:
	#		path.append(box)
			startBox = box
	queue = [startBox]
	while queue:
		print (queue)
		discBox = heappop(queue)
		print(discBox)
		if destination[0] > discBox[0] and destination[0] < discBox[1] and destination[1] > discBox [2] and destination[1] < discBox[3]: 
			print("break")
			break
		neighbors = mesh['adj'][discBox]
		print ('neighbors')
		print (neighbors)
		for next_box in neighbors:
			if prev.get(next_box) is None:
			#if next_box not in prev:
				print("1")
				prev[next_box] = discBox
				heappush(queue,(next_box))
	print(prev)
	node = discBox
	print(node)
	while node:
		path.append(node)
		node = prev[node]
	path.reverse()
	if path == []:
		print "No path possible!"
		pass
	#		print (startBox)
	#		print (mesh['adj'][box])
	#		visited_nodes.append(box)
	#for box1 in mesh['boxes']:
	#	if destination[0] >= box1[0] and destination[0] <= box1[1] and destination[1] >= box1[2] and destination[1] <= box1[3]:
	#		path.append(box)
	#		visited_nodes.append(box)
	#print (mesh['adj'][])
	#print (destination)
	return path, visited_nodes
