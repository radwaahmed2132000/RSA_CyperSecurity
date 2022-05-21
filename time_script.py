
import sys, threading
import numpy as np
import math
import csv
import time 
from utils import *

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

p = []
q = []

file = open('testcases.csv')
csvreader = csv.reader(file)
rows = []
for row in csvreader:
    rows.append(row)
    p.append(int(row[0]))
    q.append(int(row[1]))

file.close()
# data = np.array(rows).astype(int)
# data = rows

# p = data[:,0]
# q = data[:,1]
# print(p)
# print(q)

file = open('graph_data.csv', 'w', encoding='UTF8', newline='')
csvwriter = csv.writer(file)
input_message = input("Enter message")

no_of_digits = []
encryption_execution_times = []
decryption_execution_times = []

# for i in range(p.shape[0]):
for i in range(len(p)):
    row_data = []
    n = int(p[i]) * int(q[i])
    print('# of digits = ',len(str(n)))
    print(n,len(bin(n)[2:]))
    no_of_digits.append(len(bin(n)[2:]))
    row_data.append(len(bin(n)[2:]))
    e,d,n = keys(n, int(p[i]-1)*int(q[i]-1))

    # Prepare string
    message_trimmed = input_message
    M = ConvertToInt(input_message)
    j = 1
    if(M>n):
        print('Message is larger than n. Trimming it!!')
    while(M>n):
        M = ConvertToInt(input_message[0:-j])
        message_trimmed = input_message[0:-j]
        j += 1

    # Encryption
    start_time = time.time()
    ciphertext = Encrypt(message_trimmed, e, n)
    finish_time = time.time()
    total_time = finish_time - start_time
    print('Encryption Time = ', total_time*1000)
    row_data.append(total_time*1000)
    encryption_execution_times.append(total_time*1000)

    # Decryption
    start_time = time.time()
    message = Decrypt(ciphertext, n, d)
    finish_time = time.time()
    total_time = finish_time - start_time
    print('Decryption Time = ', total_time*1000)
    row_data.append(total_time*1000)
    decryption_execution_times.append(total_time*1000)
    
    print('Message',message)
    csvwriter.writerow(row_data)

file.close()