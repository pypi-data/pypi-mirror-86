# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numerology']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['main = main:start_app']}

setup_kwargs = {
    'name': 'numerology',
    'version': '0.5.1',
    'description': 'Simple numerology tool to have fun with your friends.',
    'long_description': '# numerology\n\n## 1. About\n\nA simple numerology tool to have fun with friends.\nThe interpretations are not implemented yet.\n\n## 2. Installation\n\n```shell\n# Option 1: pip\npip install numerology\n\n# Option 2: Download the numerology folder on GitHub and add it to your work folder.\n```\n\n## 3. How to use it\n\n```python\n# Import\nfrom numerology import PythagoreanNumerology\n\n# Birthdate format: yyyy-mm-dd\n# Birthdate is optional to let you have a partial numerology if that information is missing.\nmy_numerology = PythagoreanNumerology("First name", "Last name", "Birthdate")\n\n# Example:\nhis_numerology = PythagoreanNumerology("Barrack", "Obama", "1961-08-04")\n```\n\nThe precedent example should print the dict below:\n\n```python\n{\n    "first_name": "Barrack",\n    "last_name": "Obama",\n    "birthdate": "1961-08-04",\n    "life_path_number": 2,\n    "life_path_number_alternative": 2,\n    "hearth_desire_number": 1,\n    "personality_number": 4,\n    "destiny_number": 5,\n    "birthdate_day_num": 4,\n    "birthdate_month_num": 8,\n    "birthdate_year_num": 8,\n    "birthdate_year_num_alternative": 7,\n    "active_number": 9,\n    "legacy_number": 5,\n    "power_number": 7,\n    "power_number_alternative": 7,\n    "full_name_numbers": {\n        "1": 4,\n        "2": 3,\n        "9": 2,\n        "3": 1,\n        "6": 1,\n        "4": 1\n    },\n    "full_name_missing_numbers": [\n        5,\n        7,\n        8\n    ]\n}\n```\n\n## 4. Future log\n\nFeatures to implement:\n\n- Vedic Numerology implementation (original code by Andrii KRAVCHUK that will be adapted for consistency with the Pythagorean Numerology)\n- Interpretations\n\n## 5. Special thanks\n\nIn the beginning, this code was a simple tool for my friends who were struggling with calculations on paper. I could not imagine it would have gone so far.\n\nA special thanks to:\n\n- Stéphane Y. for the book \'ABC de la numérologie\' by Jean-Daniel FERMIER which helped me understand the world of numerology\n- Andrii KRAVCHUK (@yakninja) for transferring his ownership of the PyPi repository to me. That makes the command `pip install numerology` possible for this code\n- Kévin YAUY (@kyauy) for letting me see all the potential of Python\n\nHave fun!\n',
    'author': 'Emmanuel GUENOU',
    'author_email': 'emmanuel@compuute.io',
    'maintainer': 'Emmanuel GUENOU',
    'maintainer_email': 'emmanuel@compuute.io',
    'url': 'https://github.com/compuuteio/numerology',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
