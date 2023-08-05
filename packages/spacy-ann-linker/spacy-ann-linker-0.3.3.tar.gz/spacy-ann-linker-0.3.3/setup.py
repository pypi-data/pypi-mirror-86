#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['spacy_ann', 'spacy_ann.api', 'spacy_ann.cli']

package_data = \
{'': ['*']}

install_requires = \
['nmslib == 2.0.5',
 'pydantic == 1.5',
 'scikit-learn == 0.21.3',
 'scipy >= 1.5.1, <1.6.0',
 'spacy >= 2.2.1, <3.0.0',
 'typer == 0.3.0',
 'tqdm == 4.47.0']

extras_require = \
{'api': ['fastapi', 'uvicorn', 'gunicorn', 'python-dotenv'],
 'doc': ['mkdocs', 'mkdocs-material', 'markdown-include'],
 'test': ['autoflake',
          'click-completion',
          'pytest >=4.4.0',
          'pytest-cov',
          'coverage',
          'pytest-xdist',
          'pytest-sugar',
          'mypy',
          'black',
          'isort']}

entry_points = \
{'console_scripts': ['spacy_ann = spacy_ann.cli:main'],
 'spacy_factories': ['ann_linker = spacy_ann.ann_linker:AnnLinker',
                     'remote_ann_linker = '
                     'spacy_ann.remote_ann_linker:RemoteAnnLinker'],
 'spacy_kb': ['get_candidates = spacy_ann:get_candidates']}

setup(name='spacy-ann-linker',
      version='0.3.3',
      description='spaCy ANN Linker, a pipeline component for generating spaCy KnowledgeBase Alias Candidates for Entity Linking.',
      author='Kabir Khan',
      author_email='kakh@microsoft.com',
      url='https://github.com/microsoft/spacy-ann-linker',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.6',
     )
