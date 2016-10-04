from graph import *
from ps5 import *

mitmap = load_map('mit_map.txt')
testing = dfsValidPaths(mitmap,Node(1),Node(3))

if not testing:
    print 'Empty'
else:
    print testing[1][:2]
