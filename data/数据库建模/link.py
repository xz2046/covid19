from sqlalchemy import create_engine

settings = {
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
