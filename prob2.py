import solver
import functions
import constants_iteration

for constants in constants_iteration.constants_list:
    poly = functions.poly2_from_constants(constants)
    tolerance = 1e-14
    roots_list = solver.find_real_roots(poly, tolerance = tolerance)
    p_list = functions.quicktest2(constants, roots_list)
    if len(p_list) != 1:
        file = open('bad_2', 'a')
        constants_rounded = {constant : round(number, 4)
                             for constant, number in constants.items()}
        file.write('constants: ' + str(constants_rounded) + '\n')
        num = 1
        for p in p_list:
            solution_full = functions.solution2_from_root(p, constants)
            solution = {parameter : round(number, 4)
                        for parameter, number in solution_full.items()}
            file.write(f'solution {num}' + str(solution) + '\n')
            num += 1
        file.close()
