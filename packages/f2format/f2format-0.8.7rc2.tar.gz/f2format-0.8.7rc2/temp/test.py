import f2format

expr = """f'{"%s"}'"""
print(expr)
print(f2format.convert(expr))
print(eval(expr))
print(eval(f2format.convert(expr)))
