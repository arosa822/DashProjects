FILE = 'sample.csv'

def parse(FILE):
    '''
    Usage: [x,y] = parse('file.csv')
    '''
    x = []
    y = []
    with open(FILE) as f:
        for row in f:
            line = row.split()
            x.append(line[0])
            y.append(line[1])
    return x,y

def main():
    [x,y] = parse(FILE)
    #print(x[10:])
    #print(y[10:])
    return

if __name__ == '__main__':
    main()
