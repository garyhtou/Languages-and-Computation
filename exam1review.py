def genFactors(n):
    for i in range(1, n+1):
        if(n % i == 0):
            yield i


if __name__ == '__main__':
    for i in genFactors(48):
        print(i)
