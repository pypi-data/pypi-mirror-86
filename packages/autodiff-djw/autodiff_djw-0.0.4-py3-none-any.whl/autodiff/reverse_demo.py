import reverse as rv
from reverse import Node

if __name__=='__main__':

    x = Node(0.5)
    y = Node(4.2)

    a = x * y
    a.grad_value = 1.0
    print("∂a/∂x = {}".format(x.grad())) # ∂a/∂x = 4.2

    # NOTE THE OUTPUT FUNCTION CAN'T HAVE THE SAME VARIABLE NAME AS OTHERS
    x = Node(2)
    y = Node(1)

    b = x * x * y * y
    b.grad_value = 1.0
    print("∂a/∂x = {}".format(x.grad())) # ∂a/∂x = 4.0
