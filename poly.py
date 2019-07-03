"""
Author: Jacob Hillock
email: jacobhillock@gmail.com

semver versioning - https://semver.org
version: v1.0.0-alpha0

This python def takes in a string of a polynomial, a given precision, and
kwargs of the expression's variables.
"""

import re
import sys
from decimal import getcontext, Decimal


def __eval(operand):
    """takes in a list that has a number, operator, then number"""
    if len(operand) != 3:
        print(f'{len(operand)} is not 3')
        sys.exit()
    a = operand[0]
    b = operand[2]
    operator = operand[1]
    if operator == '^':
        return a**b
    if operator == '*':
        return a * b
    if operator == '/':
        return a / b
    if operator == '+':
        return a + b
    if operator == '-':
        return a - b


def __large_eval(vals):
    # takes in a list that has a number, operator, then number, operatior, etc
    if len(vals) == 1:
        return vals[0]

    if '^' in vals:
        while '^' in vals:
            # finds RIGHT most *
            # the reason for right most is because you exaluate powers from
            # 'top to bottom', which is the same as left to right in this
            pos = len(vals) - vals[::-1].index('^') - 1  # position of ^
            pos -= 1  # position of number before ^

            # exponentiates the values and put it back into the vals list
            t_val = __eval(vals[pos:pos+3])
            for i in reversed(range(pos, pos+3)):
                vals.pop(i)
            vals.insert(pos, t_val)

    if '*' in vals or '/' in vals:
        while '*' in vals or '/' in vals:
            try:
                m = vals.index('*')
            except BaseException:
                m = float('inf')
            try:
                d = vals.index('/')
            except BaseException:
                d = float('inf')

            # finds left most * or /
            pos = m if m < d else d  # pos of * or /
            pos -= 1  # pos of index before

            # multiply/divide the values and put it back into the vals list
            t_val = __eval(vals[pos:pos+3])
            for i in reversed(range(pos, pos+3)):
                vals.pop(i)
            vals.insert(pos, t_val)

    # pedmas
    # this part works with the 'a' and 's' for pedmas
    if '+' in vals or '-' in vals:
        while '+' in vals or '-' in vals:
            try:
                p = vals.index('+')
            except BaseException:
                p = float('inf')
            try:
                m = vals.index('-')
            except BaseException:
                m = float('inf')

            # finds left most + or -
            pos = p if p < m else m  # pos of * or /
            pos -= 1  # pos of index before

            # add/subtract the values and put it back into the vals list
            t_val = __eval(vals[pos:pos+3])
            for i in reversed(range(pos, pos+3)):
                vals.pop(i)
            vals.insert(pos, t_val)
    return vals[0]


def poly_eval(poly, prec=16, **kwargs):
    """Polynomial Evaluation (poly_eval) is a definition that can evaluate
    a polynomial expression from a string using the standard operators (+, -,
    *, /, and ^), for roots use (1/root power). EG: sqrt = x^(1/2).

    NOTE: xy is not x*y

    poly: polynomial to evaluate in a string
    prec: precision of calculations
    kwargs is the specific to evaluate, eg. x=1, y=3.2, z=2**(1/2), etc.
    """
    # assigns precision
    getcontext().prec = prec

    # seperates out operators and numbers/variables using a regular expression
    temp = ''
    for p in poly:
        if p != ' ':
            temp += p
    poly = temp
    evals = re.split(r'[\^*/()\+-]', poly)  # vars and numbers
    eop = re.findall(r'[\^*/()\+-]', poly)  # operatirs

    # evaluates variables and string numbers to Decimal() class
    for i in range(len(evals)):
        if evals[i] != '':
            try:
                evals[i] = Decimal(str(kwargs[evals[i]]))
            except KeyError:
                try:
                    evals[i] = Decimal(evals[i])
                except BaseException as error:
                    print(f'{error} occured at {evals[i]}')
                    print('This may be due to a bad variable assignment')
                    sys.exit()
            except BaseException as error:
                print(f'{error} occured at {evals[i]}')
                sys.exit()

    # combines evals and eops to
    func = []
    i = 0
    while True:
        try:
            func.append(evals[i])
            func.append(eop[i])
            i += 1
        except BaseException:
            break
    while '' in func:
        func.remove('')

    # creates a list of paired parenthesis
    unpaired = []
    paired = []
    for i, op in enumerate(func):
        if op == '(':
            unpaired.append(i)
        if op == ')':
            paired.append([unpaired.pop(len(unpaired)-1), i])

    # evaluating the parenthesis values
    used = []
    for o, c in paired:
        if len(used) > 0:
            for u in used:
                if o > u:
                    o -= 1
                if c > u:
                    c -= 1

        # if parenthesis is only around 1 number
        if c - o - 1 == 1:
            evaled = func[o+1]

        # if parenthesis is only around 2 numbers and an operator
        elif c - o - 1 == 3:
            evaled = __eval(func[o+1:c])

        # if parenthesis is around more than 2 numbers and 1 operator
        elif c - o - 1 > 3:
            vals = func[o:c+1]
            vals.pop(0)
            vals.pop(len(vals)-1)

            evaled = __large_eval(vals)

        for i in reversed(range(o+1, c+1)):
            func.pop(i)
            used.append(i)
        func.pop(o)
        func.insert(o, evaled)

    # evaluates the rest of the operators and
    return __large_eval(func)


def main():
    poly = 'x^y^((2)- x*x^(1/2)) + y'
    print(poly_eval(poly, x=1.3, y=3))


if __name__ == '__main__':
    main()
    print('done')
