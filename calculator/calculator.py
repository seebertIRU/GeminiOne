class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
        }
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None

        tokens = expression.strip().split()
        if not tokens:
            return None

        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            print(f"Token: {token}")
            if token in self.operators:
                print(f"Operator: {token}, Values: {values}, Operators: {operators}")
                while operators and self.precedence.get(operators[-1], 0) >= self.precedence[token]:
                    self._apply_operator(values, operators)
                operators.append(token)
                print(f"After appending, Values: {values}, Operators: {operators}")
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")
            print(f"End of token, Values: {values}, Operators: {operators}")

        while operators:
            self._apply_operator(values, operators)

        return values[0]

    def _apply_operator(self, values, operators):
        operator = operators.pop()
        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))


calculator = Calculator()
expression = "3 + 7 * 2"
result = calculator.evaluate(expression)
print(result)
