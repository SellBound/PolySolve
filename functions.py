def poly1_from_constants(constants):
    from dict_poly import dict_poly as dp
    for var, val in constants.items():
        globals()[var] = val
    x = dp({1 : 1})
    dict_poly = ((b ** A * x ** A - x ** ((g + 1) * A)) * (x ** (g + 1) - b) * (x ** (g + 1) - b * (1 - d) - a * b * d) * (1 - x)) - (1 - a) / A * ((b * x - x ** (g + 1)) * (x ** ((g + 1) * A) - b ** A) * (x ** (g + 1) - b * (1 - d)) * (1 - x ** A))
    return dict_poly.coef_dict

def poly2_from_constants(constants):
    from dict_poly import dict_poly as dp
    for var, val in constants.items():
        globals()[var] = val
    x =dp({1 : 1})
    dict_poly = (x ** (t * g) - d * a * b - b * (1 - d)) * (x ** (t * A) - 1) * (x ** g - 1) * (x ** (t * (g + 1)) - b) * (b ** A * x ** (g * A) - x ** (t * g * A))
    dict_poly -= (1 - a) * (x ** (t * g) - b * (1 - d)) * (x ** (g * A) - 1) * (x ** t - 1) * (x ** (t * (g + 1) * A) - b ** A) * (b * x ** (g) - x ** (t * g))
    return dict_poly.coef_dict

def solution1_from_roots(root, constants):
    for var, val in constants.items():
        globals()[var] = val
    var = ['p', 'r', 'S', 'w', 'K']
    for i in range(A):
        var.append(f'c_{i + 1}')
    for i in range(A + 1):
        var.append(f'k_{i}')
    sol = {}
    r = p ** (g + 1) / b - 1
    S = (a / (sol['r'][-1] + d)) ** (1 / (n - m))
    w = (1 - a) * sol['S'][-1] ** m
    K = sol['S'][-1] ** n
    c_1 = (sol['p'][-1] - 1) * (sol['S'][-1] ** n * sol['r'][-1] + sol['w'][-1]) / (sol['p'][-1] ** A - 1)
    k_0 = 0
    exec(f'k_{A} = 0')
    for i in range(A - 1):
        exec(f'c_{i + 2} = p * c_{i + 1}')
        exec(f'k_{i + 1} = (1 + r) * k_{i} + w * / A - c_{i + 1}')
    for variable in var:
        exec(f"sol['{variable}'] = {variable}")
    return(sol)

def solution2_from_root(p, constants):
    for var, val in constants.items():
        globals()[var] = val
    var = ['p', 'r', 'S', 'w', 'L', 'K']
    for i in range(A):
        var.append(f'c_{i + 1}')
    for i in range(A):
        var.append(f'l_{i + 1}')
    for i in range(A + 1):
        var.append(f'k_{i}')
    sol = {}
    r = p ** (g * t) / b - 1
    S = (a / (r + d)) ** (1 / (n - m))
    w = (1 - a) * S ** m
    L = (w / u) * ((p ** (t * A) - 1) / (p ** t - 1)) ** g
    L *= ((p ** (g * A) - 1) / ((p ** g - 1) * (S ** n * r + w))) ** t
    L /= p ** ((A - 1) * t * g)
    L = L ** (1 / (t + g))
    K = S ** n * L
    c_1 = (p ** g  - 1) / (p ** (g * A) - 1) * (S ** n * r + w) * L
    exec(f'l_{A} = (p ** t - 1) / (p ** (t * A) - 1) * L')
    k_0 = 0
    exec(f'k_{A} = 0')
    for i in range(A - 1):
        exec(f'c_{i + 2} = p  ** g * c_{i + 1}')
        exec(f'l_{A - 1 - i} = p ** t * l_{A - i}')
    for i in range(A - 1):
        exec(f'k_{i + 1} = (1 + r) * k_{i} + w * l_{i + 1} - c_{i + 1}')
    for variable in var:
        exec(f"sol['{variable}'] = {variable}")
    return sol

def quicktest1(constants, roots_list):
    for var, val in constants.items():
        globals()[var] = val
    p_list = []
    for p in roots_list:
        r = p ** (g + 1) / b - 1
        tetst = True
        test &= abs(r) > 1e-3
        test &= abs(1 + r - p ) > 1e-3
        test &= abs(p - 1) > 1e-6
        test &= (r + d) > 0
        test &= p > 0
        if test:
            S = (a / (r+ d)) ** (1 / (n - m))
            w = (1 - a) * S ** m
            c_1 = (p - 1) * (S ** n * r + w) / (p ** A - 1)
            if c_1 >= 0:
                p_list.append(p)
    return p_list

def quicktest2(constants, roots_list):
    for var, val in constants.items():
        globals()[var] = val
    p_list = []
    for p in roots_list:
        r = p ** (g * t) / b - 1
        test = True
        test &= abs(r) > 1e-3
        test &= abs(1 + r - p ** g) > 1e-3
        test &= abs((1 + r) * p ** t - 1) > 1e-3
        test &= abs(p - 1) > 1e-6
        test &= abs(p ** (t * g) - b * (1 - d)) > 1e-6
        test &= (r + d) > 0
        test &= p > 0
        if test:
            S = (a / (r + d)) ** (1 / (n - m))
            w = (1 - a) * S ** m
            if (S ** n * r + w) >= 0:
                p_list.append(p)
                # L = (w / u) ** (1 / t + g)
                # * ((p ** (t * A) - 1) / (p ** t - 1)) ** (g / (t +g))
                # * ((p ** (g * A) - 1) / ((p ** g - 1) * (S ** n * r + w))) ** (t / (t + g))
                # / (p ** ((A - 1) * t * g)) ** (1 / (t + g))
                # c_1 = (p ** g  - 1) / (p ** (g * A) - 1) * (S ** n * r + w) * L
                # if c_1 >= 0:
                #     p_list.append(p)
    return p_list

def testing2(constants, sol, number):
    for var,val in constants.items():
        globals()[var] = val
    for var,val in sol.items():
        globals()[var] = val[number]
    if number_is_big(p ** (t * g) - b * (1 + r)):
        print('test1')
        return False
    if number_is_big(K - S ** n * L):
        print('test2')
        return False
    if number_is_big(u * sol[f'c_{A}'][number] ** t * sol[f'l_{A}'][number] ** g - w):
        print('test3')
        return False
    if number_is_big(S ** (n - m) * (r + d) - a):
        print('test4')
        return False
    if number_is_big(w - (1 - a) * S ** m):
        print('test5')
        return False
    ksum = 0
    lsum = l_1
    if number_is_big(c_1 - w * l_1 + k_1):
        print('test6')
        return False
    for i in range(A - 1):
        ksum += sol[f'k_{i + 1}'][number]
        lsum += sol[f'l_{i + 2}'][number]
        if number_is_big(sol[f'c_{i + 2}'][number] - sol[f'k_{i + 1}'][number] * (1 + r) - w * sol[f'l_{i + 2}'][number] + sol[f'k_{i + 2}'][number]):
            print(f'iter{i}test1')
            return False
        if number_is_big(sol[f'c_{i + 2}'][number] - p ** g * sol[f'c_{i + 1}'][number]):
            print(f'iter{i}test2')
            return False
        if number_is_big(sol[f'l_{i + 1}'][number] - p ** t * sol[f'l_{i + 2}'][number]):
            print(f'iter{i}test3')
            return False
    if number_is_big(L - lsum):
        print('ltest')
        return False
    if number_is_big(K - ksum):
        print(f'ktest: {ksum}, {K}')
        return False
    return True
