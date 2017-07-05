from logging import getLogger
import json
from properties import get_file_location
import conversions
from collections import OrderedDict

LOGGER = getLogger(__name__)


def get_maps(file='mappings.json'):
    with open(get_file_location(file)) as json_file:
        maps = json.load(json_file, object_pairs_hook=OrderedDict)

    return maps


class Mapper(object):

    def __init__(self, data, **kwargs):
        self.data = data
        for k, v in kwargs.items():
            if k == 'mapping':
                self.mapping = v
            elif k == 'constants':
                self.constants = v
            elif k == 'convert':
                self.conversions = v
        self.processed_data = self.process(self.mapping)

    def process(self, mapping):
        processed = dict()
        for key, value in mapping.items():
            LOGGER.debug('key={key}, value={value}'.format(key=key, value=value))
            if type(value) is OrderedDict:
                processed[key] = self.process(value)
            elif key in self.constants:
                processed[key] = self.constants[key]
            elif key in self.conversions and self.data.get(value, None) is not None:
                conversion_function = getattr(conversions, self.conversions[key])
                processed[key] = conversion_function(self.data[value])
            elif value != '' and self.data.get(value, None) is not None:
                processed[key] = self.data.get(value)

        processed = self.strip_white_space(processed)
        return processed

    @staticmethod
    def strip_white_space(processed):
        for key, value in processed.items():
            if type(value) is str:
                processed[key] = value.rstrip()

        return processed

