class dict_poly:

    def __init__(self, coef_dict):
        self.coef_dict = coef_dict
        self.degrees = sorted(list(coef_dict.keys()))[::-1]
        for i in self.degrees:
            if self.coef_dict[i] == 0:
                self.coef_dict.pop(i)

    def __repr__(self):
        return "Polynomial from dictionary " + str(self.coef_dict)

    def __eq__(self, other):
        if type(other) in [int, float]:
            if self.degrees == [0] and self.coef_dict[0] == other:
                return True
            else:
                return False
        else:
            if other.coef_dict == self.coef_dict:
                return True
            else:
                return False

    def __str__(self):
        string = ''
        for i in self.degrees:
            coef = self.coef_dict[i]
            if i != 0:
                string += f'{coef} x ^ {i} + '
            else:
                string += f'{coef}'
        if 0 not in self.degrees:
            string = string[:-2]
        return string

    def __add__(self, other):
        coef_dict = {}
        for i in self.degrees:
            coef_dict[i] = 0
            coef_dict[i] += self.coef_dict[i]
        if type(other) in [int, float]:
            if 0 not in self.degrees:
                coef_dict[0] = 0
            coef_dict[0] += other
        else:
            for i in other.degrees:
                if i not in self.degrees:
                    coef_dict[i] = 0
                coef_dict[i] += other.coef_dict[i]
        return dict_poly(coef_dict)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        coef_dict = {}
        for i in self.degrees:
            coef_dict[i] = - self.coef_dict[i]
        return dict_poly(coef_dict)

    def __sub__(self, other):
        return self + (- other)

    def __rsub__(self, other):
        return other + (- self)

    def mul_by_cxn(self, degree, coef):
        coef_dict = {}
        for i in self.degrees:
            coef_dict[i + degree] = 0
            coef_dict[i + degree] += coef * self.coef_dict[i]
        return dict_poly(coef_dict)

    def __mul__(self, other):
        if type(other) in [int, float]:
            coef_dict = {}
            for i in self.degrees:
                coef_dict[i] = 0
                coef_dict[i] += self.coef_dict[i] * other
            return dict_poly(coef_dict)

        else:
            result = dict_poly({})
            for i in other.degrees:
                result += self.mul_by_cxn(i, other.coef_dict[i])
            return result

    def __rmul__(self, other):
        return self * other

    def __pow__(self,other):
        if self == dict_poly({1:1}) and type(other) in [int, float]:
            return dict_poly({other:1})
