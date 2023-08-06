# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torrentdoer']

package_data = \
{'': ['*']}

install_requires = \
['ansible>=2.10.3,<3.0.0',
 'click-conf-file>=0.1.2,<0.2.0',
 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['torrentdoer = torrentdoer.entrypoint:cli']}

setup_kwargs = {
    'name': 'torrentdoer',
    'version': '0.2.0',
    'description': 'Do your torrenting from DigitalOcean.',
    'long_description': "# torrentdoer\n\nDo your torrenting from DigitalOcean!\n\nSets up a DigitalOcean droplet in your account,\nenables transmission-daemin in systemd, and opens up\nan SSH tunnel from port 9091 on your machine to the\nremote, for easy control.\n\n## Installation\n\n```\npython -m pip install torrentdoer\n```\n\n## Usage\n\nJust make sure you have an API Access Token from DigitalOcean.\nyou can either export `$DIGITALOCEAN_ACCESS_TOKEN` or else\npass the token to the `-t/--access-token` command-line option.\n\n### Start Server\n\n```bash\nexport DIGITALOCEAN_ACCESS_TOKEN='somuchsecret'\n\ntorrentdoer create\n```\n\nNow go ahead and open up a Transmission Client, pointing it to\nlocalhost:9091.\n\n### Retrieve Files\n\nThis will run rsync between the transmission daemon and your local machine.\n\n```bash\ntorrentdoer retrieve\n```\n\n### Remove The Server\n\nSave money by deleting the server when not in use.\n\n```bash\ntorrentdoer destroy\n```\n\n### Open SSH Session To Droplet\n\n\n```bash\ntorrentdoer ssh\n```\n\n### (Re-)Open SSH Tunnel\n\n\n```bash\ntorrentdoer tunnel\n```\n\nHave fun!\n",
    'author': 'Tyler Gannon',
    'author_email': 'tgannon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tylergannon/torrentdoer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
