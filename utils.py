
import sys, threading
import numpy as np
import math
import csv
import time 

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

# Used to trim the message if it's bigger than n
def prepare_message(input_message,n):
    message_trimmed = input_message
    M = ConvertToInt(input_message)
    j = 1
    if(M>n):
        print('Message is larger than n. Trimming it!!')
    while(M>n):
        M = ConvertToInt(input_message[0:-j])
        message_trimmed = input_message[0:-j]
        j += 1
    return message_trimmed

def Encrypt(message, e, n):
    # message = input("Enter message")
    # print(e,n)
    M = ConvertToInt(message)
    # print("M = ",M)
    # i = 1
    # if(M>n):
    #     print('Message is larger than n. Trimming it!!')
    # while(M>n):
    #     M = ConvertToInt(message[0:-i])
    #     i += 1
    #   message = input("Enter message again!!!")
    #   M = ConvertToInt(message)
    c = PowMod(M, e, n)
    return c

def Decrypt(c, n, d):
    m = ConvertToStr(PowMod(c, d, n))
    return m


def checkvalidation(m):
    if(m<=1):
        return False
    for i in range(2, int(np.sqrt(m*1.0)) + 1):
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

def keys(n,phi):
    e=1
    for i in range (phi//2, phi):
        if(GCD(i,phi)==1):
            e=i
            break
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

# p = 1000000007
# q = 1000000009
# exponent = 23917
# n = p * q
# ciphertext = Encrypt("attack", n, exponent)
# message = Decrypt(ciphertext, n, exponent)
# print(message)

# "Crypto ~2022&!"
# p = 790383132652258876190399065097
# q = 662503581792812531719955475509
# p = 11
# q = 71
# exponent = 23917
# n = p * q
# print(n,len(bin(n)[2:]))
# e,d,n = keys(n, (p-1)*(q-1))
# ciphertext = Encrypt(e, n)
# print('Using e: ', ciphertext)
# message = Decrypt(ciphertext, n, d)
# print(message)
# ciphertext = Encrypt(d, n)
# print('Using d: ', ciphertext)
# message = Decrypt(ciphertext, n, e)
# print('Using d: ', message)

# start_time = time.time()
# p = 790383132652258876190399065097
# q = 662503581792812531719955475509
# exponent = 23917
# n = p * q
# ciphertext = Encrypt(exponent, n)
# finish_time = time.time()

# total_time = finish_time - start_time
# print('Total Time = ', total_time)