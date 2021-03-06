from math import sqrt, acos, degrees, pi
from decimal import Decimal, getcontext
 
getcontext().prec = 30
 
class Vector(object):
    def __init__(self, coordinates):
        try:
           if not coordinates:
                raise ValueError
           self.coordinates = tuple([Decimal(x) for x in coordinates])
           self.dimension = len(coordinates)
 
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
 
        except TypeError:
            raise TypeError('The coordinates must be an iterable')
 
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)
 
    def __eq__(self, vec):
        return self.coordinates == vec.coordinates
    
    def __iter__(self):
            return iter(self.coordinates)

    def __getitem__(self,index):
            return self.coordinates[index]
        
    def plus(self, vec):
        new_coordinates = [x + y for x,y in zip(self.coordinates, vec.coordinates)]
        return Vector(new_coordinates)
           
    def minus(self, vec):
        new_coordinates = [x - y for x,y in zip(self.coordinates, vec.coordinates)]
        return Vector(new_coordinates)
           
    def multiply(self, scalar):
        new_coordinates = [x * scalar for x in self.coordinates]               
        return Vector(new_coordinates)
 
    def magnitude(self):
        return Decimal(sqrt(sum([x *x  for x in self.coordinates])))
 
    def normalisation(self):
        try:
            normalisationFactor = Decimal("1.0") / self.magnitude()
            return Vector([x * normalisationFactor for x in self.coordinates])
       
        except ZeroDivisionError:
            raise Exception("Cannot normalise a vector with zero values")
   
    def dotProduct(self, vec):
        return sum(x * y for x,y in zip(self.coordinates, vec.coordinates))        
        
    def angle(self, vec, asDegrees = False):
        # handling 0 vector is still required
        cosTheta = self.dotProduct(vec) / (self.magnitude() * vec.magnitude())
        radians = acos(round(cosTheta, 4))       
        return radians if not asDegrees else degrees(radians)
       
    def is_parallel(self, vec):
        # if vec is 0 then is parallel
        if self.is_zero() or vec.is_zero():
            return True      
        return Decimal(self.angle(vec)) in [0, pi]
 
    def is_orthogonal(self, vec):
        # if vec is 0 then is parallel
        if self.is_zero() or vec.is_zero():
            return True     
        return round(self.dotProduct(vec),3) == 0
   
    def is_zero(self):
        return self.magnitude() == 0
   
    
    def project_onto(self, basisVector):
        """
        This is the parallel element of projected vector onto basis vector
        """
        normalisation = basisVector.Normalisation()
        weight = self.DotProduct(normalisation)
        return normalisation.Multiply(weight)
   
    def perpendicular_to_projectedVector(self, basisVector):
       """
       This is the perpendicular element of projected vector onto basis vector
       """
       projectedVector = self.project_onto(basisVector)
       return self.minus(projectedVector)
   
    def crossProduct(self, vec):
        x1 = self.coordinates[0]
        y1 = self.coordinates[1]
        z1 = self.coordinates[2]
        x2 = vec.coordinates[0]
        y2 = vec.coordinates[1]
        z2 = vec.coordinates[2]      
        return Vector([y1*z2 - y2*z1, -(x1*z2 - x2*z1), x1*y2 - x2*y1])
   
    def area_of_parallelogram(self, vec):
        """
        Area of parallelogram from the computed cross product of two vectors
        """
        crossProd = self.crossProduct(vec)
        return crossProd.magnitude()
   
    def area_of_triangle(self, vec):
        crossProd = self.crossProduct(vec)
        return crossProd.magnitude() / Decimal("2.0")