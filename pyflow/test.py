"""
Simple tests for dev.

Copyright 2020 CDFMLR. All rights reserved.
Use of this source code is governed by a MIT
license that can be found in the LICENSE file.
"""

import _ast
import ast

import astunparse

from pyflow.ast_node import *
from pyflow.flowchart import *


def flowchart_translate_test(name='流程图测试'):
    st = StartNode('流程')
    op = OperationNode('操作:' + name)
    cond = ConditionNode('条件')
    io = InputOutputNode(InputOutputNode.OUTPUT, '输出')
    e = EndNode('结束')

    st.connect(op)
    op.connect(cond)
    cond.connect_yes(io)
    cond.connect_no(op)
    io.connect(e)

    fc = Flowchart(st)
    print(fc.flowchart())


def ast_unparser_test():
    expr = ''
    with open('./test.py') as f:
        expr = f.read()
    expr_ast = ast.parse(expr)
    u = astunparse.unparse(expr_ast)
    print(u)


def ast_node_test():
    expr = ''
    with open('./test.py') as f:
        expr = f.read()
    expr_ast = ast.parse(expr)
    for b in expr_ast.body:
        if isinstance(b, _ast.FunctionDef):
            st = FunctionDefStart(b)
            arg = FunctionDefArgsInput(b)
            e = FunctionDefEnd(b)

            st.connect(arg)
            arg.connect(e)

            flow = Flowchart(st).flowchart()
            print(flow)
            break


def seq_test():
    expr = """
a()
b = 1
print(c)
    """
    expr_ast = ast.parse(expr)
    p = parse(expr_ast.body)
    flow = Flowchart(p.head_node).flowchart()
    print(flow)


def loop_test():
    expr = """
start()
while a < 0:
    print('a<0')
    for i in range(10):
        ir()
    for j in range(9):
        break
print('end')
    """
    expr_ast = ast.parse(expr)
    p = parse(expr_ast.body)
    flow = Flowchart(p.head).flowchart()
    print(flow)


def if_test():
    expr = """
if a > 0:
    if b > 0:
        print('ab')
        if c > 0:
            cgz()
        else:
            clez()
            if d > 0:
                if e > 0:
                    print('777777')
    print('abc')
else:
    alez()
end_of_ifs()
    """
    expr_ast = ast.parse(expr)
    p = parse(expr_ast.body)
    flow = Flowchart(p.head).flowchart()
    print(flow)


def cond_loop_test():
    expr = """
start()
r = randint(100)
a, m, b = 0, 50, 100
while m != r:
    m = (a + b) / 2
    if m > r:
        a = m
    elif m < r:
        b = m
print(m)
end()
    """
    expr_ast = ast.parse(expr)
    p = parse(expr_ast.body)
    flow = Flowchart(p.head).flowchart()
    print(flow)


def func_test():
    expr = """
def Lagrange(points, simplify_result=True, verbose=False):
    x = Symbol('x')
    L = 0  # 插值多项式
    for i, point in enumerate(points):
        xi, yi = point
        li = 1
        for j in range(len(points)):
            if j == i:
                continue
            xj, yj = points[j]
            li *= (x - xj) / (xi - xj)
        L += yi * li
        if verbose:
            print(f"l_{i}(x) = ", simplify(yi * li))

    if simplify_result:
        L = simplify(L)
    return L
    """
#     expr = """
# def func(a, b):
#     def nested(c):
#         if c:
#             return c()
#         raise ValueError()
#     if a > b:
#         return a
#     print('b')
#     """
    expr_ast = ast.parse(expr)
    p = parse(expr_ast.body)
    flow = Flowchart(p.head).flowchart()
    print(flow)


if __name__ == '__main__':
    # flowchart_translate_test()
    # ast_unparser_test()
    # ast_node_test()
    # seq_test()
    # loop_test()
    # if_test()
    # cond_loop_test()
    func_test()