# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.9.1,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['modern-python = modern_python.console:main']}

setup_kwargs = {
    'name': 'modern-python',
    'version': '0.3.1',
    'description': '现代化的python项目模版',
    'long_description': '[![Tests](https://github.com/liuxd2018/modern-python/workflows/Tests/badge.svg)](https://github.com/liuxd2018/modern-python/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/liuxd2018/modern-python/branch/main/graph/badge.svg?token=D0H556ME01)](https://codecov.io/gh/liuxd2018/modern-python)\n[![PyPI](https://img.shields.io/pypi/v/modern-python.svg)](https://pypi.org/project/modern-python/)\n\n# modern python project\n\n## create a repository in github\n\n* gitignore\n* license\n* readme\n\n## global tools\n\n### pyenv\n\n```bash\nbrew install pyenv\n\n# modify shell\necho -e \'if command -v pyenv 1>/dev/null 2>&1; then\\n  eval "$(pyenv init -)"\\nfi\' >> ~/.bash_profile\n\n# build dependencies of python\nbrew install openssl readline sqlite3 xz zlib\n\nsource ~/.bash_profile\n```\n\n### python\n\n```bash\npyenv install 3.9.0\n\n# make python version in local directory\npyenv local 3.9.0\n```\n\n### poetry\n\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n\n1. open a new shell, initialize python project\n\n    ```bash\n    peotry init -n\n    ```\n\n2. 修改 `project.toml`\n\n3. 增加 `src`, 在其中增加 `modern_python` package\n    repository --> kebab case  `modern-python`\n    python package --> snake case `modern_python`\n\n4. `__init__.py`\n    ```python\n    # src/modern_python/__init__.py\n    __version__ = "0.1.0"\n    ```\n\n5. 创建python虚拟环境\n\n    ```bash\n    poetry install\n\n    # run python inside the new venv\n    poetry run python\n    ```\n6. 添加依赖\n\n    ```bash\n    poetry add click\n    ```\n\n## initial code\n\n在 `src/modern_python` 中创建 `console.py`\n\n在 `project.toml` 中\n\n```toml\n[tool.poetry.scripts]\nmodern-python = "modern_python.console:main"\n```\n\n```bash\n# install\npoetry install\n# run\npoetry run modern-python\n```\n\n添加 `requests`\n\n\ntest\n',
    'author': 'Liu Xiaodong',
    'author_email': 'liuxd2018@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/liuxd2018/modern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
