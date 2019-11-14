from svd import *
import re

words = []

# I want to get rid of all characters that aren't letters or spaces, so I use
# this regex to do it
regex = re.compile("[^a-z ]+")

# unfinished, I think, function to read matrices from a saved file, so I
# wouldn't need to sit through the 30 minutes or so each time I wanted to
# calculate it
def readmatrices(filepath):
    with open(filepath) as f:
        first_line = f.readline().split()
        m = int(first_line[0])
        n = int(first_line[1])
        data = []
        for i in range(m):
            data.append(f.readline().split())
        U = Matrix(m, n)
        U.data = data
        data = []
        f.readline()
        first_line = f.readline().split()
        m = int(first_line[0])
        n = int(first_line[1])
        data = []
        for i in range(m):
            data.append(f.readline().split())
        S = Matrix(m, n)
        S.data = data
        data = []
        f.readline()
        first_line = f.readline().split()
        m = int(first_line[0])
        n = int(first_line[1])
        data = []
        for i in range(m):
            data.append(f.readline().split())
        Vt = Matrix(m, n)
        Vt.data = data
        data = []
        return [U, S, Vt]

# right now just does the svd, but lsa also involves chopping off some
# dimensions to make calculations faster and I might implement that later
def lsa(freqmat, wordlist, k):
    U, sigma, Vt = svd(freqmat, wordlist)
    if k < U.n:
        for i in range(U.m):
            for j in range(U.n - k):
                U.data[i].pop()
        U.n = k
    if k < max(sigma.m, sigma.n):
        for i in range(max(sigma.m - k, 0)):
            sigma.data.pop()
        for row in sigma.data:
            for i in range(max(len(row) - k, 0)):
                row.pop()
        sigma.m = sigma.n = k
    if k < Vt.m:
        for i in range(Vt.m - k):
            Vt.data.pop()
        Vt.m = k
    return [U, sigma, Vt]

# helper function to calculate dot products of two vectors
def dot(vec1, vec2):
    assert len(vec1) == len(vec2),"Can only take dot product of vectors of same\
length"
    mag1 = 0
    mag2 = 0
    prod = 0
    for i in range(len(vec1)):
        mag1 += vec1[i] * vec1[i]
        mag2 += vec2[i] * vec2[i]
    mag1 = math.sqrt(mag1)
    mag2 = math.sqrt(mag2)
    for i in range(len(vec1)):
        vec1[i] /= mag1
        vec2[i] /= mag2
    for i in range(len(vec1)):
        prod += vec1[i] * vec2[i]
    return prod

# basically read the data file, split it up along paragraphs, and clean it; by
# the way almost all of this code is stolen from stackoverflow because I never
# managed to clean it properly myself
with open("data.txt") as f:
    remove = ".,<>/?;:'\"\\[{]}|=+-_)(*&^%$#@!~`1234567890"
    allowed = "abcdefghijklmnopqrstuvwxyz"
    data = f.read()
    paragraphs = data.split("\n\n")
    for paragraph in paragraphs:
        paragraph = " ".join(paragraph.lower().split())
        paragraph = regex.sub(" ", paragraph)
        paragraph = paragraph.split(" ")
        paragraph = list(filter(lambda x: x != '', paragraph))
        words.append(paragraph)

# set up a dictionary of words to figure out how many unique words there are and
# what their frequencies in each document are; btw "words" is a list of
# paragraphs not words, I'm sorry
freqtemp = {}
unique_words = 0
wordlist = []
for i in range(len(words)):
    paragraph = words[i]
    for word in paragraph:
        if word not in freqtemp:
            wordlist.append(word)
            unique_words += 1
            freqtemp[word] = [0] * len(words)
        freqtemp[word][i] += 1

# just prints the frequencies in a very pretty way
print("Frequencies: ")
for word in wordlist:
    print(word, end = ': ')
    print(' ' * (12 - len(word)), end = '')
    for doc in freqtemp[word]:
        print(doc, end = ' ')
    print()

# build the actual frequency matrix with proper weighting and everything
index = 0
freq = Matrix(unique_words, len(words))
for word in freqtemp:
    docfreq = 0
    for i in range(len(words)):
        if freq[[index,i]] > 0:
            docfreq += 1
        freq[[index,i]] = math.log(1 + freqtemp[word][i])
    for i in range(len(words)):
        freq[[index,i]] *= math.log(len(words) / (1 + docfreq)) / math.log(2)
    index += 1

# either calculate the matrices or read them from the file, uncomment if you
# want to calculate the matrices
#T, S, Dt = lsa(freq, wordlist, 2)
T, S, Dt = readmatrices('matrix.txt')

# write the matrices to a file for future reference and more legibility than
# printing it to the console
with open("matrix.txt", "w") as f:
    f.write("{} {}\n".format(T.m, T.n))
    f.write(str(T))
    f.write('\n')
    f.write("{} {}\n".format(S.m, S.n))
    f.write(str(S))
    f.write('\n')
    f.write("{} {}\n".format(Dt.m, Dt.n))
    f.write(str(Dt))
    f.write('\n')
    for i in range(len(wordlist)):
        word = wordlist[i]
        f.write(word)
        f.write(' ')
        for freq in freqtemp[word]:
            f.write(str(freq))
            f.write(' ')
        f.write('\n')

# read the document 'input.txt', figure out the query vector, translate the
# query vector to the document space, and figure out how close each document is,
# allowing us to evaluate whether the document is more math-y or linguistics-y

with open("input.txt", "r") as f:
    querytemp = {}
    for line in f:
        for char in line.split():
            if char in freqtemp:
                if char not in querytemp:
                    querytemp[char] = 0
                querytemp[char] += 1
    querymat = Matrix(1, len(freqtemp))
    for i, word in enumerate(freqtemp.keys()):
        if word in querytemp:
            querymat[[0, i]] = math.log(1 + querytemp[word])
        else:
            querymat[[0, i]] = 0.0

Sinv = S
for i in min(range())

querymat = querymat * T * S.inverse()
print(querymat)
