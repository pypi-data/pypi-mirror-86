# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohcaptcha']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0']

setup_kwargs = {
    'name': 'aiohcaptcha',
    'version': '0.1.0',
    'description': 'AsyncIO client for the hCaptcha service.',
    'long_description': '# aiohcaptcha\n\nAsyncIO client for the hCaptcha service\n\nSecure your forms using a captcha.\n\n---\n\n## Install\n    pip install aiohcaptcha\n## Usage\n### Configuration\nYou can define the secret key `HCAPTCHA_SECRET_KEY` in the environment or directly pass it to the `HCaptchaClient` model as a parameter.\n\nGet the secret and public keys from the [hcaptcha.com](https://hcaptcha.com).\n### Template\n    <div class="h-captcha" data-sitekey="your_site_key"></div>\n    <script src="https://hcaptcha.com/1/api.js" async defer></script>\n\nCheck [hCaptcha docs](https://docs.hcaptcha.com/) for more details on the HTML widget.\n### View\n    response_token = request.POST["h-captcha-response"]\n    client = HCaptchaClient(secret_key)\n    verified = await client.verify(response_token)  # a boolean\n\n### Response details\n\nResponse details are stored in `client.response`,\ndetails of the `HCaptchaResponse` model is same as the JSON response provided in the hCaptcha documentation.\n\n### Extra arguments\n\nYou can also add `remote_ip` and `sitekey` (expected key) to the `client.verify` function.\nThese parameters are explain the the [hCaptcha docs](https://docs.hcaptcha.com/).\n\n---\n\n&copy; 2020 Emin Mastizada. MIT Licenced.\n',
    'author': 'Emin Mastizada',
    'author_email': 'emin@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mastizada/aiohcaptcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
