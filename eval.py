"""
This module provides a function safe_eval(expr, variables={}, functions={}) that evaluates a mathematical expression
safely. The function takes an expression expr, a dictionary of variables variables, and a dictionary of functions.
The function returns the result of evaluating the expression expr using the variables and functions provided.

This module belongs to Aleksi Torhamo (https://stackoverflow.com/users/680727/aleksi-torhamo)
Obtained from the following stackoverflow discussion (https://stackoverflow.com/questions/26505420/evaluate-math-equations-from-unsafe-user-input-in-python)
"""
import ast
import operator


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


def safe_eval(expr, variables={}, functions={}):
    """
    Evaluate a mathematical expression safely.
    """
    node = ast.parse(expr, '<string>', 'eval').body
    return _safe_eval(node, variables, functions)


def _safe_eval(node, variables, functions):
    """
    The main function that evaluates the expression safely.
    """
    if isinstance(node, ast.Constant):
        return node.n
    elif isinstance(node, ast.Name):
        return variables[node.id]  # KeyError -> Unsafe variable
    elif isinstance(node, ast.BinOp):
        op = _operations[node.op.__class__]  # KeyError -> Unsafe operation
        left = _safe_eval(node.left, variables, functions)
        right = _safe_eval(node.right, variables, functions)
        if isinstance(node.op, ast.Pow):
            assert right < 100
        if isinstance(node.op, ast.Div):
            if right == 0:
                return 0
        return op(left, right)
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'abs':
        # Manejar la función abs
        arg = _safe_eval(node.args[0], variables, functions)
        return abs(arg)
    elif isinstance(node, ast.Call):
        assert not node.keywords and not node.starargs and not node.kwargs
        assert isinstance(node.func, ast.Name), 'Unsafe function derivation'
        func = functions[node.func.id]  # KeyError -> Unsafe function
        args = [_safe_eval(arg, variables, functions) for arg in node.args]
        return func(*args)
    elif isinstance(node, ast.Attribute):
        # Manejo del operador de concatenación (A.B)
        left = _safe_eval(node.value, variables, functions)
        right = node.attr
        result = _operations['.'](left, right)
        if result in variables:
            return variables[result]
        return result

    assert False, 'Unsafe operation'
