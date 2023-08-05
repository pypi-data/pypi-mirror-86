# Quantum Mechanics Library
A small python quantum mechanics library which simplifies the notation of numpy and tailors it for quantum mechanics teaching
# Installation
The library can be used by placing the <span>QM</span>.py alongside your code, or be installed on your system by typing the following into your terminal:
```bash
python setup.py install
```
The library is also registred with PyPi and you can install it with:
```bash
pip install QM-KU
```

# Quick start
```python
# Load library
import QM as q

# bra <v| = [1, 5, 2]
v = q.bra([1, 5, 2])

# ket |w> = [9, 0, 5]
w = q.ket([9, 0, 5])

# Operator M = [7, 3, 0]
#              |2, 7, 3|
#              [8, 4, 5]
M = q.operator([[7, 3, 0], [2, 7, 3], [8, 4, 5]])

# <v|w>
a = v * w

# <v|v*>
b = v * v.H

# <v|M|w>
c = v * M * w
```
# Documentation
This library introduces three classes ```bra```, ```ket``` and ```operator```.

All of three objects are array-like:
```bra```, ```ket``` are vector-like, while ```operator``` is matrix-like.

The classes are subclasses of numpy.ndarray, and they work with numpy functions. (e.g. np.shape(), np.linalg.norm())

The classes overload the arithmatic operator +, -, and * such that they obey the rules of Dirac notation.
That is, multiplication can only be done between the correct classes and the operation does not commute.

In addition to introducing Dirac-like arithmatic operator, the library includes two methods:

.prob() - Which works on ```bra``` and ```ket``` and returns a numpy.ndarray containing the absolute value of each element

.eig() - Which works on ```operator``` and returns a tuple containing a numpy.ndarray of sorted eigenvalues, followed by an operator with the sorted eigenvectors. The n'th eigenvector is stored at index n in the operator.
