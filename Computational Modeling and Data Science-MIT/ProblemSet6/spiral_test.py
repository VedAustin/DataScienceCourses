import numpy as np

def top(arr):
	# Read the top layer 
    a = [elem for elem in arr[0]]
    # Delete the top layer from the array
    arr = np.delete(arr,(0), axis=0)
    return a,arr

def sideR(arr):
	# Read the side layer (R)
    x,y=arr.shape # get the dimensions
    a = [elem[y-1] for elem in arr]
    # Delete the side layer (R) from the array
    arr = np.delete(arr,y-1,axis=1)
    return a,arr

def bottom(arr):
	# Read the bottom layer
    x,y = arr.shape # get the dimensions
    a = arr[x-1]
    reverse_a = a[::-1] # reverse the array
    # Delete the bottom layer from the array
    arr = np.delete(arr,x-1,axis=0)
    return reverse_a.tolist(),arr

def sideL(arr):
	# Read the side layer (L)
    a = [elem[0] for elem in arr]
    # Delete the side layer [L] from the array
    arr = np.delete(arr,0,axis=1)
    reverse_a = a[::-1]
    return reverse_a,arr


#square matrix
n = 5
# Build a square 1d array
A = np.array(range(n**2))
# Convert A into a 2d array, B
B = A.reshape(n,-1)
print B

spiral_form = []
while (B.size):
    temp,B = top(B)
    #print temp
    spiral_form += temp
    if B.size:
        temp,B = sideR(B)
        #print temp
        spiral_form += temp
    else:
        break
    if B.size:
        temp,B = bottom(B)
        #print temp
        spiral_form += temp
    else:
        break
    if B.size:
        temp,B = sideL(B)
        #print temp
        spiral_form += temp
    else:
        break
print spiral_form