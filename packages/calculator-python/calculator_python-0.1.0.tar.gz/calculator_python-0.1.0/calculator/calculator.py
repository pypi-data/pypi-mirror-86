from c_19_11.calculator_python.calculator.operation import Operation


def count(string: str):
    stack = []

    for s in string.strip().split(" "):

        try:
            stack.append(float(s))
        except ValueError:
            operator = Operation(s)
            stack.append(operator.value(stack))

    return stack[-1]


def reformat(expression: str):
    stack = []
    out = ""

    for element in expression.strip().split(" "):

        try:
            float(element)
            out += element + " "
        except ValueError:
            operator = Operation(element)
            out += operator.add(stack)

    while len(stack) != 0:
        out += stack.pop() + " "
    return out


def main():
    while True:
        express = input()
        if express == "q":
            break
        reform = reformat(express)
        print(count(reform))
