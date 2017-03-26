import logging

LOGGER = logging.getLogger(__name__)


def YYYYMMDD_to_DDMMYYYY(old_date):
    # LOGGER.debug('converting: YYYYMMDD_to_DDMMYYYY from {old_date}'.format(old_date=old_date))
    new_date = old_date[6:] + old_date[4:6] + old_date[0:4]
    return new_date


def at_least_twelve(number):
    if number < 12:
        return 12
    else:
        return number
