import numpy
import elasticdeform

X = numpy.zeros((2000, 3000))
X[::10, ::10] = 1

# apply deformation with a random 3 x 3 grid
X_deformed = elasticdeform.deform_random_grid(X, sigma=25, points=3)
