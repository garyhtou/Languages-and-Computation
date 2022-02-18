from functools import reduce
coordList = [(1, 4), (2, 5), (0, 2)]
print(sorted(coordList, key=lambda x: (x[0]**2+x[1]**2)**0.5))


def y(x):
    return (x[0]**2+x[1]**2)**0.5


print(sorted(coordList, key=y))


numbers = [(1, 2), (5, 2), (0.1, 2)]


print(reduce(lambda a, b: a if (
    a[0]/a[1]) < (b[0]/b[1]) else b, numbers))
