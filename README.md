Flask-Swag
==========

Swagger spec extractor for flask.

It supports only python3.4 and higher.

[![PyPI version](https://badge.fury.io/py/Flask-Swag.svg)](https://badge.fury.io/py/Flask-Swag)
[![Build Status](https://travis-ci.org/Hardtack/Flask-Swag.svg?branch=master)](https://travis-ci.org/Hardtack/Flask-Swag)
[![Documentation Status](https://readthedocs.org/projects/flask-swag/badge/?version=latest)](http://flask-swag.readthedocs.org/en/latest/?badge=latest)


How to use it
-------------

Flask-Swag is a Flask extesnsion.

You can configure by

```python

from flask.ext.swag import Swag

swag = Swag(app)
```

then, Swagger-UI will be served at `/swagger/ui/`

You can add details to flask view functions.

```python

from myapp.app import app
from myapp.exts import swag

@app.route('/some-list')
@swag.mark.query('page', int)
@swag.mark.response(200, "List of somethings.", some_list_schema)
def some_list():
    pass

```

Documentation
-------------

You can find out more info at http://flask-swag.readthedocs.org/
