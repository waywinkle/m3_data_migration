from suds.client import Client
import logging
from suds import WebFault
from properties import get_property
from time import sleep


FAS001_test_data = dict(W1DIVI= '100', W1ASID= '0000100001', W1FAST= '1', W1SBNO= '1',
                        FAS002=dict(WWDPMD= '1', WWBVAT= '20', WWNOMT= '141', WWSVAL= '1', WWSTPC= '1',
                                    WEDBPC= '3', WEBELZ= '0', WGDPTP= '10')

)
FAS001_wsdl = 'http://smlm3be1.synlait.local:46007/mws-ws/M3BE-M3SQL/MPD_FAS001_FAS002_Change?wsdl'


def get_available_methods(client):
    methods = [method for method in client.wsdl.services[0].ports[0].methods]
    return methods


def get_method_params(method_name, client):
    method = client.wsdl.services[0].ports[0].methods[method_name]
    params = method.binding.input.param_defs(method)
    param_names = []
    for param in params:
        param_names.append(param[0])
    return param_names


def connect(wsdl, username, password):
    c = Client(wsdl, username=username, password=password)
    c.set_options()
    return c


def call_web_service(wsdl, method, ws_data, retry=0):
    logger = logging.getLogger(__name__)
    client = connect(wsdl,
                     get_property('properties.json', 'username'),
                     get_property('properties.json', 'password'))

    ws_method = getattr(client.service, method)
    try:
        ws_method(ws_data)
    except WebFault as e:
        logger.error(e)
        logger.error('wsdl={wsdl}, method={method}, data={ws_data}'.format(wsdl=wsdl, method=method, ws_data=ws_data))
    except:
        if retry < 5:
            sleep(30)
            retry += 1
            call_web_service(wsdl, method, wsdl, retry=retry)
        else:
            logger.error('failed with 5 retries')
            logger.error(
                'wsdl={wsdl}, method={method}, data={ws_data}'.format(wsdl=wsdl, method=method, ws_data=ws_data))


if __name__ == "__main__":
    call_web_service(FAS001_wsdl, 'Change', FAS001_test_data)
    # client = connect(FAS001_wsdl,
    #                  get_property('properties.json', 'username'),
    #                  get_property('properties.json', 'password'))
    # print(client)
