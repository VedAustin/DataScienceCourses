import pylab
import random
print "Hello World"
pylab.plot(range(100),[random.random() for i in range(100)])
pylab.show()