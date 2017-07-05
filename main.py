import logging
from log_setup import setup_logging
from sql_server import get_records
from mapper import Mapper, get_maps
from soap import call_web_service

FA_FILTER = """[Fixed Asset No] = '0000200267'
AND [Sub Number] = 2
AND [Value Type] = 21
"""


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    maps = get_maps()

    for map_, values in maps.items():
        # if map_ == 'FAS003':
        logger.debug(values)
        records = get_records(values['data_source'], sort_column='Fixed Asset No')
        for rec in records:
            process_record = Mapper(rec, **values)
            logger.info(process_record.processed_data)
            call_web_service(values['wsdl'], values['method'], process_record.processed_data)


def get_processed_data(mapping):
    setup_logging(default_path='logging_.json')
    logger = logging.getLogger(__name__)
    maps = get_maps()

    records = get_records(maps[mapping]['data_source'])
    process_record = Mapper(records[0], **maps[mapping])
    logger.info(process_record.processed_data)
    logger.info(process_record.data)


def process_single_map(mapping, query_filter):
    setup_logging()
    logger = logging.getLogger(__name__)
    maps = get_maps()

    for map_, values in maps.items():
        if map_ == mapping:
            logger.debug(values)
            records = get_records(values['data_source'], query_filter=query_filter)
            for rec in records:
                        process_record = Mapper(rec, **values)
                        logger.info(process_record.processed_data)
                        call_web_service(values['wsdl'], values['method'], process_record.processed_data)


def process_single_record(query_filter):
    setup_logging()
    logger = logging.getLogger(__name__)
    maps = get_maps()

    for map_, values in maps.items():
        logger.debug(values)
        records = get_records(values['data_source'], query_filter=query_filter)
        for rec in records:
                    process_record = Mapper(rec, **values)
                    logger.info(process_record.processed_data)
                    call_web_service(values['wsdl'], values['method'], process_record.processed_data)


if __name__ == '__main__':
    # process_single_record("[Fixed Asset No] = '0000200468'")
    # process_single_map('FAS003', "")
    process_single_map('FAS003', FA_FILTER)
    # main()
