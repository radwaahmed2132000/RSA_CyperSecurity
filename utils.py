
import sys, threading
import numpy as np
import math

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

def ConvertToInt(message_str):
    res = 0
    for i in range(len(message_str)):
        res = res * 256 + ord(message_str[i])
    return res

def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]

def GCD(a, b):
    if b == 0:
        return a
    return GCD(b, a % b)

def ExtendedEuclid(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = ExtendedEuclid(b, a % b)
    k = a // b
    return (y, x - k * y)

# this is an R2L recursive implementation that works for large integers
def PowMod(a, n, mod): 
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    else:
        b = PowMod(a, n // 2, mod)
        b = b * b % mod
        if n % 2 == 0:
            return b
        else:
            return b * a % mod

def InvertModulo(a, n):
    (b, x) = ExtendedEuclid(a, n)
    if b < 0:
        b = (b % n + n) % n # we don't want -ve integers
    return b

def Encrypt( e, n):
    message =input("Enter message")
    print(e,n)
    M = ConvertToInt(message)
    while(M>n):
      message =input("Enter message again!!!")
      M = ConvertToInt(message)
    c = PowMod(ConvertToInt(message), e, n)
    return c

def Decrypt(c, p, q, d):
    # phi = (p-1)*(q-1)
    # d = InvertModulo(e, phi)
    m = ConvertToStr(PowMod(c, d, p * q ))
    return m


def checkvalidation(m):
    if(m<=1):
        return False
    for i in range(2, int(np.sqrt(m)) + 1):
        if (m % i == 0):
            return False
    return True

def  readvalue():
    p= int(input("Enter P"))
    q = int(input("Enter Q"))
    while p ==q:
        p= int(input("Enter P again"))
        q = int(input("Enter Q again"))
    if(not checkvalidation(p)):
        return False,p*q,(p-1)*(q-1),p,q
    if(not checkvalidation(q) ):
        return False,p*q,(p-1)*(q-1)
    return True,p*q,(p-1)*(q-1),p,q

# def modularInverse(e, phi):
#     for i in range(1, phi):
#         if (((e%phi) * (i%phi)) % phi == 1):
#             return i
#     return -1

def keys(n,phi):
    e=1
    for i in range (2, phi):
        if(GCD(i,phi)==1):
            e=i
            break
    # d=modularInverse(e,phi)
    d = InvertModulo(e, phi)
    return e,d,n

def BruteForceAttack(e,n):
    q=0
    p=0
    for i in range (2, n):
            if(n%i==0):
                check = False
                for j in range(2,i):
                    if(i%j==0):
                        check =True
                        break
                if(not check):
                    p = i
                    q = n/i
                    break
    phi = int( (p-1)*(q-1))
    d= InvertModulo(e,phi)
    return d

def ChosenCipherTextAttack(a,b):
    a = max(a,b)
    b= min(a,b)
    r=[]
    r.append(a)
    r.append(b)
    x=[]
    x.append(1)
    x.append(0)
    y=[]
    y.append(0)
    y.append(1)
    rn = a
    while(rn !=0):
        rn= r[-2] % r[-1]
        qn = math.floor(r[-2]/r[-1])
        x.append(x[-2]-qn*x[-1])
        y.append(y[-2]-qn*y[-1])
        r.append(rn)   
    return y[-2]

# p = 
# q = 1000000009
# exponent = 23917
# modulo = p * q
# ciphertext = Encrypt("attack", modulo, exponent)
# message = Decrypt(ciphertext, p, q, exponent)
# print(message)