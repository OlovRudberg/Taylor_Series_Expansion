import re
import math
from typing import Callable, List, Dict
import sympy as S

class TaylorSeries:
    def __init__(self, expression: S.Symbol, x: int, a: int = 0, degree: int = None):
        self.expression = str(expression)
        self.derivative = self.expression
        self.x = x
        self.a = a
        self.variable = self._find_variable()
        self.degree = self._find_degree() if degree is None else degree
        self.polynomial_coefficient_vector = []
        self.iterator = 0

        if 'e' in self.expression:
            self.expression = self.expression.replace('e', 'E')

    def _expression_type(self):
        if re.findall(r'e\*\*|cos|sin|cosinus|tan', self.expression):
            return True
        else:
            return False

    def _find_variable(self):
        if self._expression_type():
            return S.symbols('x')
        else:
            return S.symbols(
                ''.join(
                    re.findall(
                        '[a-zA-Z]', ''.join(
                            set(self.expression)
                        )
                    )
                )
            )

    def _find_degree(self):
        degree = 0
        if self._expression_type():
            '''
            If a function can be differentiated inf many times, select a number of
            iterations to ensure close approximative precision yet reasonable
            compute time. Note that for differentiating tan(x) 20 times will time out.
            '''
            degree = 15
        else:
            for degree_iterator in re.findall(r'x\*\*(\d+)', self.expression):
                degree = max(
                    int(
                        max(degree_iterator)
                    ),
                    degree
                )
        return degree

    def _compute_factorial(self, n: int):
        return 1 / math.factorial(n)

    def _evaluate_expression(self, derivative: S.Symbol, value: int):
        evaluation = S.lambdify(self.variable, derivative, "math")
        return evaluation(value)

    def _polynomial_term(self, x, a, iterator):
        return (self.x - self.a)**self.iterator

    def execute_granular_series(self) -> List[Dict]:
        while self.iterator <= self.degree:
            self.derivative = S.diff(self.derivative, self.variable)
            if self.iterator == 0:
                self.derivative = self.expression

            self.polynomial_coefficient_vector.append(
                {
                    "current_expression": self.derivative,
                    "current_derivative_iteration": self.iterator,
                    "current_evaluation_at": self.a,
                    "current_expression_valuation": self._evaluate_expression(
                        self.derivative, self.a
                    ),
                    "factorial_value": self._compute_factorial(self.iterator),
                    "polynomial_evaluation": self._polynomial_term(
                        self.x, self.a, self.iterator
                    ),
                    "total_value_evaluated": self._compute_factorial(
                        self.iterator
                    ) * self._evaluate_expression(
                        self.derivative, self.a
                    ) * (
                        self.x - self.a
                    )**self.iterator
                }
            )
            self.iterator = self.iterator + 1
        return self.polynomial_coefficient_vector

    def execute_general_series(self):
        taylor_term_value = 0
        for taylor_term in self.execute_granular_series():
            taylor_term_value += taylor_term.get('total_value_evaluated')
        return taylor_term_value


# Example usage:
taylor_series = TaylorSeries(expression='-0.5*x**5 + 3*x**2 + 2*x + 1', x=5, a=0)
# taylor_series = TaylorSeries(expression='e**x', x=5, a=0)
# taylor_series = TaylorSeries(expression='tan(x)', x=5, a=0)
