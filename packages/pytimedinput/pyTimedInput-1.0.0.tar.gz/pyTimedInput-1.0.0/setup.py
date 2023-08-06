# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytimedinput']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytimedinput',
    'version': '1.0.0',
    'description': 'Query a user for input with a timeout.',
    'long_description': 'pyTimedInput\n============\n\nDescription\n-----------\n\nA tiny, simplistic little alternative to the standard Python input()-function allowing you to specify a timeout for the function.\n\npyTimedInput should work on both Windows and Linux, though no exceedingly extensive testing has been done and there might be bugs.\n\nInstall\n-------\n\n.. code:: bash\n\n    $ pip3 install pyTimedInput\n\nUsage\n-----\n\n.. code:: python\n\n    def timedInput(prompt="", timeOut=5, forcedTimeout=False, endCharacters=[\'\\x1b\', \'\\n\', \'\\r\'])\n\nThe function timedInput() from pyTimedInput accepts the following parameters:\n - prompt, str: a string to show the user as a prompt when waiting for input.\n     *Defaults to an empty string.*\n - timeout: how many seconds to wait before timing out.\n     *Defaults to 5 seconds.*\n - forcedTimeout: whether to wait for \'timeout\' many seconds consecutively or simply time out regardless of user-input.\n     *Defaults to False, ie. consecutive.*\n - endCharacters[]: what characters to consider as end-of-input.\n     *Defaults to new-line, carrier-feed and ESC-key.*\n\nThe function returns a string containing whatever user entered and a boolean whether the input timed out or not.\n\n.. code:: python\n\n    from pyTimedInput import timedInput\n    userText, timedOut = timedInput("Please, do enter something: ")\n    if(timedOut):\n        print("Timed out when waiting for input.")\n        print(f"User-input so far: \'{userText}\'")\n    else:\n        print(f"User-input: \'{userText}\'")\n\nLicense\n-------\n\nMIT',
    'author': 'WereCatf',
    'author_email': 'werecatf@runbox.com',
    'maintainer': 'WereCatf',
    'maintainer_email': 'werecatf@runbox.com',
    'url': 'https://github.com/werecatf/pyTimedInput/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
