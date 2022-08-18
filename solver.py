import numpy as np

def sign(value):
    if value < 0:
        return -1
    elif value == 0:
        return 0
    return 1

def degree(p):
    return max(p.keys())

def p_to_str(p):
    s = ''
    for i in p.keys():
        if i != 0 and p[i] != 0:
            s += str(p[i]) + '*' + 'x^' + str(i) + ' + '
    if 0 in p.keys() and p[0] != 0:
        s += str(p[0])
    else:
        s = s[:-2]
    return s

def derivative(p):
    q = {}
    m = max(p.keys())
    for i in p.keys():
        if i != 0:
            q[i - 1] = i * p[i] / m
    return q

def discard_zero_roots(p):
    q = {}
    m = min(p.keys())
    for deg, coef in p.items():
        q[deg - m] = coef
    return q

def evaluate(p, x_value):
    result = 0
    for deg, coef in p.items():
        result += (coef) * (x_value) ** deg
    return result

def big_evaluate(p, x_value):
    result = (0)
    n = max(p.keys())
    if abs(x_value) > 1:
        if x_value != 0:
            for deg, coef in p.items():
                result += (coef) * (x_value) ** (deg - n)
            if x_value < 0 and n % 2 == 1:
                result = - result
        else:
            if 0 in p.keys():
                result = ((p[0]))
    else:
        for deg, coef in p.items():
            result += ((coef)) * (x_value) ** deg
    return result


def bisection(a, b, tolerance, p, pdiff):
    p_a = big_evaluate(p, a)
    p_b = big_evaluate(p, b)
    m = (a + b) / 2
    p_m = big_evaluate(p, m)

    if p_a == 0:
        return a
    elif p_b == 0:
        return b
    while abs(b - a) > tolerance:
        if p_a * p_m <= 0:
            b = m
            p_b = p_m
        elif p_b * p_m <= 0:
            a = m
            p_a = p_m
        m = (a + b) / 2
        p_m = big_evaluate(p, m)
    return m

def internal_root(p, pdiff, roots_list, derivative_roots_list,
                  a, b, tolerance, bracketing):
    p_a = big_evaluate(p, a)
    p_b = big_evaluate(p, b)
    sign_at_a = sign(p_a)
    sign_at_b = sign(p_b)
    if sign_at_a * sign_at_b >= 0:
        if sign_at_a == 0:
            if a not in roots_list:
                roots_list.append(a)
            elif sign_at_b == 0:
                roots_list.append(b)
    else:
        roots_list.append(bracketing(a, b, tolerance, p, pdiff))


def external_root(p, pdiff, roots_list, derivative_roots_list,
                  extremity, limit_sign, initial_step, tolerance, bracketing):
    '''
    extremity is the smallest or largest root of pdiff.
    If initial_step < 0, this function will look for a root in interval (-inf, extremity];
    If initial_step > 0, this function will look for a root in interval (extremity, inf)
    '''

    def point_with_sign_inversion(p, extremity, sign_at_extremity, initial_step):

        step = initial_step
        x = extremity + step
        p_x = big_evaluate(p, x)
        sign_at_x = sign(p_x)

        while sign_at_x == sign_at_extremity:
            step = 2*step # Double step length
            x = x + step
            p_x = big_evaluate(p, x)
            sign_at_x = sign(p_x)

        return x

    value_at_extremity = big_evaluate(p, extremity)
    sign_at_extremity = sign(value_at_extremity)

    if limit_sign * sign_at_extremity == - 1:
        if initial_step > 0:
            a = extremity
            b = point_with_sign_inversion(p, extremity,
                                            sign_at_extremity, initial_step)
        else:
            a = point_with_sign_inversion(p, extremity,
                                            sign_at_extremity, initial_step)
            b = extremity
        root = bracketing(a, b, tolerance, p, pdiff)
        roots_list.append(root)
    elif sign_at_extremity == 0:
        roots_list.append(extremity)

def roots_from_derivative_roots(p, derivative_roots, tolerance, bracketing):
    '''
    Returns a list of roots
    '''

    roots_list = []

    n = degree(p)
    n_derivative_roots = len(derivative_roots)
    pdiff = derivative(p)

    if n_derivative_roots == 0:
        # I took 0, but any point should work
        left_extremity = ((0))
        right_extremity = ((0))
    else:
        left_extremity = derivative_roots[0]
        right_extremity = derivative_roots[-1]

    right_limit_sign = sign(p[n]) # p[n]: Leading Coefficient

    if degree(p) % 2 == 0:
        left_limit_sign = sign(p[n])
    else:
        left_limit_sign = -sign(p[n])

    external_root(p, pdiff, roots_list, derivative_roots,
                  left_extremity, left_limit_sign, (-1),
                  tolerance, bracketing)

    for i in range(n_derivative_roots - 1):
        internal_root(p, pdiff, roots_list, derivative_roots,
                      derivative_roots[i], derivative_roots[i+1],
                      tolerance, bracketing)

    external_root(p, pdiff, roots_list, derivative_roots,
                  right_extremity, right_limit_sign, (1),
                  tolerance, bracketing)

    return roots_list

def find_real_roots(p, tolerance=1.0e-15, bracketing=bisection):
    '''
     Find real roots of polynomial defined by ordered dict p
    '''
    roots_list = []

    if 0 not in p.keys() or p.keys() == [0]:
        roots_list.append((0))
        q = discard_zero_roots(p)
        p = q

    if len(p.keys()) == 2:
        n = max(p.keys())
        coef = p[0]/p[n]
        if sign(coef) == -1:
            roots_list.append((-(coef)) ** (1 / n))
        elif n % 2 == 1:
            roots_list.append(-(coef) ** (1 / n))

    else:
        roots_list += roots_from_derivative_roots(
            p, find_real_roots(derivative(p), tolerance, bracketing),
            tolerance, bracketing)

    roots_list.sort()

    return roots_list
