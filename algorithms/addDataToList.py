import datetime
from datetime import timedelta, date


l = [0,100,0,100,0,100]
t = [1,2,3,4,5,6]

def addDataToList(list_1,list_2):
    n = 0
    list_1_1 = []
    list_2_2 = []

    for i in list_1:
        if n == 0:
            list_1_1.append(i)
            list_2_2.append(list_2[n])
        else:

            list_1_1.append(list_1[n-1])
            list_1_1.append(i)
            list_2_2.append(list_2[n]-.001)
            list_2_2.append(list_2[n])
        n += 1
    print(list_1_1)
    print(list_2_2)

    return

def main():
    addDataToList(l,t)
    return

if __name__ == '__main__':
    main()
