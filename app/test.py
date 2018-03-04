width = 10
height = 10
list = []
for i in range(0, height):
	innerList = []
	for k in range(0, width):
		innerList.append(0)
	list.append(innerList)

print list
