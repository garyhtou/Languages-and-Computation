import re
import hw6  # your file must be named hw6.py

def test(p, s, expected):
    """Test s with regular expression p to get expected result.
    >>> test(re.compile(r'a*b*'), 'aaaabb', True)
    re.compile('a*b*') passed on accepting 'aaaabb'
    >>> test(re.compile(r'a*b*'), 'aaaabb', False)
    re.compile('a*b*') FAILED by not rejecting 'aaaabb' (got <re.Match object; span=(0, 6), match='aaaabb'>)
    >>> test(re.compile(r'a*b*'), 'aaaabbccc', True)
    re.compile('a*b*') FAILED by rejecting 'aaaabbccc'
    >>> test(re.compile(r'a*b*'), 'aaaabbccc', False)
    re.compile('a*b*') passed on rejecting 'aaaabbccc'
    """
    m = p.fullmatch(s)
    if m is None:
        if not expected:
            print("{} passed on rejecting '{}'".format(p, s))
        else:
            print("{} FAILED by rejecting '{}'".format(p, s))
    else:
        if not expected:
            print("{} FAILED by not rejecting '{}' (got {})".format(p, s, m))
        else:
            print("{} passed on accepting '{}'".format(p, s))


if __name__ == '__main__':
    re_a = re.compile(hw6.a)
    test(re_a, '15445', True)
    test(re_a, '55', True)
    test(re_a, '05563', True)
    test(re_a, '555', False)

    re_b = re.compile(hw6.b)
    test(re_b, '1:45 PM', True)
    test(re_b, '0:59 AM', False)

    re_c = re.compile(hw6.c)
    test(re_c, 'hello, get_max, sum3', True)
    test(re_c, '', True)
    test(re_c, '_673x', True)
    test(re_c, ', x, y', False)
    test(re_c, '_673x, 8y, ww', False)

    re_d = re.compile(hw6.d)
    test(re_d, 'a < b', True)
    test(re_d, 'a <= b', True)

    print('part d test 1')
    result = re_d.sub(hw6.d_sub, 'if a < b: # just less than')
    expected = 'if b > a: # just less than'
    if result == expected:
        print('passed')
    else:
        print("FAILED\nexpected: '{}'\ngot:      '{}'".format(expected, result))

    print('part d test 2')
    result = re_d.sub(hw6.d_sub, 'if (a <= b ||  _c_89   <woohoo){')
    expected = 'if (b >= a ||  woohoo > _c_89){'
    if result == expected:
        print('passed')
    else:
        print("FAILED\nexpected: '{}'\ngot:      '{}'".format(expected, result))
