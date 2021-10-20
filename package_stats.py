#!/usr/bin/env python3

#imports
import wget
import sys
import os
from sh import gunzip
from collections import Counter
# import subprocess

# fail when no parameter added
if len(sys.argv) != 2:
    raise ValueError('\n\nPlease,\nprovide architecture as parameter (amd64, arm64, mips etc.)\n')

#read parameter
arch = sys.argv[1]

# remove old content if existing
folder = './'
for file in os.listdir(folder):
    if file.endswith('.gz'):
        os.unlink(os.path.join(folder, file))

folder = './'
for file in os.listdir(folder):
    if file.startswith('Contents'):
        os.unlink(os.path.join(folder, file))

#pulling file
print(f'Pulling Contents for {arch} architecture')
filename='Contents-'+ arch +'.gz'
url='http://ftp.de.debian.org/debian/dists/stable/main/'+filename
file = wget.download(url)
file

# #make exec
# os.chmod(file,0o775)

#unzip file
print(f'\nunpacking...')
gunzip('./'+file)

#parsing part as bruteforce forst i will do bash takes ca. 2 sec
# print(f'processing in bash ...')
# bashCommand = "awk '{print $2}' Contents-amd64 | awk -F / {'print $NF}' | uniq -c| sort -nr |head -n 10"
# bashout = subprocess.check_output(['bash','-c', bashCommand])
# print(bashout)

print(f'processing...')

packages=[]
for line in open('Contents-'+ arch):
    columns = line.split("/")
    if len(columns) >= 2:
        packages.append(columns[-1])

print(f'sorting occurences...')

unique = list(set(packages))
frequency = {}

print(f'creating lists...')

for item in unique:
    frequency[item] = packages.count(item)

print(f'sorting uniq...')

supsort=Counter(frequency)
final=supsort.most_common()
print("the top 10 packages that have the most files associated with them.\n")

num=1
for line in final[:10] :
    print(num, line)
    num=num+1


#finish
print("\ndone")