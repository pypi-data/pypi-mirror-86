import argparse
import sys


class Calculator:
    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--statement", type=str, help="Выражение")

        statement = parser.parse_args().statement
        statement_processor = StatementProcessor()
        tokens = list()
        for i in statement.split():
            tokens.append(Token(i))
        print(statement_processor.process(tokens))


class Token:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"token: {self.value}"

    def is_operator(self) -> bool:
        return self.value in ["+", "-", "/", "*", "^"]

    def is_left_bracket(self) -> bool:
        return self.value == "("

    def is_right_bracket(self) -> bool:
        return self.value == ")"

    def is_operand(self):
        try:
            float(self.value)
            return True
        except ValueError:
            return False

    def is_pop_needed(self, stack: "Stack") -> bool:
        if not self.is_operator():
            return False
        if stack.is_empty():
            return False
        if self.value in ["+", "-"]:
            return stack.peek().value != "("
        if self.value in ["/", "*"]:
            return stack.peek().value in ["/", "*", "^"]
        if self.value == "^":
            return stack.peek().value == "^"


class Stack:
    def __init__(self):
        self.a = list()
        self.size = 0

    def is_empty(self) -> bool:
        return self.size == 0

    def pop(self) -> Token:
        if self.is_empty():
            raise IndexError("Stack is empty, but element is asked")
        self.size -= 1
        return self.a.pop()

    def push(self, token: Token):
        self.a.append(token)
        self.size += 1

    def peek(self) -> Token:
        if self.is_empty():
            raise IndexError("Stack is empty, but element is asked")
        return self.a[self.size - 1]


class StatementProcessor:
    def process(self, tokens: list) -> float:
        return self.solve_postfix(self.infix_to_postfix(tokens))

    def infix_to_postfix(self, tokens: list) -> list:
        stack = Stack()
        ans = list()
        for i in tokens:
            if i.is_operator():
                while  i.is_pop_needed(stack):
                    ans.append(stack.pop())
                stack.push(i)
                continue
            if i.is_left_bracket():
                stack.push(i)
                continue
            if i.is_right_bracket():
                try:
                    while not (n := stack.pop()).is_left_bracket():
                        ans.append(n)
                    continue
                except IndexError:
                    raise IOError("Statement is incorrect")
            if i.is_operand:
                ans.append(i)
                continue
            raise IOError(f"Unrecognized token {i.value}")
        while not stack.is_empty():
            ans.append(stack.pop())
        return ans

    def solve_postfix(self, tokens: list) -> float:
        stack = Stack()
        for i in tokens:
            if i.is_operand():
                stack.push(i)
            if i.is_operator():
                try:

                    a = float(stack.pop().value)
                    b = float(stack.pop().value)
                    if i.value != "^":
                        stack.push(Token(eval(f"{b} {i.value} {a}")))
                    else:
                        stack.push(Token(float(b) ** float(a)))
                except IndexError as e:
                    raise IOError("Statement is incorrect")

        ans = float(stack.pop().value)
        if not stack.is_empty():
            raise IOError("Statement is incorrect")
        return ans


Calculator().main()
