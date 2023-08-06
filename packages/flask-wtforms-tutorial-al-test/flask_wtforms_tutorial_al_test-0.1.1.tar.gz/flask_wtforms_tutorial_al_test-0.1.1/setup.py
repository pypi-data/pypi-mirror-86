# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_wtforms_tutorial_al_test']

package_data = \
{'': ['*'], 'flask_wtforms_tutorial_al_test': ['static/css/*', 'templates/*']}

install_requires = \
['email_validator', 'flask', 'flask-wtf', 'python-dotenv']

entry_points = \
{'console_scripts': ['run = wsgi:app']}

setup_kwargs = {
    'name': 'flask-wtforms-tutorial-al-test',
    'version': '0.1.1',
    'description': 'Tutorial to implement forms in your Flask app.',
    'long_description': "# Flask-WTF Tutorial\n\n![Python](https://img.shields.io/badge/Python-v^3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)\n![Flask](https://img.shields.io/badge/Flask-v1.1.1-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)\n![Flask-WTF](https://img.shields.io/badge/Flask--WTF-v0.14.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)\n![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c&logo=GitHub)\n[![GitHub Issues](https://img.shields.io/github/issues/hackersandslackers/flask-wtform-tutorial.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/hackersandslackers/flask-wtform-tutorial/issues)\n[![GitHub Stars](https://img.shields.io/github/stars/hackersandslackers/flask-wtform-tutorial.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/hackersandslackers/flask-wtform-tutorial/stargazers)\n[![GitHub Forks](https://img.shields.io/github/forks/hackersandslackers/flask-wtform-tutorial.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/hackersandslackers/flask-wtform-tutorial/network)\n\n![Flask-WTF Tutorial](https://github.com/hackersandslackers/flask-wtform-tutorial/blob/master/.github/flask-wtforms-tutorial@2x.jpg?raw=true)\n\nSource code for the accompanying tutorial found here: https://hackersandslackers.com/flask-wtforms-forms/\n\n\n# Getting Started\n\nGet set up locally in two steps:\n\n### Environment Variables\n\nReplace the values in **.env.example** with your values and rename this file to **.env**:\n\n* `FLASK_APP`: Entry point of your application (should be `wsgi.py`).\n* `FLASK_ENV`: The environment to run your app in (either `development` or `production`).\n* `SECRET_KEY`: Randomly generated string of characters used to encrypt your app's data.\n\n*Remember never to commit secrets saved in .env files to Github.*\n\n### Installation\n\nGet up and running with `make deploy`:\n\n```shell\n$ git clone https://github.com/hackersandslackers/flask-wtform-tutorial.git\n$ cd flask-wtform-tutorial\n$ make deploy\n``` \n\n-----\n\n**Hackers and Slackers** tutorials are free of charge. If you found this tutorial helpful, a [small donation](https://www.buymeacoffee.com/hackersslackers) would be greatly appreciated to keep us in business. All proceeds go towards coffee, and all coffee goes towards more content.\n",
    'author': 'Alok Singh',
    'author_email': 'alok2k5singh@outlook.com',
    'maintainer': 'Alok Singh',
    'maintainer_email': 'alok2k5singh@outlook.com',
    'url': 'https://hackersandslackers.com/flask-wtforms-forms/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
