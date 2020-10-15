

# Python3 program to Print all possible paths from 
# top left to bottom right of a mXn matrix 
def findPaths(M, n, allPaths, directions, aux):
	path = [0 for d in range((n*2)-1)] 
	findPathsUtil(M, n, 0, 0, path, 0, allPaths, directions, aux)
	
def findPathsUtil(M, n,i,j,path,indx, allPaths, directions, aux): 
	# if we reach the bottom of M, we can only move right 
	if i==n-1: 
		for k in range(j,n): 
			aux.append(M[i][k])
			if(len(aux) != len(path)):
				print(*aux, sep=' -> ', end=' -> down\n')
				allPaths.append(aux[:])
				directions.append(' -> down')
			path[indx+k-j] = M[i][k] 

		# if we hit this block, it means one path is completed. 
		# Add it to paths list and print 
		print(*path, sep=' -> ', end=' -> down\n')
		allPaths.append(path[:])
		directions.append(' -> down')
		return
        
	# if we reach to the right most corner, we can only move down 
	if j == n-1:
		aux = []
		for k in range(0, indx):
			aux.append(path[k])
		for k in range(i, n):
			aux.append(M[k][j])
			if(len(aux) != len(path)):
				print(*aux, sep=' -> ', end=' -> right\n')
				allPaths.append(aux[:])
				directions.append(' -> right')
			path[indx+k-i] = M[k][j] 

		# if we hit this block, it means one path is completed. 
		# Add it to paths list and print 
		print(*path, sep=' -> ', end=' -> right\n')
		allPaths.append(path[:])
		directions.append(' -> right')
		return
	
	# add current element to the path list 
	path[indx] = M[i][j]
	aux = []
	for k in range(0, indx+1):
		aux.append(path[k])
	
	# move down in y direction and call findPathsUtil recursively 
	findPathsUtil(M, n, i+1, j, path, indx+1, allPaths, directions, aux)
	
	# move down in y direction and call findPathsUtil recursively 
	findPathsUtil(M, n, i, j+1, path, indx+1, allPaths, directions, aux)

def maxSumPath(paths):
	max = 0
	result = []
	index = 0
	for i, path in enumerate(paths):
		pathAux = path
		while (len(pathAux) != 0):
			soma = sum(path)
			if(max < soma):
				result = pathAux[:]
				index = i
				max = soma
			pathAux.pop(0)
	print(*result, sep=' -> ', end=directions[index])

if __name__ == '__main__': 
	allPaths = []
	directions = []
	aux = []
	M = [[3, 1, -4, 1], 
			[5,-1, 9, 2]
            ,[6, 5, -3, -5]
			,[-8, -9, -7, -9]
			] 
	findPaths(M, 4, allPaths, directions, aux)
	print("")
	#print(allPaths, " - ", len(allPaths), " elements")
	print("")
	maxSumPath(allPaths)
