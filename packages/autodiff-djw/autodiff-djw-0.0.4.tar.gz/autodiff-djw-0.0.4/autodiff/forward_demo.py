import numpy as np
from forward import Variable

if __name__=='__main__':

    # Forward, single function output
    # Expected (f1.val == -0.172, f1.der == 3.94)

    x1 = Variable(val=np.pi/16, der=1)
    f1 = x1 - np.exp(-2*(np.sin(4*x1)**2))


    print(f1.val, f1.der)
