# Python Tricks - [Notebook](./python_tricks.ipynb)

#### Explicit integer division

```python
type(4/2)   # float
type(4//2)  # int, double slash performs integer division
```

#### Helpful numeric formats

```python
# printf-like syntax
# """ allows printed statements in multiple lines

print("""
Compact decimal notation: %g 
Compact scientific notation: %e
Percent sign: %.2f%%
""" % (1234.5678, 1234.5678, 1234.5678))

# Compact decimal notation: 1234.57 
# Compact scientific notation: 1.234568e+03
# Percent sign: 1234.57%

# format string syntax

print("""
Compact decimal notation: {dec_:g}
Compact scientific notation: {exp_:e}
Percent sign: {per_:.2f}%
""".format(dec_=1234.5678, exp_=1234.5678, per_=1234.5678))

# Compact decimal notation: 1234.57
# Compact scientific notation: 1.234568e+03
# Percent sign: 1234.57%
```

#### Symbolic math with sympy

```python
from math import pi
from sympy import (
    symbols,    # define symbols
    diff,       # derivatives
    integrate,  # integrals
    lambdify,   # symbolic expression -> python function
    latex,      # create latex expressions
    sin         # symbolic sine function
)

x = symbols('x')
y = sin(x)
dydx = diff(y, x)  # cos(x)
integrate(dydx)    # sin(x)

f = lambdify(x, y)
f(pi/2)            # 1.0

y.series(x, 0, 6)  # x - x**3/6 + x**5/120 + O(x**6)

print(latex(y.series(x, 0, 6)))
# x - \frac{x^{3}}{6} + \frac{x^{5}}{120} + \mathcal{O}\left(x^{6}\right)
```

#### Viewing doc strings with `__doc__`
* Also using zip() for multiple list processing 
```python
list1 = ['a', 'b', 'c', 'd', 'e']
list2 = [1, 2, 3, 4, 5]

def f(list1, list2):
    
    """ Uses zip to process 2 lists in parallel.
    
    Args:
        list1: first list.
        list2: second list.
    
    """
    
    for i, j in zip(list1, list2):
        print(i, j)

print(f.__doc__)
 
# Uses zip to process 2 lists in parallel.
    
#    Args:
#        list1: first list.
#        list2: second list.

f(list1, list2)

# a 1
# b 2
# c 3
# c 4
# e 5
```

#### Profiling code snippet performance with timeit 
* Notice performance increase when list is pre-initialized
```python
import timeit
n = 10000000
list3 = [0]*n
list4 = []
print(timeit.timeit('for i in range(0, n): list3[i] = i', number=1, setup='from __main__ import n, list3'))
print(timeit.timeit('for i in range(0, n): list4.append(i)', number=1, setup='from __main__ import n, list4'))

# 0.5378604060970247
# 0.8394112652167678
```