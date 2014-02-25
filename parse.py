import pprint
import os

def parse( f_name, d ):
    """to start, count how many messages each person has typed"""
    for line in open(f_name):
        line = line.split()

        if len(line) != 4:
            continue

        try:
            d[ line[2] ] += 1

        except:
            d[ line[2] ] = 1

    return d


#parse("2014-02-24:0.txt")

file_list = []

for f in os.listdir('.'):
    if (f.lower().endswith('.txt')):
            file_list.append(f)

print(file_list)

d = {}

for f in file_list:
    d = parse(f, d)

pprint.pprint(d)




  

