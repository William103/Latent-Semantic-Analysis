import math
import numpy as np

class Matrix:
    # constructor: initializes to a 0 mxn matrix
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.data = [[0.0] * n for _ in range(m)]
    
    # this allows for mat[[1,1]] = 5 for example
    def __setitem__(self, index, value):
        self.data[index[0]][index[1]] = float(value)

    # this allows you to get mat[[1,1]] for example
    def __getitem__(self, key):
        return self.data[key[0]][key[1]]

    # returns a string representation of the matrix
    def __str__(self):
        s = ''
        for row in self.data:
            for entry in row:
                s += str(entry) + " "
            s += "\n"
        return s

    # just does termwise addition, so mat1 + mat2 does termwise addition
    def __add__(self, other):
        assert self.m == other.m and self.n == other.n,"Dimension Mismatch"
        retval = Matrix(self.m, self.n)
        for i in range(self.m):
            for j in range(self.n):
                retval[[i,j]] = self[[i,j]] + other[[i,j]]
        return retval

    # termwise negation
    def __neg__(self):
        retval = Matrix(self.m, self.n)
        for i in range(self.m):
            for j in range(self.n):
                retval[[i,j]] = -self[[i,j]]
        return retval

    # termwise subtraction
    def __sub__(self, other):
        return self + -other

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    # implementation of matrix multiplication in a very brute-force way
    def __mul__(self, other):
        if isinstance(other, Matrix):
            assert self.n == other.m,"Dimension Mismatch"
            retval = Matrix(self.m, other.n)
            for i in range(retval.m):
                for j in range(retval.n):
                    val = 0
                    for r in range(self.n):
                        val += self[[i,r]] * other[[r,j]]
                    retval[[i,j]] = val
            return retval
        else:
            assert isinstance(other, float) or isinstance(other, int),"Scalar\
 Multiplication By Non Numeric Type"
            retval = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    retval[[i,j]] = self[[i,j]] * other
            return retval

    def __imul__(self, other):
        self = self * other
        return self

    # so matrix.transpose() is the transpose of a given matrix
    def transpose(self):
        retval = Matrix(self.n, self.m)
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                retval[[j,i]] = self[[i,j]]
        return retval

    # cheat and use numpy's determinant function
    def det(self):
        assert self.m == self.n,"Can only find det of square matrix"
        return np.linalg.det(self.data)

    # cheat and use numpy's eigenvalue/eigenvector function
    def eig(self):
        assert self.m == self.n,"Can only find eig of square matrix"
        return np.linalg.eig(self.data)

# a diagonal matrix is a special case of a matrix, whose inverse is easy to
# calculate, so might as well make a subclass for it
class Diagonal_Matrix(Matrix):
    def inverse(self):
        retval = self.transpose()
        for i in range(self.m):
            for j in range(self.n):
                if i == j:
                    retval[[j,i]] = 0 if self[[i,j]] == 0 else 1 / self[[i,j]]
                else:
                    assert retval[[j,i]] == 0,"Diagonal_Matrix non-diagonal"
        return retval


# same thing for a rotate matrix
class Rotate_Matrix(Matrix):
    def __init__(self, m, n):
        Matrix.__init__(self, m, n)
    def inverse(self):
        return self.transpose()
