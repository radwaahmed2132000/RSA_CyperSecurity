
import sys, threading
import numpy as np
import math
import csv
import time 
from utils import *

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

# First, the Encryption & Decryption time vs. Execution time graph preparations.
p = []
q = []

# Read the testcases from the file
file = open('testcases.csv')
csvreader = csv.reader(file)
for row in csvreader:
    p.append(int(row[0]))
    q.append(int(row[1]))
file.close()

# Open a file to write the no. of bits of n, execution time of the encryption & decreption respectively.
file = open('graph_data.csv', 'w', encoding='UTF8', newline='')
csvwriter = csv.writer(file)

# Read message to use to test on all the testcases.
input_message = input("Enter message")

# Loop on all the testcases, calculate the encryption & decreption execution times.
for i in range(len(p)):

    timing_ed_data = []
    n = int(p[i]) * int(q[i])
    print('# of digits = ',len(str(n)))
    print(n,len(bin(n)[2:]))
    timing_ed_data.append(len(bin(n)[2:]))
    e,d = GenerateKeys(int(p[i]-1)*int(q[i]-1))

    # Prepare string
    message_trimmed = PrepareMessage(input_message, n)

    # Encryption
    start_time = time.time()
    ciphertext = Encrypt(message_trimmed, e, n)
    finish_time = time.time()
    total_time = finish_time - start_time
    print('Encryption Time = ', total_time*1000)
    timing_ed_data.append(total_time*1000)

    # Decryption
    start_time = time.time()
    message = Decrypt(ciphertext, d, n)
    finish_time = time.time()
    total_time = finish_time - start_time
    print('Decryption Time = ', total_time*1000)
    timing_ed_data.append(total_time*1000)
    
    print('Message',message)
    csvwriter.writerow(timing_ed_data)

file.close()

# Second, n vs. the Brute Force Attack Execution time graph preparations.
p = []
q = []

# Read the testcases from the file
file = open('brute_force_input.csv')
csvreader = csv.reader(file)
rows = []
for row in csvreader:
    rows.append(row)
    p.append(int(row[0]))
    q.append(int(row[1]))

file.close()

file2 = open('brute_force_data.csv', 'w', encoding='UTF8', newline='')
csvwriter2 = csv.writer(file2)

for i in range(len(p)):
    brute_force_data = []

    n = int(p[i]) * int(q[i])
    print('# of digits = ',len(str(n)))
    print(n,len(bin(n)[2:]))
    brute_force_data.append(n)
    e,d = keys(int(p[i]-1)*int(q[i]-1))

    # Brute Force Attack
    start_time = time.time()
    BruteForceAttack(e,n)
    finish_time = time.time()
    total_time = finish_time - start_time
    print('Brute Force Attack Time = ', total_time)
    brute_force_data.append(total_time)
    brute_force_data.append(len(bin(n)[2:]))

    csvwriter2.writerow(brute_force_data)

file2.close()