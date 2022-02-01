import random
N = int(input("Enter the number of trials (enter a large number to get an accurate expected value) "))
def rand():
    i = 0
    k = 0
    while i<1:
        k=k+1
        i = i +random.random()
    return k
print(sum(rand() for _ in range(N))/N)








