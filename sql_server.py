from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import text
from properties import get_property
import logging

LOGGER = logging.getLogger(__name__)


def get_engine():
    return create_engine(get_property('properties.json', 'connection_string_ss'))


def get_records(table, sort_column=None, query_filter=None):
    engine = get_engine()
    session = sessionmaker(engine)()
    meta = MetaData()
    meta.reflect(bind=engine)
    table_obj = Table(table,
                      meta,
                      autoload=True,
                      autoload_with=get_engine()
                      )

    if sort_column and query_filter:
        records = [rec._asdict() for rec in session.query(table_obj).order_by(sort_column).filter(text(query_filter))]
    elif sort_column:
        records = [rec._asdict() for rec in session.query(table_obj).order_by(sort_column)]
    elif query_filter:
        records = [rec._asdict() for rec in session.query(table_obj).filter(text(query_filter))]
    else:
        records = [rec._asdict() for rec in session.query(table_obj).all()]
    # LOGGER.debug(records)
    return records


if __name__ == "__main__":
    result = get_records('FAS001', sort_column='Fixed Asset No', query_filter="[Fixed Asset No] = '0000200925'")
    for rec in result:
        print(rec)
