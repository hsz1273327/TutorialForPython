from setuptools import setup


try:
    from mypyc.build import mypycify
except Exception as e:
    print("没有 mypyc, model install as a pure python model")
    setup()
else:
    from mypyc.build import mypycify
    print("有 mypyc, model install as a dll model")
    setup(
        packages=['mymath'],
        ext_modules=mypycify([
            'mymath/__init__.py',
            'mymath/fib.py',
            'mymath/square_op/quadratic_sum.py',
            'mymath/square_op/square_error.py',
            'mymath/square_op/square_root.py',
            'mymath/square_op/square.py',
        ]),
    )
