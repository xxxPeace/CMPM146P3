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
	bdist = {}
	bprev = {}
	detail_points = {}
	queue = []
	bqueue = []
	path = []	
	startBox = None
	endBox = None
	new_cost = 0.0
	bnew_cost = 0.0
	fristBreak = False
	secondBreak = False

	for box in mesh['boxes']:
		if source[0] >= box[0] and source[0] <= box[1] and source[1] >= box[2] and source[1] <= box[3]:
			startBox = box
			dist[startBox] = 0.0		
		if destination[0] >= box[0] and destination[0] <= box[1] and destination[1] >= box[2] and destination[1] <= box[3]: 
			endBox = box
			bdist[endBox] = 0.0
	if (startBox == None or endBox == None):
		print('no such source box or destination box')
		return [],[]

	queue = [(dist[startBox],startBox,source)]
	bqueue = [(bdist[endBox],endBox,destination)]
	
	prev[startBox] = None
	bprev[endBox] = None

	while queue or bqueue:
		discBox = heappop(queue)
		bdiscBox = heappop(bqueue)

		if discBox[1] in bprev.values():
			fristBreak = True
			break
		if bdiscBox[1] in prev.values():
			secondBreak = True
			break
		
		if discBox[0] <= bdiscBox[0]:
			neighbors = mesh['adj'][discBox[1]]
			prevD = (discBox[2][0], discBox[2][1])
			for next_box in neighbors:
				coypXY = close_box(prevD, next_box)
				cost = sqrt((prevD[0]-coypXY[0])*(prevD[0]-coypXY[0]) + (prevD[1] - coypXY[1])*(prevD[1] - coypXY[1]))
				new_cost = dist[discBox[1]] + cost
				if next_box not in prev or new_cost < dist[next_box]:
					dist[next_box] = new_cost
					priority = new_cost  + heuristic(destination, coypXY)
					prev[next_box] = discBox[1]
					heappush(queue,(priority, next_box, coypXY))
			heappush(bqueue, bdiscBox)
		if discBox[0] > bdiscBox[0]:
			bneighbors = mesh['adj'][bdiscBox[1]]
			bprevD = (bdiscBox[2][0], bdiscBox[2][1])
			for bnext_box in bneighbors:
				bcoypXY = close_box(bprevD, bnext_box)
				bcost = sqrt((bprevD[0]-bcoypXY[0])*(bprevD[0]-bcoypXY[0]) + (bprevD[1] - bcoypXY[1])*(bprevD[1] - bcoypXY[1]))
				bnew_cost = bdist[bdiscBox[1]] + bcost
				if bnext_box not in bprev or bnew_cost < bdist[bnext_box]:
					bdist[bnext_box] = bnew_cost
					bpriority = bnew_cost  + heuristic(source, bcoypXY)
					bprev[bnext_box] = bdiscBox[1]
					heappush(bqueue,(bpriority, bnext_box, bcoypXY))
			heappush(queue, discBox)

	if endBox == startBox:
		detail_points[endBox] = (source,destination)
		return detail_points.values(), prev.keys() + bprev.keys()
	if fristBreak:	
		node = discBox[1]
		bnode = bprev[discBox[1]]
	if secondBreak:
		node = bdiscBox[1]
		bnode = bprev[bdiscBox[1]]
	while node:
		path.append(node)
		node = prev[node]
	path.reverse()
	while bnode:
		path.append(bnode)
		bnode = bprev[bnode]

	prevPoint = source
	for box in path:
		lineXY = close_box(prevPoint, box)
		detail_points[box] = (prevPoint,lineXY)

		if box != endBox:
			prevPoint = (lineXY)
	detail_points[endBox] = (prevPoint,destination)
	return detail_points.values(), prev.keys() + bprev.keys()





