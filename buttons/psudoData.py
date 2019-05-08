#! /usr/bin/env python3
from random import randint
import time
from time import sleep
import datetime

def writeLine(i):
    with open("sample.csv","a") as f:
        string = str(i) + ' ' +  str(randint(0,9)) 
        f.write(string)
        f.write("\n")
    return 

def main():
    print("data generation in progres..")
    i = 0
    while True:
        writeLine(i)
        i = i + 1 
        sleep(30)
    return

if __name__ == '__main__':
    main()
