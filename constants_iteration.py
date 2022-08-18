import random

constants_list = []
    constants = {}
    constants['A'] = random.randint(2, 60)
    constants['b'] = random.random()
    constants['d'] = random.random()
    constants['n'] = random.randint(5, 20)
    constants['m'] = random.randint(1, constants['n'] - 1)
    constants['a'] = constants['m'] / constants['n']
    constants['g'] = random.randint(5, 20)
    constants['t'] = random.randint(5, 20)
    switcher = random.choice([True, False])
    value = random.random()
    if switcher:
        constants['u'] = value
    else:
        constants['u'] = 1 / value
    constants_list.append(constants)
