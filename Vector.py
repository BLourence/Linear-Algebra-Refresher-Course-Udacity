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
   
    def Plus(self, vec):
        new_coordinates = [x + y for x,y in zip(self.coordinates, vec.coordinates)]
        return Vector(new_coordinates)
           
    def Minus(self, vec):
        new_coordinates = [x - y for x,y in zip(self.coordinates, vec.coordinates)]
        return Vector(new_coordinates)
           
    def Multiply(self, scalar):
        new_coordinates = [x * scalar for x in self.coordinates]               
        return Vector(new_coordinates)
 
    def Magnitude(self):
        return Decimal(sqrt(sum([x *x  for x in self.coordinates])))
 
    def Normalisation(self):
        try:
            normalisationFactor = Decimal("1.0") / self.Magnitude()
            return Vector([x * normalisationFactor for x in self.coordinates])
       
        except ZeroDivisionError:
            raise Exception("Cannot normalise a vector with zero values")
   
    def DotProduct(self, vec):
        return sum(x * y for x,y in zip(self.coordinates, vec.coordinates))        
        
    def Angle(self, vec, asDegrees = False):
        # handling 0 vector is still required
        cosTheta = self.DotProduct(vec) / (self.Magnitude() * vec.Magnitude())
        radians = acos(round(cosTheta, 4))       
        return radians if not asDegrees else degrees(radians)
       
    def IsParallel(self, vec):
        # if vec is 0 then is parallel
        if self.IsZero() or vec.IsZero():
            return True      
        return Decimal(self.Angle(vec)) in [0, pi]
 
    def IsOrthogonal(self, vec):
        # if vec is 0 then is parallel
        if self.IsZero() or vec.IsZero():
            return True     
        return round(self.DotProduct(vec),3) == 0
   
    def IsZero(self):
        return self.Magnitude() == 0
   
    
    def ProjectOnto(self, basisVector):
        """
        This is the parallel element of projected vector onto basis vector
        """
        normalisation = basisVector.Normalisation()
        weight = self.DotProduct(normalisation)
        return normalisation.Multiply(weight)
   
    def PerpendicularToProjectedVector(self, basisVector):
       """
        This is the perpendicular element of projected vector onto basis vector
        """
        projectedVector = self.ProjectOnto(basisVector)
        return self.Minus(projectedVector)
   
    def CrossProduct(self, vec):
        x1 = self.coordinates[0]
        y1 = self.coordinates[1]
        z1 = self.coordinates[2]
        x2 = vec.coordinates[0]
        y2 = vec.coordinates[1]
        z2 = vec.coordinates[2]      
        return Vector([y1*z2 - y2*z1, -(x1*z2 - x2*z1), x1*y2 - x2*y1])
   
    def AreaOfParallelogram(self, vec):
        """
        Area of parallelogram from the computed cross product of two vectors
        """
        crossProd = self.CrossProduct(vec)
        return crossProd.Magnitude()
   
    def AreaOfTriangle(self, vec):
        crossProd = self.CrossProduct(vec)
        return crossProd.Magnitude() / Decimal("2.0")