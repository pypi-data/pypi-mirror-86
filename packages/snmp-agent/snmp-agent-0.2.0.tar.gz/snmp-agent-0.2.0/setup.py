# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['snmp_agent']

package_data = \
{'': ['*']}

install_requires = \
['asn1>=2.4.1,<3.0.0']

setup_kwargs = {
    'name': 'snmp-agent',
    'version': '0.2.0',
    'description': 'SNMP Server',
    'long_description': "# snmp-agent\nSNMP Server\n\n```\nimport asyncio\nimport snmp_agent\n\nasync def handler(req: snmp_agent.SNMPRequest) -> snmp_agent.SNMPResponse:\n    vbs = [\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.1.1.0', snmp_agent.OctetString('System')),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.1.3.0', snmp_agent.TimeTicks(100)),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.2.2.1.1.1', snmp_agent.Integer(1)),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.2.2.1.2.1', snmp_agent.OctetString('fxp0')),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.2.2.1.5.1', snmp_agent.Gauge32(0)),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.2.2.1.10.1', snmp_agent.Counter32(1000)),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.2.2.1.16.1', snmp_agent.Counter32(1000)),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.31.1.1.1.6.1', snmp_agent.Counter64(1000)),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.31.1.1.1.10.1', snmp_agent.Counter64(1000)),\n        snmp_agent.VariableBinding(\n            '1.3.6.1.2.1.4.20.1.1.10.0.0.1', snmp_agent.IPAddress('10.0.0.1')),\n    ]\n    res_vbs = snmp_agent.utils.handle_request(req=req, vbs=vbs)\n    res = req.create_response(res_vbs)\n    return res\n\nasync def main():\n    sv = snmp_agent.Server(handler=handler, host='0.0.0.0')\n    await sv.start()\n    while True:\n        await asyncio.sleep(3600)\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\n\n# Requirements\n- Python >= 3.8\n- asn1\n\n\n# Installation\n```\npip install snmp-agent\n```\n\n\n# License\nMIT\n",
    'author': 'kthrdei',
    'author_email': 'kthrd.tech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kthrdei/snmp-agent',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
