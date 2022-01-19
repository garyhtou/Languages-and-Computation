"""
Gary Tou
CPSC 3400, Worksheet 3
1/10/2022
"""


def worksheet3a():
    def since_midnight(h, m, am_or_pm):
        """Calculate number of minutes from midnight to given time. 
        :param h: hour hand of clock as an int (i.e., 12, 1, 2, ..., 11) 
        :param m: minute hand of clock as an int 
        :param am_or_pm: either 'AM' or 'PM' 
        :return: number of minutes (0 for (12, 0, 'AM') up to 1439 for 
                (11, 59, 'PM')) 

        # FIXME: write the tests 
        """

    print(since_midnight(12, 0, 'AM'))


def worksheet3b():
    def p8():
        dict1 = {iso_weekdays[weekday_num]                 : 0 for weekday_num in iso_weekdays if weekday_num < 6}

    def p9():
        swap = {d[key]: key for key in d}

    def p10():
        rand_map = {}
        for i in range(10_000):
            rand_map[randint(lo, hi)] = i

    def p11():
        x_y_points = {}
        for x in x_vals:
            if abs(x) < 1.56e14:
                x_y_points[x] = f(x)

    def p12():
        def gen(value):
            next_val = input('value ' + str(value) + ': ')
            yield (next_val,)

        n = 5
        values = [gen(i) for i in range(1, n+1)]
        print(values)

    def p13():
        big_vals = []
        for x in x_vals:
            if f(x) > big_lim:
                big_vals.append(x)


def classExercise():
    """
    >>> [s for s in tuple_sums([(1, 2), (3, 4), (0, 7.3)], 6]]
    [7, 7.3]
    """
    def tuple_sums(pairs, threshold):
        for pair in pairs:
            sum = pair[0] + pair[1]
            if sum >= threshold:
                yield sum


def main():
    worksheet3a()
    worksheet3b()


if __name__ == "__main__":
    main()
