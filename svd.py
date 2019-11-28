from matrix import *

# this function calculates the singular value decomposition of a matrix and
# returns (U, sigma, Vt) as a list
def svd(mat, wordlist):
    AAt = mat * mat.transpose()
    sigma = Diagonal_Matrix(min(mat.m, mat.n), min(mat.m, mat.n))
    U = Rotate_Matrix(mat.m, min(mat.m, mat.n))
    Vt = Rotate_Matrix(min(mat.m, mat.n), mat.n)

    # the next 13 lines are just a very messy way to get the
    # eigenvectors/eigenvalues and sort the eigenvalues and eigenvectors
    # accordingly, it just turns out that numpy stores the eigenvalues as a
    # numpy array of numpy arrays with the vectors in the columns, so I
    # processed them in the laziest way I could think of, i.e. turn everything
    # into a python list, turn the nested list into a matrix, and calculate its
    # transpose, giving me a list of vectors
    eigs = AAt.eig()
    eigvec = list(eigs[1])
    for i in range(len(eigvec)):
        eigvec[i] = list(eigvec[i])
    eigmat = Matrix(len(eigvec), len(eigvec[0]))
    eigmat.data = eigvec
    eigmat = eigmat.transpose()
    eigvec = eigmat.data
    eigval = list(eigs[0])
    eigs2 = list(zip(eigval, eigvec, wordlist))
    eigs2.sort()
    eigval =   [x for x,_,_ in eigs2]
    eigvec =   [x for _,x,_ in eigs2]
    wordlist = [x for _,_,x in eigs2]

    # get rid of all the 0 eigenvalues, since they don't really matter
    while eigval[0] == 0:
        eigval.remove(0)

    # set the diagonal of sigma to the square roots of the eigenvalues
    for i in range(min(sigma.n, sigma.m)):
        sigma[[i,i]] = math.sqrt(abs(eigval[-1-i]))
    
    # set the columns of U to the eigenvectors
    for i in range(U.n):
        for j in range(U.m):
            U[[j,i]] = eigvec[-1-i][j]

    # calculate Vt based on the other values we already have
    Vt = sigma.inverse() * U.inverse() * mat

    return [U, sigma, Vt]
