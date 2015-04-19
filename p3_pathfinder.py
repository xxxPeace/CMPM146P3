from math import sqrt
from heapq import heappush, heappop


def find_path(source, destination, mesh):
	prev = {}
	queue = []
	path = []
	detail_points = {}
	startBox = None

	print(source)
	print(destination)

	for box in mesh['boxes']:
		if source[0] >= box[0] and source[0] <= box[1] and source[1] >= box[2] and source[1] <= box[3]:
			startBox = box
	queue = [startBox]
	prev[startBox] = None

	while queue:
		discBox = heappop(queue)
		if destination[0] >= discBox[0] and destination[0] <= discBox[1] and destination[1] >= discBox [2] and destination[1] <= discBox[3]: 
			destination_box = discBox
			break
		neighbors = mesh['adj'][discBox]
		for next_box in neighbors:
			if next_box not in prev:
				prev[next_box] = discBox
				heappush(queue,(next_box))

	if destination[0] >= discBox[0] and destination[0] <= discBox[1] and destination[1] >= discBox [2] and destination[1] <= discBox[3]: 
		node = discBox
		while node != startBox:
			path.append(node)
			node = prev[node]
		path.reverse()
		prevPoint = source
		for box in path:
			smallDist = {}
			smallDist[(box[0],box[2])] = sqrt(prevPoint[0]*box[0] + prevPoint[1]*box[2])
			smallDist[(box[1],box[2])] = sqrt(prevPoint[0]*box[1] + prevPoint[1]*box[2])
			smallDist[(box[0],box[3])] = sqrt(prevPoint[0]*box[3] + prevPoint[1]*box[3])
			smallDist[(box[1],box[3])] = sqrt(prevPoint[0]*box[1] + prevPoint[1]*box[3])
			detail_points[box]= (prevPoint,(smallDist.keys()[0][0],smallDist.keys()[0][1]))
			if box != destination_box:
				prevPoint = ((smallDist.keys()[0][0],smallDist.keys()[0][1]))
		detail_points[destination_box]= (prevPoint,destination)
		return detail_points.values(), prev.keys()
	else:
		print ('no path')
		return detail_points.values(), prev.keys()
		
	#		print (startBox)
	#		print (mesh['adj'][box])
	#		visited_nodes.append(box)
	#for box1 in mesh['boxes']:
	#	if destination[0] >= box1[0] and destination[0] <= box1[1] and destination[1] >= box1[2] and destination[1] <= box1[3]:
	#		path.append(box)
	#		visited_nodes.append(box)
	#print (mesh['adj'][])
	#print (destination)

