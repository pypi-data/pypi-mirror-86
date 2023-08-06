# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_plugintemplate']

package_data = \
{'': ['*']}

entry_points = \
{'manim.plugins': ['manim_plugintemplate = manim_plugintemplate']}

setup_kwargs = {
    'name': 'manim-plugintemplate',
    'version': '0.1.3',
    'description': 'A template project to both illustrate and serve as an example for plugin creations on top of the manim (community edition) engine.',
    'long_description': 'Plugin Template\n===============\nThis is a template project that demonstrates how one can create and upload a manim \nplugin to PyPI using a PEP 517 compliant build system (in this case\n`poetry <https://python-poetry.org>`_). This build system ensures users of\nyour plugin are able to do so reliably without without falling into\ndependency hell. You may use another build system other than poetry (e.g.\nFlit, Enscons, etc...) if you wish to.\n\nCreating Plugins\n----------------\nPlugins are features that can be used to extend the core of Manim\'s\nfunctionality. By convention, plugins should be prefixed by ``manim-`` when\nbeing named. This allows users to easily search for plugins on organizations\nlike PyPi, but it is not required. Manim discovers user plugins via the\nmetadata specified in the ``pyproject.toml``.\n\nInstalling Poetry\n~~~~~~~~~~~~~~~~~\nPoetry can be installed on any OS that can has curl. Please visit the\nofficial poetry website for `installation instructions\n<https://python-poetry.org/docs/#installation>`_.\n\nSetting Up Your Plugin Directory Structure\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTo create a Python project suitable for poetry you may want to see the\nofficial documentation for a list of all `available commands\n<https://python-poetry.org/docs/cli/>`_. In short, if you haven\'t\nextended manim\'s functionality yet, run:\n\n.. code-block:: bash\n\n\tpoetry new --src manim-YourPluginName \n\n*Note:* ``--src`` *is both optional and recomended in order to create a src\ndirectory where all of your plugin code should live.*\n\nThis will create the following project structure:\n:: \n\n    manim-YourPluginName\n    ├── pyproject.toml\n    ├── README.rst\n    ├── src\n    │   └── manim_yourpluginname\n    │       └── __init__.py\n    └── tests\n        ├── __init__.py\n        └── test_manim_yourpluginname.py \n\nIf you have already extended manim\'s functionality, you can instead run:\n\n.. code-block:: bash\n\n    cd path/to/plugin\n    poetry init\n\nThis will prompt you for basic information regarding your plugin and help\ncreate and populate a ``pyproject.toml`` similar to the one in this template.\n\nSee the official documentation \nfor more information on the `init command <https://python-poetry.org/docs/cli/#init>`_.\n\nUpdating Pyproject.toml\n~~~~~~~~~~~~~~~~~~~~~~~\nThe ``pyproject.toml`` file is used by poetry and other build systems to\nmanage and configure your project. Manim uses the `package\'s entry\npoint metadata\n<https://packaging.python.org/guides/creating-and-discovering-plugins/#using-package-metadata>`_\nto discover available plugins. The entry point, ``"manim.plugins"``, is\n**REQUIRED** and can be `specified as\nfollows <https://python-poetry.org/docs/pyproject/#plugins>`_:\n\n.. code-block:: toml\n\n    [tool.poetry.plugins."manim.plugins"]\n    "manim_yourpluginname" = "manim_yourpluginname"\n\nThis allows Manim to discover your plugin via ``manim plugin -u``\n\nTesting Your Plugin Locally\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n.. code-block:: bash\n\n    poetry install\n\nThis command will read the ``pyproject.toml``, install the dependencies of\nyour plugin, and create a ``poetry.lock`` file to ensure everyone using your\nplugin gets the same version of dependencies. It is important that your\ndependencies are properly annotated with a version constraint (e.g.\n``manim:^0.1.1``, ``numpy:1.19.2``, etc...). Equally important to the\ndependencies specified here is that they do not conflict with manim\'s.\n\nSee the official documentation for more information on `versioning\n<https://python-poetry.org/docs/dependency-specification/>`_ or the `install\ncommand <https://python-poetry.org/docs/cli/#install>`_. \n\nUploading Your Project\n----------------------\n\nBy default, poetry is set to register the package/plugin to pypi. As soon as\nyour plugin is useful locally, run the following:\n\n.. code-block:: bash\n\n    poetry publish --build\n\nYour project should now be available on PyPI for users to install via ``pip\ninstall manim-YourPluginName`` and usable within their respective\nenvironments.\n\nSee the official documentation for more information on the `publish command\n<https://python-poetry.org/docs/cli/#publish>`_.',
    'author': 'Jason G. Villanueva',
    'author_email': 'a@jsonvillanueva.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/jsonV/manim-PluginTemplate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
