# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sa2django']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.36.8,<0.37.0',
 'django>=3.1.1,<4.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'sqlalchemy-citext>=1.7.0,<2.0.0',
 'sqlalchemy>=1.3.19,<2.0.0']

setup_kwargs = {
    'name': 'sa2django',
    'version': '0.1.1',
    'description': 'Convert sqlalchemy database schemas to django database models at runtime.',
    'long_description': '# SqlAlchemy to Django Bridge\n\nConvert sqlalchemy database schemas to django database models at runtime.\n\nOriginal url: [https://github.com/mariushelf/sa2django](https://github.com/mariushelf/sa2django)\n\n\nThe SQLAlchemy to Django Bridge allows to specify your data models in SQLAlchemy\nand use them in Django, without manually re-specifying all your models and fields\nfor the Django ORM.\n\n\n# Why did you create this package?\n\nSpecifying a schema in SQLAlchemy and then using it in Django sounds like... counter-\nintuitive. There are a lot of *Why nots* to answer...\n\n\n## Why not specify your models in Django straight away?\n\nWe use Django to serve data that is maintained from sources outside of the Django\napplication. Those sources already specify a complete SQLAlchemy model.\n\nHence we already have a full specification of the data model in SQLAlchemy.\n\n\n## Why not simply use `inspectdb` to dynamically generate the Django model specifications?\n\n[inspectdb](https://docs.djangoproject.com/en/3.1/howto/legacy-databases/) is not\nthat dynamic after all -- it generates a Python file once, which needs to be manually\ntweaked. And each time the data model changes, you need to adjust that Python file.\n\nAlso it is often not possible to automatically derive all relations between models\nfrom the database. With third-party datasources, often relations are not manifested\nas foreign key constraints in the database schema, but just in some documentation\nthat explains the relations in human-, but not machine-readable form.\n\nOur SQLAlchemy models already contain all those relations, and it makes sense to\nconvert the SQLAlchemy models to Django ORM *at runtime*.\n\n\n# Status\n\nThe SQLAlchemy to Django Bridge works well for our use case.\n\nThere are probably a lot of corner cases and advanced (or not so advanced) features\nof SQLAlchemy that are not (yet) supported.\n\n\n# Installation\n\n`pip install sa2django`\n\n\n# Features\n\n* basic data types (int, float, string, varchar, char, date, datetime etc, bytea)\n* foreign keys and many-to-one relationships\n* many-to-many relationships including `through` tables\n* automatic inference of all declared models in a sqlalchemy `Base`\n* alternatively define your Django models as usual, but use the `SA2DModel` as\n  base class. Then all database fields are added from the corresponding sqlalchemy\n  model, but you can still add properties and functions to the Django model\n\n\n# Limitations\n\nSQLAlchemy provides a superset of Django\'s functionality. For this reason, there\'s a\nlong list of limitations.\n\nThe list is even longer and probably not exhaustive because sa2django is a young project\ntailored to its author\'s current needs.\n\n* at the moment only declarative base definitions are supported, no pure `Mapper`\n  objects\n* composite foreign keys and primary keys are not supported. Primary keys and foreign\n  keys must contain exactly one column\n  \n\n## Many to many relationships\n\n* In sqlalchemy, in the mapper of the intermediate table, both foreign keys *and*\n  relationships linking to both tables must be specified.\n  \n  Example:\n  ```python\n  class CarParentAssoc(Base):\n      __tablename__ = "cartoparent"\n      id = Column(Integer, primary_key=True)\n      car = relationship("Car")\n      parent = relationship("Parent")\n      car_id = Column(Integer, ForeignKey("car.car_id"))\n      parent_id = Column(Integer, ForeignKey("parent.id"))\n  ```\n  Note that for both links to the `car` and `parent` table, both foreign keys and\n  relationship attributes are specified.\n\n\n# Contributing\n\nPull requests are more than welcome! Ideally reach out to us by creating or replying\nto a Github ticket such that we can align our work and ideas.\n\n\n# License\n\n[MIT](LICENSE)\n\n\nAuthor: Marius Helf \n  ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n',
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariushelf/sa2django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
