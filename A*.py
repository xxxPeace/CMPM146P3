from math import sqrt
from heapq import heappush, heappop

def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def close_box(src,box):
	if (src[0] >= box[0]):
		if (box[1] >= src[0]):
			closeX = src[0]
		else:
			closeX = box[1]
	else:
		if (box[1] >= box[0]):
			closeX = box[0]
		else:
			closeX = box[1]

	if (src[1] >= box[2]):
		if (box[3] >= src[1]):
			closeY = src[1]
		else:
			closeY = box[3]
	else: 
		if (box[3] >= box[2]):
			closeY = box[2]
		else:
			closeY = box[3]
			
	return (closeX, closeY)

def find_path(source, destination, mesh):
	dist = {}
	prev = {}
	queue = []
	path = []
	detail_points = {}
	startBox = None
	new_cost = 0.0

	for box in mesh['boxes']:
		if source[0] >= box[0] and source[0] <= box[1] and source[1] >= box[2] and source[1] <= box[3]:
			startBox = box
			dist[startBox] = 0.0
	if (startBox == None):
		print('no such source box')
		return [],[]
	queue = [(dist[startBox],startBox,source)]
	prev[startBox] = None

	while queue:
		discBox = heappop(queue)
		if destination[0] >= discBox[1][0] and destination[0] <= discBox[1][1] and destination[1] >= discBox[1][2] and destination[1] <= discBox[1][3]: 
			destination_box = discBox[1]
			break
		neighbors = mesh['adj'][discBox[1]]
		prevD = (discBox[2][0],discBox[2][1])

		for next_box in neighbors:
			#method 1
			#lessDist = {}
			#lessDist[sqrt(prevD[0]*next_box[0] + prevD[1]*next_box[2])] = (next_box[0],next_box[2])
			#lessDist[sqrt(prevD[0]*next_box[1] + prevD[1]*next_box[2])] = (next_box[1],next_box[2])
			#lessDist[sqrt(prevD[0]*next_box[2] + prevD[1]*next_box[3])] = (next_box[0],next_box[3])
			#lessDist[sqrt(prevD[0]*next_box[1] + prevD[1]*next_box[3])] = (next_box[1],next_box[3])
			#tempKey = sorted(lessDist.keys())
			#coypXY = lessDist[tempKey[0]]
			#new_cost = dist[discBox[1]] + sorted(lessDist.keys())[0]

			#method 2
			#midPiontX = (next_box[1] + next_box[0])/2
			#midPiontY = (next_box[3] + next_box[2])/2
			#coypXY = (midPiontX, midPiontY)
			#cost = sqrt(prevD[0]*midPiontX + prevD[1]*midPiontY)
			#new_cost = dist[discBox[1]] + cost

			#method 3
			coypXY = close_box(prevD, next_box)
			cost = sqrt((prevD[0]-coypXY[0])*(prevD[0]-coypXY[0]) + (prevD[1] - coypXY[1])*(prevD[1] - coypXY[1]))

			new_cost = dist[discBox[1]] + cost
			if next_box not in prev or new_cost < dist[next_box]:
				dist[next_box] = new_cost
				priority = new_cost  + heuristic(destination, coypXY)
				prev[next_box] = discBox[1]
				heappush(queue,(priority, next_box, coypXY))


	if destination[0] >= discBox[1][0] and destination[0] <= discBox[1][1] and destination[1] >= discBox[1][2] and destination[1] <= discBox[1][3]: 
		node = discBox[1]
		while node != startBox:
			path.append(node)
			node = prev[node]
		path.reverse()
		prevPoint = source
		for box in path:
			#method 1
			#smallDist = {}
			#smallDist[sqrt(prevPoint[0]*box[0] + prevPoint[1]*box[2])] = (box[0],box[2])
			#smallDist[sqrt(prevPoint[0]*box[1] + prevPoint[1]*box[2])] = (box[1],box[2])
			#smallDist[sqrt(prevPoint[0]*box[3] + prevPoint[1]*box[3])] = (box[0],box[3])
			#smallDist[sqrt(prevPoint[0]*box[1] + prevPoint[1]*box[3])] = (box[1],box[3])
			#sortKey = sorted(smallDist.keys())
			#copyKey = smallDist[sortKey[0]]
			#detail_points[box] = (prevPoint, copyKey)

			#method 2
			#midX = (box[1] + box[0])/2
			#midY = (box[3] + box[2])/2
			#midXY = (midX,midY)
			#detail_points[box] = (prevPoint,midXY)

			#method 3
			lineXY = close_box(prevPoint, box)
			detail_points[box] = (prevPoint,lineXY)

			if box != destination_box:
				#prevPoint = (copyKey)
				#prevPoint =(midXY)
				prevPoint = (lineXY)
		detail_points[destination_box] = (prevPoint,destination)
		return detail_points.values(), prev.keys()
	else:
		print ('no path')
		return detail_points.values(), prev.keys()
