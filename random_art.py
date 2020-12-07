import random
from math import pi, sin, cos, copysign, fabs



def modsquad(m, n):
    if n == 0:
        return m
    else:
        return (m / n) % 1


def constrain(n):
    return max(min(n, 1), -1)

def create_flipper():
    value = 1

    def flipper():
        nonlocal value
        value = -1 if value == 1 else 1
        return value

    return flipper


class Expression:
    def __init__(self):
        self.randx = random.uniform(-1, 1)
        self.randy = random.uniform(-1, 1)
        self.commands = []
        self.methods = {
            "sin": {
                "weight": 10,
                "method": lambda n: sin(pi * n)
            },
            "cos": {
                "weight": 10,
                "method": lambda n: cos(pi * n)
            },
            "sintimes": {
                "arity": 2,
                "method": lambda m, n: sin(m * n * pi)
            },
            "sindiv": {
                "arity": 2,
                "method": lambda m, n: sin(m / (n or 1) * pi)
            },
            "costimes": {
                "arity": 2,
                "method": lambda m, n: cos(m * n * pi)
            },
            "cosdiv": {
                "arity": 2,
                "method": lambda m, n: cos(m / (n or 1) * pi)
            },
            "max": {
                "arity": 2,
                "method": lambda m, n: m if m > n else n
            },
            "avg": {
                "weight": 7,
                "arity": 2,
                "method": lambda m, n: (m + n) / 2
            },
            "band1": {
                "method": lambda n: round(n, 1),
                "weight": 3,
            },
            "band2": {
                "method": lambda n: round(n, 2),
                "weight": 2,
            },
            "triplethreat": {
                "method": lambda n: n * 3 % 1,
                "weight": 3
            },
            "seventhheaven": {
                "method": lambda n: n * 7 % 1,
                "weight": 3
            },
            "shiftleft": {
                "method": lambda n: (10 * n) % 1
            },
            "shiftright": {
                "method": lambda n: n / 10
            },
            "modsquad": {
                "method": modsquad,
                "arity": 2,
                "weight": 3
            },
            "sincos": {
                "method": lambda n: sin(pi * n) if n < 0 else cos(pi * n)
            },
            "cossin": {
                "method": lambda n: sin(pi * n) if n > 0 else cos(pi * n)
            },
            "sqrt": {
                "method": lambda n: copysign(pow(fabs(n), 0.5), n)
            },
            "square": {
                "method": lambda n: pow(n, 2),
                "weight": 5,
            },
            "cube": {
                "weight": 1,
                "method": lambda n: pow(n, 3)
            },
            "prod": {
                "arity": 2,
                "method": lambda m, n: m * n
            },
            "half": {
                "method": lambda n: n / 2,
                "weight": 2
            },
            "neg": {
                "method": lambda n: -n
            },
            "invert": {
                "method": lambda n: copysign((1 / n) % 1, n) if n != 0 else n
            },
            "rotate": {
                "method": lambda n: n - 1 if n > 0 else n + 1
            },
            "flipper": {
                "method": create_flipper(),
                "arity": 0
            }
        }

    def random(self):
        fns = []
        for command, info in self.methods.items():
            fns.extend([command] * info.get("weight", 1))
        fns.sort()

        values = ["x", "y", "x", "y", "xy", "randx", "randy"]
        

        def generate_commands(depth=0):
            end_chance = 1 - pow(0.85, depth)
            if random.random() < end_chance:
                return random.choice(values)
            else:
                fn = random.choice(fns)
                commands = [fn]
                for _ in range(self.methods[fn].get("arity", 1)):
                    commands.append(generate_commands(depth + 1))
                return commands

        self.commands = generate_commands()
        return self

    def evaluate(self, x, y):
        def eval_commands(commands, x, y):
            if isinstance(commands, list):
                args = [
                    eval_commands(command, x, y) for command in commands[1:]
                ]
                return self.methods[commands[0]]["method"](*args)
            elif isinstance(commands, str):
                randx = constrain(x + self.randx)
                randy = constrain(y + self.randy)
                xy = x * y
                return locals()[commands]
            else:
                return 0

        return eval_commands(self.commands, x, y)

    def __str__(self):
        def sexp(commands):
            if isinstance(commands, list):
                return "({})".format(" ".join(
                    sexp(command) for command in commands))
            else:
                return str(commands)

        return sexp(self.commands)

    def __repr__(self):
        return str(self)


def create_expression():
    
    expr = Expression().random()
    return expr


def run_expression(expr, x, y):
    
    return expr.evaluate(x, y)
