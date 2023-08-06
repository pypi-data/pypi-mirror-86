# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opoca',
 'opoca.data',
 'opoca.data.integrations',
 'opoca.evaluation',
 'opoca.features',
 'opoca.hyperparam_search',
 'opoca.models',
 'opoca.trainers']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.20,<0.30.0',
 'MonthDelta>=0.9.1,<0.10.0',
 'category_encoders>=2.2.2,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'dynaconf>=2.2.3,<3.0.0',
 'google-cloud-storage>=1.29.0,<2.0.0',
 'horology>=1.1.0,<2.0.0',
 'imbalanced-learn>=0.7.0,<0.8.0',
 'ipython>=7.16.1,<8.0.0',
 'joblib>=0.15.1,<0.16.0',
 'kubernetes>=11.0.0,<12.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'mlflow>=1.9.1,<2.0.0',
 'numpy>=1.19.0,<2.0.0',
 'optuna>=1.5.0,<2.0.0',
 'pandas-profiling>=2.8.0,<3.0.0',
 'pandas>=1.0.5,<2.0.0',
 'plotly>=4.8.1,<5.0.0',
 'pyarrow>=0.17.1,<0.18.0',
 'python-dateutil==2.8.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'quilt3>=3.1.14,<4.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scikit-optimize>=0.7.4,<0.8.0',
 'scipy>=1.5.0,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'simple-salesforce>=1.1.0,<2.0.0',
 'tqdm>=4.46.1,<5.0.0',
 'urllib3==1.24.3',
 'xgboost>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'opoca',
    'version': '0.1.1',
    'description': 'Opoca library aims to drastically speed up producing proof of concepts (PoC) for machine learning projects.',
    'long_description': "# Opoca\n\nOpoca library aims to drastically speed up producing proof of concepts (PoC) for machine learning projects. \n\nWe define proof of concept as a small, quick and (not) dirty projects that results in:\n- exploratory data analysis\n- log of experiments along with models\n- deployable best model\n- demo (jupyter notebook/streamlit app etc.)\n- short report including results analysis\n\nThere are several challenges that ML Engineer faces given a task to build new PoC project:\n* it's not easy to track and reproduce experiments\n* it's not easy to version and share data\n* it's not easy to schedule jobs and not burn much money on training\n* there's a lot of code that can be reused between different PoCs such as:\n    * training logic for similar problems\n    * evaluation logic\n    * plotting\n    * hyperparameters search\n    * generic feature engineering transformations\n    \nThose are just few and a list is not complete without a doubt.\n\n## Prerequisites\n\nBefore you begin, ensure you have met the following requirements:\n* You have installed the latest version of [poetry](https://github.com/python-poetry/poetry)\n\n## Installing Opoca\n\nOpoca is installable from PyPi by executing:\n\n```shell script\npip install opoca\n```\n\nOne may also use docker to build image:\n\n```shell script\ndocker build -t opoca -f Dockerfile .\n```\n\nAnd run bash session interactively by executing:\n\n```shell script\ndocker run -it --rm -v $PWD:/home -w /home opoca bash\n```\n\n## Contributing to Opoca\n<!--- If your README is long or you have some specific process or steps you want contributors to follow, consider creating a separate CONTRIBUTING.md file--->\nTo contribute to `Opoca`, follow these steps:\n\n1. Fork this repository.\n2. Create a branch: `git checkout -b <branch_name>`.\n3. Make your changes and commit them: `git commit -m '<commit_message>'`\n4. Push to the original branch: `git push origin <project_name>/<location>`\n5. Create the pull request.\n\nAlternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).\n\n## Contributors\n\nThanks to the following people who have contributed to this project:\n* [@plazowicz](https://github.com/plazowicz)\n* [@pedrito87](https://github.com/pedrito87)\n* [@mjmikulski](https://github.com/mjmikulski)\n* [@AdrianMaciej](https://github.com/AdrianMaciej)\n* [@dkosowski87](https://github.com/dkosowski87)\n\n## Contact\n\nIf you want to contact me you can reach me at <ml-team@netguru.com>.\n\n## License\n\nThis project uses the following license: [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n",
    'author': 'Apollo Team',
    'author_email': 'ml-team@netguru.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
