import random

def generate_equation(range=(0, 5), operator='+'):
    num1 = random.randint(*range)
    num2 = random.randint(*range)
    solution = eval(f"{num1} {operator} {num2}")
    
    return num1, num2, operator, solution