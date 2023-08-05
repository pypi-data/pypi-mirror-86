# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interactionviz',
 'interactionviz.cli',
 'interactionviz.cli.viewer',
 'interactionviz.maps',
 'interactionviz.tracks',
 'interactionviz.viewers',
 'interactionviz.viewers.webviewer']

package_data = \
{'': ['*'], 'interactionviz.viewers': ['static/*']}

install_requires = \
['arcade>=2.4.2,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'numpy>=1.19.2,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'websockets>=8.1,<9.0']

entry_points = \
{'console_scripts': ['interactionviz = interactionviz.cli.viewer.__main__:main']}

setup_kwargs = {
    'name': 'interactionviz',
    'version': '0.2.3',
    'description': 'Pure Python viewer / renderer / visualizer and loader for the INTERACTION dataset',
    'long_description': '# Interaction Viz.\n\nA no-nonsense, pure Python, renderer / visualizer and loader for the [INTERACTION](http://interaction-dataset.com/) dataset.\n\n![Demo](https://raw.githubusercontent.com/rosshemsley/interactionviz/master/demo/output.gif)\n\n\n## Quickstart\nIf you have Python >= 3.7.5, just use\n```\n$ pip install interactionviz\n```\n(probably it\'s best to run this inside of an activated `virtualenv` of some kind)\n\nTo view a scene, you can use\n```\n$ interactionviz --root-dir </root/of/interaction/dataset> --dataset DR_USA_Intersection_EP0 --session 1\n```\nThis will open a native 2D top-down viewer.\n\nIf you have an older version of Python, you can use `pyenv` to install a more recent version.\n\n### \xf0\x9f\xa7\xaa Experimental Feature: 3D Web viewer\nAn experimental feature is provided to support rendering the tracks in a webviewer using THREE.js.\nTo try this out, run the following command and navigate to `http://localhost:8000/viewer`.\n```\n$ interactionviz --viewer-kind web --root-dir </root/of/interaction/dataset>\n```\n\n## Using this as a library\nThe code is modular and easy to extend. Beware this is an early version and the API\nmight change unexpectedly in future versions.\n\nHere\'s an example of importing and using this viewer in your own code.\n\n```python\nfrom interactionviz.maps import load_map_xml\nfrom interactionviz.tracks import load_tracks_files\nfrom interactionviz.viewers import ArcadeViewer\n# Note: You can use the following to render in 3D in a web browser,\n#   from interactionviz.viewers import WebViewer\n\ninteraction_map = load_map_xml("<path/to/map.osm_xy>")\ntracks = load_tracks_files("<path/to/vehicle_tracks_000.csv>")\nviewer = ArcadeViewer(interaction_map, tracks)\n\nviewer.run()\n```\n',
    'author': 'Ross Hemsley',
    'author_email': 'rlhemsley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.5,<4.0.0',
}


setup(**setup_kwargs)
