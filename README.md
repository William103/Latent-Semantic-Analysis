# Latent-Semantic-Analysis
Simple, inefficient implementation of LSA.

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
You will likely need to make some changes to the code, though. The first time
you run it after changing the data, you need to uncomment the line 152 and
comment line 151. This will recalculate the matrices the next time you run it.
After it has recalculated them, you can change it back to how it was to make
things run faster. Also, make sure the math documents are first in data.txt and
change the number in line 219 to the number of math documents.

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
