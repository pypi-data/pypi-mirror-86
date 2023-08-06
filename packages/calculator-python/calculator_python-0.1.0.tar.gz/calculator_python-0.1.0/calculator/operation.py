class Operation:
    _allOperators = "-+*/^"

    def __init__(self, operator: str):
        if operator:
            self.index = self._allOperators.find(operator)
            self.operator = operator
            if self.index == -1 and "()".find(operator) == -1:
                raise Exception("The operator {} does not exist".format(operator), False)

    def value(self, polish_notation: list):
        result = 0.0
        first = 0.0
        second = 0.0

        if len(polish_notation) != 0:
            first = float(polish_notation.pop())

            if len(polish_notation) != 0:
                second = float(polish_notation.pop())

        if self.index == 0:
            result = second - first
        elif self.index == 1:
            result = first + second
        elif self.index == 2:
            result = first * second
        elif self.index == 3:

            try:
                result = second / first

            except ZeroDivisionError:
                print("Division by 0")

        elif self.index == 4:

            try:
                result = 1.0

                for i in range(abs(int(first))):
                    if first > 0:
                        result *= second

                    elif first < 0:
                        result /= second

            except ZeroDivisionError:
                result = 0.0

        return result

    def add(self, stack: list):
        out = ""
        last_symbol = -1

        if len(stack) != 0:
            last_symbol = self._allOperators.find(stack[-1])

        if self.operator == "(":
            stack.append(self.operator)

        elif self.operator == ")":
            check = True

            while check and len(stack) != 0:
                out += stack.pop() + " "

                if stack[-1] == "(":
                    check = False
                    stack.pop()

            if check:
                raise Exception(") without (")

        else:
            if self.index > -1:
                if last_symbol == -1:
                    stack.append(self.operator)

                else:

                    while len(stack) != 0:

                        if self.index > 1 and last_symbol <= 1:
                            stack.append(self.operator)
                            break

                        elif self.index > 3 and last_symbol <= 3:
                            stack.append(self.operator)
                            break

                        else:
                            out += stack.pop() + " "

                            if len(stack):
                                last_symbol = self._allOperators.find(stack[-1])

                            else:
                                stack.append(self.operator)
                                break

        return out
