# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ubatch']

package_data = \
{'': ['*']}

extras_require = \
{u'benchmark': ['gunicorn>=20.0,<21.0',
                'keras>=2.4,<3.0',
                'xgboost>=1.2,<2.0',
                'scikit-learn>=0.23,<0.24',
                'tensorflow>=2.3,<3.0',
                'flask-restx>=0.2,<0.3'],
 u'docs': ['sphinx_rtd_theme>=0.5,<0.6',
           'Sphinx>=3.3,<4.0',
           'sphinx-autodoc-typehints>=1.11,<2.0',
           'recommonmark>=0.6,<0.7']}

setup_kwargs = {
    'name': 'ubatch',
    'version': '0.0.3',
    'description': 'Micro batch solution for improve throughput in SIMD processes',
    'long_description': '# uBatch\n\n**uBatch** is a simple, yet elegant library for processing streams data in micro batches.\n\n**uBatch** allow to process multiple inputs data from different threads\nas a single block of data, this is useful when process data in a batches\nhas a lower cost than processing it independently, for example process data\nin GPU or take advantage from optimization of libraries written in C. Ideally,\nthe code that processes the batches should release the Python GIL for allowing\nothers threads/coroutines to run, this is true in many C libraries wrapped in\nPython.\n\n[![Documentation Status](https://readthedocs.org/projects/ubatch/badge/?version=latest)](https://ubatch.readthedocs.io/en/latest/?badge=latest)\n\nExample\n\n```python\n>>> import threading\n>>>\n>>> from typing import List\n>>> from ubatch import ubatch_decorator\n>>>\n>>>\n>>> @ubatch_decorator(max_size=5, timeout=0.01)\n... def squared(a: List[int]) -> List[int]:\n...     print(a)\n...     return [x ** 2 for x in a]\n...\n>>>\n>>> inputs = list(range(10))\n>>>\n>>> # Run squared as usual\n... _ = squared(inputs)\n[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\n>>>\n>>>\n>>> def thread_function(number: int) -> None:\n...     _ = squared.ubatch(number)\n...\n>>>\n>>> # Multiple threads squared individual inputs\n... threads = []\n>>> for i in inputs:\n...     t = threading.Thread(target=thread_function, args=(i,))\n...     threads.append(t)\n...     t.start()\n...\n[0, 1, 2, 3, 4]\n[5, 6, 7, 8, 9]\n>>> for t in threads:\n...     t.join()\n```\n\nThe example above shows 10 threads calculating the square of a number, using\n**uBatch** the threads delegate the calculation task to a single\nprocess that calculates them in batch.\n\n## Installing uBatch and Supported Versions\n\n```bash\npip install ubatch\n```\n\nuBatch officially supports Python 3.6+.\n\n## Why using uBatch\n\nWhen data is processed offline it is easy to collect data to be processed at\nsame time, the same does not happen when requests are attended online as\nexample using Flask, this is where the uBatch potential comes in.\n\n**TensorFlow** or **Scikit-learn** are just some of the libraries\nthat can take advantage of this functionality.\n\n## uBatch and application server\n\nPython application servers work like this:\n\nWhen the server is initialized multiple processes are created and each process\ncreate a bunch of threads for handling requests. Taking advantage of those\nthreads that run in parallel **uBatch** can be used to group several\ninputs and process them in a single block.\n\nLet\'s see a Flask example:\n\n```python\nimport numpy as np\n\nfrom typing import List, Dict\nfrom flask import Flask, request as flask_request\nfrom flask_restx import Resource, Api\n\nfrom ubatch import UBatch\nfrom model import load_model\n\n\napp = Flask(__name__)\napi = Api(app)\n\nmodel = load_model()\n\npredict_batch: UBatch[np.array, np.array] = UBatch(max_size=50, timeout=0.01)\npredict_batch.set_handler(handler=model.batch_predict)\npredict_batch.start()\n\n\n@api.route("/predict")\nclass Predict(Resource):\n    def post(self) -> Dict[str, List[float]]:\n        received_input = np.array(flask_request.json["input"])\n        result = predict_batch.ubatch(received_input)\n\n        return {"prediction": result.tolist()}\n```\n\nStart application server:\n\n```bash\ngunicorn -k gevent app:app\n```\n\nAnother example using **uBatch** to join multiple requests into one:\n\n```python\nimport requests\n\nfrom typing import List, Dict\nfrom flask import Flask, request as flask_request\nfrom flask_restx import Resource, Api\n\nfrom ubatch import ubatch_decorator\n\n\napp = Flask(__name__)\napi = Api(app)\n\nFAKE_TITLE_MPI_URL = "http://my_mpi_url/predict"\n\n@ubatch_decorator(max_size=100, timeout=0.03)\ndef batch_fake_title_post(titles: List[str]) -> List[bool]:\n    """Post a list of titles to MPI and return responses in a list"""\n\n    # json_post example: {"predict": ["title1", "title2", "title3"]}\n    json_post = {"predict": titles}\n\n    # response example: {"predictions": [False, True. False]}\n    response = requests.post(FAKE_TITLE_MPI_URL, json=json_post).json()\n\n    # return: [False, True, False]\n    return [x for x in response["predictions"]]\n\n@api.route("/predict")\nclass Predict(Resource):\n    def post(self) -> Dict[str, bool]:\n        # title example: "Title1"\n        title = flask_request.json["title"]\n\n        # prediction example: False\n        prediction = fake_title_batch.ubatch(title)\n\n        return {"prediction": prediction}\n```\n\nStart application server:\n\n```bash\ngunicorn -k gevent app:app\n```\n\n## Start developing uBatch\n\nInstall poetry\n\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n\nClone repository\n\n```bash\ngit clone git@github.com:mercadolibre/ubatch.git\n```\n\nStart shell and install dependencies\n\n```bash\ncd ubatch\npoetry shell\npoetry install\n```\n\nRun tests\n\n```bash\npytest\n```\n\nBuilding docs\n\n```bash\ncd ubatch/docs\npoetry shell\nmake html\n```\n\n## Licensing\n\n**uBatch** is licensed under the Apache License, Version 2.0.\nSee [LICENSE](https://github.com/mercadolibre/ubatch/blob/master/docs/LICENSE) for the full license text.\n',
    'author': 'Rodolfo E. Edelmann',
    'author_email': 'redelmann@mercadolibre.com',
    'maintainer': 'Leandro E. Colombo Vi\xc3\xb1a',
    'maintainer_email': 'leandro.colombo@mercadolibre.com',
    'url': 'https://github.com/mercadolibre/ubatch',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
