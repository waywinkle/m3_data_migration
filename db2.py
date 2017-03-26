from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from properties import get_property


def get_engine():
    return create_engine(get_property('properties.json', 'connection_string'))


def get_data():
    Session = sessionmaker(bind=get_engine())
    session = Session()

    return session.execute('select oacono from oohead')


if __name__ == "__main__":
    result = get_data()

    for i in result:
        print(i)
