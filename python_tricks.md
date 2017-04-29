# Python Tricks - [Notebook](./python_tricks.ipynb)

### Contents
* [Explicit integer division](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#explicit-integer-division)
* [Helpful numeric formats](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#helpful-numeric-formats)
* [Symbolic math with sympy](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#symbolic-math-with-sympy)
* [Viewing doc strings with `__doc__`](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#viewing-doc-strings-with-__doc__)
* [Profiling code snippet performance with timeit ](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#profiling-code-snippet-performance-with-timeit)
* [Passing a variable number of function arguments with `**kwargs`](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#passing-a-variable-number-of-function-arguments-with-kwargs)
* [Function passing](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#function-passing)
* [Anonymous (lambda) functions](https://github.com/jphall663/GWU_data_mining/blob/master/python_tricks.md#anonymous-lambda-functions)

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

#### Passing a variable number of function arguments with `**kwargs`

```python
def f(**kwargs):
    
    # kwargs is a dict
    if kwargs is not None:
        for key, val in sorted(kwargs.items()):
            print('%s = %s' %(key, val))
            
    print('----------')
        
f(a='hello')
f(a='hello', b='world')
f(a='goodbye', b='cruel', c='world')

# a = hello
# ----------
# a = hello
# b = world
# ----------
# a = goodbye
# b = cruel
# c = world
# ----------
```

#### Function passing

```python
# import numeric sine function
from math import sin
print(sin(0))

# simple function for numerical derivative of f at x
def num_dfdx(f, x, h):
    
    return (f(x + h) + f(x))/float(h)

print(num_dfdx(sin, 0, 0.01))
print(num_dfdx(sin, 0, 0.000001))

# 0.0
# 0.9999833334166665
# 0.9999999999998334
```

#### Anonymous (lambda) functions

* Define simple functions in one line of code
```python
# simple function for numerical derivative of f at x
def num_dfdx(f, x, h):
    
    return (f(x + h) - f(x))/float(h)

num_dfdx(lambda x: x**2, 1, 1e-6)
# 2.0000009999243673

magnitude = lambda x: 'small' if 1 >= x >= -1 else 'big'
print(magnitude(0.5))
# small

# map and lamba used often to apply a simple function
# to all elements in a list
list(map(lambda x: x**2, range(0,10)))
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

#### Sets

#### List comprehensions