import random

def generate_equation(low=0, high=5, operator='+'):
    while True:
        num1 = random.randint(low, high)
        num2 = random.randint(low, high)
        solution = {'+': num1 + num2, '-': num1 - num2, '*': num1 * num2}[operator]
        if 0 <= solution <= 9:
            return num1, num2, operator, solution