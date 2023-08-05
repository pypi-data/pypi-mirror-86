import numpy as np

class Node:
    def __init__(self, **kwargs):
        self.val = 0
        self.children = [] 
        self.grad_value = None #the adjoint
        
        # QUESTION - HOW DO WE HANDLE CHILDREN IN kwargs?
        if 'val' in kwargs: 
            self.val = kwargs['val']
            
    ### KEY TO THE REVERSE MODE: ###
    # The recursive differentiation function 
    # Source (Adapted From): https://rufflewind.com/2016-12-30/reverse-mode-automatic-differentiation
    def grad(self):
        # recurse only if the value is not yet cached
        if self.grad_value is None:
            # recursively calculate derivative (adjoint) using chain rule
            self.grad_value = sum(weight * node.grad()
                                  for weight, node in self.children)
        return self.grad_value

    ### MATHEMATICAL OPERATORS ###
    # 1) Multiplication, 2) Division, 3) Addition, 4) Subtraction, 5) Power
    
    # 1) Multiplication
    def __mul__(self, other):
        out = Node()
        try:
            out.val = self.val*other.val
            self.children.append((other.val, out)) # weight = ∂z/∂self = other.value
            other.children.append((self.val, out)) # weight = ∂z/∂other = self.value
        except AttributeError:
            try:
                out.val = self.val*other
                self.children.append((other, out)) # weight = ∂z/∂self = other.value
            except Exception as e:
                raise TypeError('Multiplication failed: `other` not an `Node` object neither a real number.')
        return out

    def __rmul__(self, other):
        return self.__mul__(other)

    # 2) Division
    def __truediv__(self, other):
        out = Node()
        try:
            out.val = self.val / other.val
            self.children.append((1/other.val, out)) # weight = ∂z/∂self = 1/other.value
            other.children.append((-1*self.val/other.val**2, out)) # weight = ∂z/∂other = -1*self.value/ other.value**2
        except AttributeError:
            try:
                out.val = self.val/other
                self.children.append((1/other, out)) # weight = ∂z/∂self = 1/other
            except Exception as e:
                raise TypeError('Division failed: `other` not an `Node` object neither a real number.')
        return out
    
    def __rtruediv__(self, other):
        out = Node()
        
        try:
            out.val = other.val / self.val
            self.children.append((-1*other.val/ self.val**2, out)) # weight = ∂z/∂self = -1*other.value/ self.value**2
            other.children.append((1/self.val, out)) # weight = ∂z/∂other = 1 / self.value
        except AttributeError:
            try:
                out.val = other / self.val
                self.children.append((-1*other/ self.val**2, out)) # weight = ∂z/∂self = -1*other/ self.value**2
            except Exception as e:
                raise TypeError('Reverse Division failed: `self` not an `Node` object neither a real number.')
        
        return out
        
    # 3) Addition
    def __add__(self, other):
        out = Node()
        try:
            out.val = self.val + other.val
            self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            other.children.append((1.0, out)) # weight = ∂z/∂other = 1            
        except AttributeError:
            try:
                out.val = self.val + other
                self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            except Exception as e:
                raise TypeError('Addition failed: `other` not an `Node` object neither a real number.')
        return out
    
    def __radd__(self, other):
        return self.__add__(other)  
    
    # 4) Subtraction
    def __sub__(self, other):
        out = Node()
        try:
            out.val = self.val - other.val
            self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            other.children.append((-1.0, out)) # weight = ∂z/∂other = -1            
        except AttributeError:
            try:
                out.val = self.val - other
                self.children.append((1.0, out)) # weight = ∂z/∂self = 1
            except Exception as e:
                raise TypeError('Subtraction failed: `other` not an `Node` object neither a real number.')
        return out
    
    def __rsub__(self, other):
        out = Node()
        try:
            out.val = other.val - self.val
            self.children.append((-1.0, out)) # weight = ∂z/∂self = 1
            other.children.append((1.0, out)) # weight = ∂z/∂other = -1            
        except AttributeError:
            try:
                out.val = other - self.val
                self.children.append((-1.0, out)) # weight = ∂z/∂self = 1
            except Exception as e:
                raise TypeError('Reverse Subtraction failed: `self` not an `Node` object neither a real number.')
        return out
    
    # 5) Power
    #NOTE left argument (self) MUST BE > 0
    def __pow__(self, other):    
        out = Node()
        try:
            out.val = self.val**other.val
            self.children.append((other.val * self.val ** (other.val - 1), out)) # weight = ∂z/∂self = other.value * self.value ** (other.value - 1)
            other.children.append((self.val ** other.val * np.log(self.val), out)) # weight = ∂z/∂other = self.value ** other.value * log(self.value)
        except AttributeError:
            try:
                out.val = self.val**other
                self.children.append((other * self.val ** (other - 1), out)) # weight = ∂z/∂self = other * self.value ** (other - 1)
            except Exception as e:
                raise TypeError('Power failed: `other` not an `Node` object neither a real number.')
        return out

    def __rpow__(self, other):    
        out = Node()
        try:
            out.val = other.val ** self.val
            self.children.append((other.val ** self.val * np.log(other.val), out)) # weight = ∂z/∂self = self.value ** other.value * log(self.value)
            other.children.append((self.val * other.val ** (self.val - 1), out)) # weight = ∂z/∂other = other.value * self.value ** (other.value - 1)
        except AttributeError:
            try:
                out.val = other ** self.val
                self.children.append((other ** self.val * np.log(other), out)) # weight = ∂z/∂self = self.value ** other.value * log(self.value)
            except Exception as e:
                raise TypeError('Reverse Power failed: `self` not an `Node` object neither a real number.')
        return out
    
    ### CLASS METHODS ###
    # 1) len, 2) str, 3) repr, etc.
    # TO DO
    
### NUMPY FUNCTIONS ###
# 1) log (i.e. ln), 2) exp, 3) sin, 4) cos, 5) tan

# 1) Logarithm    
def log(a):
    out = Node()
    try:
        out.val = np.log(a.val)
        a.children.append((1/a.val, out)) # weight = ∂z/∂self = 1 / self
    except AttributeError:
        try:
            out.val = np.log(a)
        except Exception as e:
            raise TypeError('Logarithm failed: `input` not an `Node` object, positive number or a real number.')
    return out

# 2) Exponent
def exp(a):
    out = Node()
    try:
        out.val = np.exp(a.val)
        a.children.append((np.exp(a.val), out)) # weight = ∂z/∂self = exp(self)
    except AttributeError:
        try:
            out.val = np.exp(a)
        except Exception as e:
            raise TypeError('Exponential failed: `input` not an `Node` object or a real number.')
    return out

# 3) Sin        
def sin(a):
    out = Node()
    try:
        out.val = np.sin(a.val)
        a.children.append((np.cos(a.val), out)) # weight = ∂z/∂self = cos(self)
    except AttributeError:
        try:
            out.val = np.sin(a)
        except Exception as e:
            raise TypeError('Sin failed: `input` not an `Node` object or a real number.')
    return out

# 4) Cos        
def cos(a):
    out = Node()
    try:
        out.val = np.cos(a.val)
        a.children.append((-1*np.sin(a.val), out)) # weight = ∂z/∂self = -sin(self)
    except AttributeError:
        try:
            out.val = np.cos(a)
        except Exception as e:
            raise TypeError('Cos failed: `input` not an `Node` object or a real number.')
    return out

# 5) Tan        
def tan(a):
    out = Node()
    try:
        out.val = np.tan(a.val)
        a.children.append((1/(np.cos(a.val))**2, out)) # weight = ∂z/∂self = 1/(cos(self))^2
    except AttributeError:
        try:
            out.val = np.tan(a)
        except Exception as e:
            raise TypeError('Tan failed: `input` not an `Node` object or a real number.')
    return out
