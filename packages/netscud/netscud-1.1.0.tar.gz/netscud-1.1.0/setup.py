# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netscud',
 'netscud.devices',
 'netscud.devices.alcatel',
 'netscud.devices.cisco',
 'netscud.devices.mikrotik']

package_data = \
{'': ['*']}

install_requires = \
['asyncssh>=2.4.2,<3.0.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'netscud',
    'version': '1.1.0',
    'description': 'Network device Asynchronous python library',
    'long_description': '# netscud\n\nnetscud is an SSH and Telnet python library for network devices (mainly network switches and routers). It uses async techniques to speed up concurrent connections.\n\nAs an overview here is an example of netscud code for a Cisco IOS device:\n\n\n```python\n# Python library import\nimport asyncio, netscud\n\nasync def main():\n\n   # Device parameters\n   my_device = {\n      "ip": "192.168.0.16",\n      "username": "cisco",\n      "password": "cisco",\n      "device_type": "cisco_ios",\n   }\n\n   # Creation of a device\n   async with netscud.ConnectDevice(**my_device) as sw1:\n\n      # Sending command\n      output = await sw1.send_command("show interfaces description")\n\n      # Display message\n      print(output)\n\n# Main function call\nif __name__ == "__main__":\n\n   # Main async loop\n   asyncio.run(main())\n```\n\nThe result of this script is:\n\n```bat\nc:\\>script.py\nInterface              IP-Address      OK? Method Status                Protocol\nFastEthernet0/0        192.168.0.16    YES NVRAM  up                    up\nFastEthernet0/1        unassigned      YES manual up                    up\nFastEthernet1/0        unassigned      YES manual administratively down down\nFastEthernet1/1        unassigned      YES DHCP   up                    up\nEthernet2/0            unassigned      YES DHCP   up                    up\nEthernet2/1            unassigned      YES NVRAM  up                    up\nEthernet2/2            unassigned      YES NVRAM  up                    up\nEthernet2/3            unassigned      YES NVRAM  up                    up\n\nc:\\>\n```\n\nDocumentation can be found here: https://netscud.readthedocs.io/en/latest/\n',
    'author': 'ericorain',
    'author_email': 'ericorain@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ericorain/netscud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
