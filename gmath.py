import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
	normalize(view)
	normalize(light[0])
	normalize(normal)
	a = calculate_ambient(ambient,areflect)
	b = calculate_diffuse(light,dreflect,normal)
	c = calculate_specular(light,sreflect,view,normal)
	color = [a[0]+b[0]+c[0],
			a[1]+b[1]+c[1],
			a[2]+b[2]+c[2]]
	return limit_color(color)

def calculate_ambient(alight, areflect):
	return [alight[0]*areflect[0],
			alight[1]*areflect[1],
			alight[2]*areflect[2]]

def calculate_diffuse(light, dreflect, normal):
	dir = dot_product(light[0],normal)
	return [dreflect[0]*dir*light[1][0],
			dreflect[1]*dir*light[1][1],
			dreflect[2]*dir*light[1][2]]

def calculate_specular(light, sreflect, view, normal):
	r = [2*dot_product(light[0],normal)*normal[0] - light[0][0],
		2*dot_product(light[0],normal)*normal[1] - light[0][1],
		2*dot_product(light[0],normal)*normal[2] - light[0][2]]
	cosa = dot_product(view,r)
	cosa = -1*(cosa**SPECULAR_EXP) if cosa<0 else cosa**SPECULAR_EXP
	return [sreflect[0]*light[1][0]*cosa,
			sreflect[1]*light[1][1]*cosa,
			sreflect[2]*light[1][2]*cosa]

def limit_color(color):
	for i in range(3):
		if color[i] > 255:
			color[i] = 255
		elif color[i] < 0:
			color[i] = 0
		color[i] = int(color[i])
	return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
	magnitude = math.sqrt( vector[0] * vector[0] +
						   vector[1] * vector[1] +
						   vector[2] * vector[2])
	for i in range(3):
		vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
	return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

	A = [0, 0, 0]
	B = [0, 0, 0]
	N = [0, 0, 0]

	A[0] = polygons[i+1][0] - polygons[i][0]
	A[1] = polygons[i+1][1] - polygons[i][1]
	A[2] = polygons[i+1][2] - polygons[i][2]

	B[0] = polygons[i+2][0] - polygons[i][0]
	B[1] = polygons[i+2][1] - polygons[i][1]
	B[2] = polygons[i+2][2] - polygons[i][2]

	N[0] = A[1] * B[2] - A[2] * B[1]
	N[1] = A[2] * B[0] - A[0] * B[2]
	N[2] = A[0] * B[1] - A[1] * B[0]

	return N
