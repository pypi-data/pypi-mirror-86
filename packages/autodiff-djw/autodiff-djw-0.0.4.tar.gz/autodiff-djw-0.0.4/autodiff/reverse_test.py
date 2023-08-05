# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:19:53 2020

@author: david
"""

## Usage case

import reverse as rv
from reverse import Node

if __name__=='__main__':

    # NOTE THE OUTPUT FUNCTION CAN'T HAVE THE SAME VARIABLE NAME AS OTHER FUNCTIONS

    # MULTIPLICATION TESTS
    x = Node(val = 0.5)
    y = Node(val = 4.2)

    a = x * y
    a.grad_value = 1.0
    print("∂a/∂x = {}".format(x.grad())) # ∂a/∂x = 4.2

    x = Node(val = 2)
    y = Node(val = 1)

    b = x * x * y * y
    b.grad_value = 1.0
    print("∂b/∂x = {}".format(x.grad())) # ∂b/∂x = 4.0

    # ADDITION TEST
    x = Node(val = 2)
    y = Node(val = 1)

    c = x + x + y
    c.grad_value = 1.0
    print("∂c/∂x = {}".format(x.grad())) # ∂c/∂x = 2.0

    x = Node(val = 2)

    d = 1.0 + x + x
    d.grad_value = 1.0
    print("∂d/∂x = {}".format(x.grad())) # ∂d/∂x = 2.0
    print(d.val)

    # SUBTRACTION TEST
    x = Node(val = 2)
    y = Node(val = 1)

    e = 1 - x - x - y
    e.grad_value = 1.0
    print("∂e/∂x = {}".format(x.grad())) # ∂e/∂x = -2
    print(e.val) # -4

    x = Node(val = 2)
    y = Node(val = 1)

    f = x - y
    f.grad_value = 1.0
    print("∂f/∂x = {}".format(y.grad())) # ∂f/∂x = -1
    print(f.val) # 1

    # DIVISION TESTS
    x = Node(val = 0.5)
    y = Node(val = 4.2)

    g = x / y
    g.grad_value = 1.0
    print("∂g/∂y = {}".format(y.grad())) # ∂g/∂y = -0.028

    y = Node(val = 4.2)

    h = 0.5 / y
    h.grad_value = 1.0
    print("∂h/∂y = {}".format(y.grad())) # ∂h/∂y = -0.028

    # POWER TESTS
    x = Node(val = 1.5)
    y = Node(val = 2.5)

    i = x ** y #NOTE x MUST BE > 0
    i.grad_value = 1.0
    print("∂i/∂x = {}".format(x.grad())) # ∂i/∂x = 4.593
    print("∂i/∂y = {}".format(y.grad())) # ∂i/∂y = 1.117

    y = Node(val = 2.5)

    j = 1.5 ** y
    j.grad_value = 1.0
    print("∂j/∂y = {}".format(y.grad())) # ∂j/∂y = 1.117

    x = Node(val = 1.5)

    k = x ** x
    k.grad_value = 1.0
    print("∂k/∂y = {}".format(x.grad())) # ∂k/∂x = 2.582

    x = Node(val = 1.5)

    k = x ** x
    k.grad_value = 1.0
    print("∂k/∂y = {}".format(x.grad())) # ∂k/∂x = 2.582


    # LOGARITHM TESTS
    x = Node(val = 1.5)

    l = rv.log(x) #NOTE x MUST BE > 0
    l.grad_value = 1.0
    print("∂l/∂x = {}".format(x.grad())) # ∂l/∂x = 0.6666

    # EXPONENT TESTS
    x = Node(val = 1.5)

    m = rv.exp(x) 
    m.grad_value = 1.0
    print("∂m/∂x = {}".format(x.grad())) # ∂m/∂x = 4.48

    # SIN TESTS
    x = Node(val = 1.5)

    n = rv.sin(x) 
    n.grad_value = 1.0
    print("∂n/∂x = {}".format(x.grad())) # ∂n/∂x = 0.07

    # COS TESTS
    x = Node(val = 1.5)

    o = rv.cos(x) 
    o.grad_value = 1.0
    print("∂o/∂x = {}".format(x.grad())) # ∂o/∂x = -0.997

    # TAN TESTS
    x = Node(val = 1.5)

    p = rv.tan(x) 
    p.grad_value = 1.0
    print("∂p/∂x = {}".format(x.grad())) # ∂p/∂x = 199.85