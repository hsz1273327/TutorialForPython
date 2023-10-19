# 构造用于编译的虚拟环境
python -m venv env
source env/bin/activate
python -m pip install 'mypy[mypyc]'
python -m pip install 'setuptools>=61.0.0'
python -m pip install 'wheel'

# 打包源码版本
python -m build --sdist

# 打包当前平台的编译完成版本
python -m build --wheel -n 

# 从源码安装纯python版本
python -m pip install 'dist/mymath-0.0.1rc1.tar.gz'

# 从源码根据是否环境中有mypyc来安编译版本或python版本
python -m pip install --no-build-isolation 'dist/mymath-0.0.1rc1.tar.gz'