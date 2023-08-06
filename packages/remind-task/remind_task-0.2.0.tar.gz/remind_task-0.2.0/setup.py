# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['remind_task']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'fire>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['remindtask = remind_task.remindtask:main']}

setup_kwargs = {
    'name': 'remind-task',
    'version': '0.2.0',
    'description': '',
    'long_description': '# remind_task ![pytest](https://github.com/atu4403/remind_task/workflows/pytest/badge.svg)\n\nmacosで通知を繰り返すCLIアプリケーション\n\n## Install\n\n```shell\n> pip install remind_task\n```\n\n\n## Usage\n\n```shell\n> remindtask run\n```\n\n通知はユーザー設定によりバナーもしくは通知パネルになるが設定方法はシステム環境設定 -> 通知と移動してアプリケーション一覧からスクリプトエディタを選択する。\n**停止する場合は`ctrl + c`などでプロセスを止めてください**\n\n\n## Commands\n\n### run\n---\n通知を行う。optionがない場合は1回だけ行う。\n\n#### --munute\n\nType: `int`\n\n通知を繰り返す間隔を分単位で設定する\n\n\n```shell\n> remindtask run --minute 60 # 60分ごとに通知を繰り返す\n```\n\n### edit\n---\n設定ファイルをエディタで開く。optionがない場合は規定のエディタで開く\n\n#### --app\n\nType: `str`\n\nエディタを指定する。\n\n\n```shell\n> remindtask edit --app vim\n```\n\n### init\n---\n設定ファイルを作成する。既に存在するなら何もしない\n\n#### --force\n\nType: `bool`\n\n設定ファイルがあっても強制再作成する\n\n#### --silent\n\nType: `bool`\n\nログを出力しない\n\n\n```shell\n> remindtask init --force --silent\n```\n\n\n\n## License\n\nMIT © [atu4403](https://github.com/atu4403)\n',
    'author': 'atu4403',
    'author_email': '73111778+atu4403@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atu4403/remind_task',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
