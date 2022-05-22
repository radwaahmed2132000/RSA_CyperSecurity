
import sys, threading
import numpy as np
import math

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

# A function that converts a string message to a long integer.
# To turn it back to string use the function ConvertToStr.
# Input: string str_message
# Output: long int int_message
def ConvertToInt(str_message):
    int_message = 0
    for i in range(len(str_message)):
        int_message = ord(str_message[i]) + int_message * 256
    return int_message

# A function that converts a long integer to its respective string
# It is the opposite of the ConvertToInt function.
# Input: long int int_message
# Output: string str_message
def ConvertToStr(int_message):
    str_message = ""
    while int_message > 0:
        str_message += chr(int_message % 256)
        int_message //= 256
    return str_message[::-1]

# A function that calculates the Greatest Common Divisor (GCD) of two integers.
# Inputs: int integer_1, int integer_2
# Output: int -> GCD of the ints integer_1 & integer_2
def GCD(integer_1, integer_2):
    if integer_2 == 0:
        return integer_1
    return GCD(integer_2, integer_1 % integer_2)

# Extended Euclidean Algorithm that calculates the coefficients of Bezout's Identity.
# where x*integer_1 + y*integer_2 = gcd(integer_1,integer_2)
# Inputs: int integer_1, int integer_2
# Outputs: int, int -> coefficients of the ints integer_1 & integer_2 respectively.
def ExtendedEuclid(integer_1, integer_2):
    if integer_2 == 0:
        return (1, 0)
    (x, y) = ExtendedEuclid(integer_2, integer_1 % integer_2)
    return (y, x - (integer_1 // integer_2) * y)

# Modular Exponentiation Alogorithm that performs an exponentiation over a modulus.
# This is a right to left recursive implementation that works for large integers.
# It's as follows: remainder = base**(power) mod modulus.
# Inputs: int base, int power, int modulus.
# Output: int -> remainder when an integer (base) is raised to a power and divided by a positive integer (modulus).
def ModularExp(base, power, modulus): 
    if power == 0:
        return 1 % modulus
    elif power == 1:
        return base % modulus
    else:
        temp = ModularExp(base, power // 2, modulus)
        temp = temp * temp % modulus
        if power % 2 == 0:
            return temp
        else:
            return temp * base % modulus

# A function that gets the modular multiplicative inverse of an integer.
# where inverse*integer is congrent to 1 mod modulus.
# Inputs: int integer, int modulus.
# Output: int inverse.
def InvertModulo(integer, modulus):
    (inverse, extra) = ExtendedEuclid(integer, modulus)
    if inverse < 0:
        inverse = (inverse % modulus + modulus) % modulus # Because we don't want -ve integers.
    return inverse

# A function used to trim the message if it's bigger than n.
# Inputs: string input_message, int modulus.
# Output: string message_trimmed.
def PrepareMessage(input_message,modulus):
    message_trimmed = input_message
    M = ConvertToInt(input_message)
    j = 1
    if(M>modulus):
        print('Message is larger than n. Trimming it!!')
    while(M>modulus):
        M = ConvertToInt(input_message[0:-j])
        message_trimmed = input_message[0:-j]
        j += 1
    return message_trimmed

# RSA Encryption function.
# First, converts the message to integer then encrypts it using the public key by using the ModularExp function.
# Inputs: string plain_text, int encryption_key, int modulus. {encryption_key, modulus} is known as the public key.
# Output: int cipher_text.
def Encrypt(plain_text, encryption_key, modulus):
    cipher_text = ModularExp(ConvertToInt(plain_text), encryption_key, modulus)
    return cipher_text

# RSA Decryption function.
# First, decrypts the cipher using the private key by using the ModularExp function.then converts it to string.
# Inputs: int cipher_text, int decryption_key, int modulus. {decryption_key, modulus} is known as the private key.
# Output: string plain_text.
def Decrypt(cipher_text, decryption_key, modulus):
    plain_text = ConvertToStr(ModularExp(cipher_text, decryption_key, modulus))
    return plain_text

# A function that checks whether an integer is a prime or not.
# Input: int integer.
# Output: bool is_prime True-> integer is a prime / False -> integer is not a prime.
def CheckIfPrime(integer):
    if(integer<=1):
        return False
    for i in range(2, int(np.sqrt(integer*1.0)) + 1):
        if (integer % i == 0):
            return False
    return True

# A function that reads the p & q values from the user.
# It checks that they are prime before returning them.
# where modulus = p * q, phi = (p-1)*(q-1)
# are_prime -> True if both p & q are prime / -> False otherwise.
# Inputs: _
# Outputs: bool are_prime, int modulus, int phi, int p, int q.
def ReadValues():
    p = int(input("Enter P"))
    q = int(input("Enter Q"))
    while p == q:
        p = int(input("Enter P again"))
        q = int(input("Enter Q again"))
    if(not CheckIfPrime(p)):
        return False,p*q,(p-1)*(q-1),p,q
    if(not CheckIfPrime(q) ):
        return False,p*q,(p-1)*(q-1)
    return True,p*q,(p-1)*(q-1),p,q

# A key generation function that generates a pair of keys (public and private keys).
# Input: int phi.
# Outputs: int encryption_key, int decryption_key.
def GenerateKeys(phi):
    encryption_key=1
    for i in range (phi//2, phi):
        if(GCD(i,phi)==1):
            encryption_key=i
            break
    decryption_key = InvertModulo(encryption_key, phi)
    return encryption_key,decryption_key

# A brute force attack that attempts to find the private key given the modulus and the public key.
# Inputs: int encryption_key, int modulus.
# Output: int decryption_key.
def BruteForceAttack(encryption_key,modulus):
    q=0
    p=0
    for i in range (2, modulus):
            if(modulus%i==0):
                check = False
                for j in range(2,i):
                    if(i%j==0):
                        check =True
                        break
                if(not check):
                    p = i
                    q = modulus/i
                    break
    phi = int( (p-1)*(q-1))
    decryption_key = InvertModulo(encryption_key,phi)
    return decryption_key

# Chosen Ciphertext Attack Algorithm.
# Inputs: int a, int b.
# Output: int decryption_key.
def ChosenCipherTextAttack(a,b):
    a = max(a,b)
    b = min(a,b)
    r = []
    r.append(a)
    r.append(b)
    x = []
    x.append(1)
    x.append(0)
    y = []
    y.append(0)
    y.append(1)
    rn = a
    while(rn != 0):
        rn= r[-2] % r[-1]
        qn = math.floor(r[-2]/r[-1])
        x.append(x[-2]-qn*x[-1])
        y.append(y[-2]-qn*y[-1])
        r.append(rn)   
    return y[-2]