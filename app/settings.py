import os
from sqlalchemy import create_engine

root_path = os.path.dirname(__file__)
settings = {
    'debug': True,
    'template_path': os.path.join(root_path, 'templates'),
    'static_path': os.path.join(root_path, 'static'),
    'dbsetting': {
        'user': 'root',
        'password': '*******',
        'hostname': 'localhost',
        'prot': 3306,
        'dbname': 'covid19'
    }
}
engine = create_engine(
    "mysql+pymysql://{user}:{password}@{hostname}:{prot}/{dbname}?charset=utf8"
    .format(**settings['dbsetting']))
