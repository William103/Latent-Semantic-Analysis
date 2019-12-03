# Latent-Semantic-Analysis
Simple, inefficient implementation of LSA.

## Sample results

| --- | --- | --- |
| Input | Output | Comments |
| --- | --- | --- |
| Semantics is a kind of boring subfield. | Linguistics | Works great |
| linear algebra is very interesting | Math | It actually does some preliminary data processing so this doesn't mess it up |
| Historical linguistics is my favorite subfield. | Linguistics | Works great |
| That or computational linguistics. | Math | Sometimes it does screw up. My guess is most of these words aren't in the data set |
| vector calculus is fun too | Math | Works great |
| The fundamental theorem is important | Math | It sees "theorem" and "fundamental" in math contexts a lot |
| The theorem is important | Linguistics | But it sees "important" a lot in linguistics by a quirk of the data set, so gets it wrong here |

## How to download and use
If you want to attempt to run it, you will need python3 installed. I'm assuming
you know how to do that. You may also need to install numpy, a matrix library I
used to calculate eigenvalues and eigenvectors. To do this, type `pip install
numpy`, `pip3 install numpy`, `python -m pip install numpy`, `python3 -m pip
install numpy`, `python -m pip3 install numpy`, or `python3 -m pip3 install
numpy` on the command line. One of those should work on any operating system and
if it doesn't, then I can't help you. Then, to run it, type `python lsa.py` on
the command line. Then you can type something and the model will compare what
you inputted with all math documents and all linguistics documents and see what
matches the best in order to guess if you typed something mathy or linguisticsy.
I did not give it very much data, so it's not great, but in the context of the
data I gave it, it works perfectly. 

## How to expand
Like I said, there is not much data here. I really struggled to find good, clean
data, especially math data, in the form of text files, so I just typed up
whatever came to mind myself. If you find data, feel free to change data.txt.
If you change the data, you will need to change some of the code. At the very
top are three variables you can set how you need them.
`number_of_math_documents` is fairly self explanatory; if you change the number
of math documents (they MUST be first in data.txt), change this variable.
`recalculate` can be set to either "True" or "False" exactly like this without
the quotes; "True" if you want to recalculate the matrices and "False"
otherwise, just make sure to run it once with "True" if change things. It will
be much slower with "False" and will probably give some warnings you can ignore.
Finally, `k` is the rank approximation. If you are getting really bad results,
make this number higher. It basically sets how many singular values should be
kept and how many should be discarded. 10 is about the smallest number I've
gotten consistently good results with with an 18-dimensional document space (and
400-something dimensional term space; ideally you'd have a lot more documents
with not too many more words), but with better data, who knows.

## How it works
It's surprisingly straightforward. I wrote a quick matrix library in matrix.py
(originally we were going to implement everything from scratch, but I'm not
writing code to find eigenvalues and eigenvectors) and used that in svd.py to
implement singular value decomposition. This was very straightforward; all I had
to do was follow the algorithm and cheat once to calculate the eigenvalues and
eigenvectors using numpy. Next I wrote lsa.py, which is a giant mess of a
program that reads data, converts them into a frequency matrix with proper
weightings, feeds that matrix into svd.py, which spits out the matrices we need
(or just reads the precalculated matrices from a file), handles and processes
user input (converting it into the abstract term space using the matrices), and
finally compares it to the other documents and figures out which it is most
similar to, using the cosine of the angle between the vectors as a measure of
similarity.
