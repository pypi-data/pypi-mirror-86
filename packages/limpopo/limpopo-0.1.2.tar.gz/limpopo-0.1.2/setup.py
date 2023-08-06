# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['limpopo',
 'limpopo.services',
 'limpopo.storages',
 'limpopo.storages.postgres',
 'limpopo.storages.postgres.migrations',
 'limpopo.storages.postgres.migrations.versions']

package_data = \
{'': ['*']}

install_requires = \
['Telethon[pillow,cryptg]>=1.18.2,<2.0.0']

setup_kwargs = {
    'name': 'limpopo',
    'version': '0.1.2',
    'description': 'limpopo is a framework that allows you to create an application for conducting surveys via messengers',
    'long_description': 'Limpopo\n=======\n\n**limpopo** is a framework that allows you to create an application for conducting surveys in the following messengers:\n\n- Telegram\n\n- Viber\n\n\nInstalling\n----------\n\nInstall and update using `pip`:\n\n.. code-block:: text\n\n    pip install limpopo\n\n\nA Simple Example\n----------------\n\n.. code-block:: python\n\n    import env\n    import envparse  # External dependencies\n    import import\n    from limpopo.question import Question\n    from limpopo.services import TelegramService\n    from limpopo.storages import FakeStorage\n\n    how_are_you_question = Question(\n        topic="How are you?",\n        choices=[\n            "fine"\n        ],\n        strict_choose=False\n    )\n\n    await def quiz(dialog):\n        how_are_you_answer = await dialog.ask(how_are_you_question)\n\n        if how_are_you_answer.text != "fine":\n            await dialog.tell("Ohh")\n\n\n    def main():\n        settings = {\n            \'api_id\': env("TELEGRAM_API_ID", cast=int),\n            \'api_hash\': env("TELEGRAM_API_HASH", cast=str),\n            \'token\': env("TELEGRAM_BOT_TOKEN", cast=str)\n        }\n\n        storage = FakeStorage()\n\n        service = TelegramService(\n            quiz=quiz,\n            storage=storage,\n            settings=settings\n        )\n\n        service.run_forever()\n\nDesign\n------\n\nlimpopo provides the following entities, by which an poll-application is created:\n\n1. Service (limpopo provides `TelegramService`, `ViberService`)\n\n2. Storage (limpopo provides `PostgreStorage`, `FakeStorage`)\n\n3. Dialog\n\n4. Question\n\n\nDevelopment\n-----------\n\nHow to lint and format the code\n-------------------------------\n\nWe are using `pre-commit <https://pre-commit.com/>`_ tool,\nsee `installation guides <https://pre-commit.com/#installation>`_.\n\n.. code-block:: text\n\n    pre-commit install\n    pre-commit run -a\n',
    'author': 'limpopooooo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
