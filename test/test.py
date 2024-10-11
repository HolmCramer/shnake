from math import log

def main():
    numinator = 120
    denominator = 100
    
    for _ in range(20):
        result = log(numinator/denominator, 25)
        numinator += 10
        print(result)
        
main()