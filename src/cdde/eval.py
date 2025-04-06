"""
This module provides a function safe_eval(expr, variables={}, functions={}) 
that evaluates a mathematical expression safely. 
The function takes an expression expr, a dictionary of variables variables, 
and a dictionary of functions.
The function returns the result of evaluating the expression expr
using the variables and functions provided.

This module belongs to Aleksi Torhamo 
(https://stackoverflow.com/users/680727/aleksi-torhamo),
Obtained from the following stackoverflow discussion 
(https://stackoverflow.com/questions/26505420/evaluate-math-equations-from-unsafe-user-input-in-python) # pylint: disable=line-too-long
"""
import ast
import operator
from typing import Any, Callable, Dict, Union

# Dictionary of safe operations
_operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    '.': operator.concat,
    'abs': abs
}

EvalResult = Union[int, float, Any]


def safe_eval(expr: Any,
              variables: dict = {},
              functions: dict = {}) -> EvalResult:
    """
    Evaluate a mathematical expression safely.
    """
    node = ast.parse(expr, '<string>', 'eval').body
    return _safe_eval(node, variables, functions)


def _safe_eval(node: Any, variables: Dict[str, EvalResult],
               functions: Dict[str, Callable]) -> EvalResult:
    """
    Safely evaluate an AST expression.
    """
    if isinstance(node, ast.Constant):
        # Return literal values like integers, floats, strings, etc.
        return node.n

    if isinstance(node, ast.Name):
        # Get the value of a variable, or raise KeyError if not defined
        return variables[node.id]

    if isinstance(node, ast.BinOp):
        # Binary operations: addition, subtraction, multiplication, division, etc.
        op = _operations.get(node.op.__class__)
        if not op:
            raise ValueError(f"Operation not allowed: {node.op}")
        left = _safe_eval(node.left, variables, functions)
        right = _safe_eval(node.right, variables, functions)
        # Specific rules for exponents and divisions
        if isinstance(node.op, ast.Pow) and right >= 100:
            raise ValueError(
                "Exponents greater than or equal to 100 are not allowed")
        if isinstance(node.op, ast.Div) and right == 0:
            return 0
        return op(left, right)

    if isinstance(node, ast.Call):
        # Call user-defined functions or safe functions like abs
        if not isinstance(node.func, ast.Name):
            raise ValueError("Unsafe function call")
        func_name = node.func.id
        if func_name == 'abs':
            # Explicit support for abs
            if len(node.args) != 1:
                raise ValueError("abs requires exactly one argument")
            arg = _safe_eval(node.args[0], variables, functions)
            return abs(arg)
        if func_name not in functions:
            raise ValueError(f"Function not allowed: {func_name}")
        args = [_safe_eval(arg, variables, functions) for arg in node.args]
        return functions[func_name](*args)

    if isinstance(node, ast.Attribute):
        # Handle attributes (concatenation, property access)
        left = _safe_eval(node.value, variables, functions)
        result = _operations.get('.')(left, node.attr)
        return variables.get(result, result)

    raise ValueError(f"Unsafe or unsupported operation: {node}")
