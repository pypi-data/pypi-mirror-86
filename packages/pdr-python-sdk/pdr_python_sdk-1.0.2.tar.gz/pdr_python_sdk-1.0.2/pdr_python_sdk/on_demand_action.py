import logging
import sys

from .common.logging import config_logging


class OnDemandAction(object):
    """
    One time action which process starts on new request and ends after handling it.
    """

    def on_request(self, argv=None, input_stream=sys.stdin.buffer, output_stream=sys.stdout.buffer):
        """
        method used to handle request.
        """
        raise NotImplemented('method [on_request()] is not yet implemented')


def run(clz, argv=None, input_stream=sys.stdin.buffer, output_stream=sys.stdout.buffer):
    config_logging()
    logging.info('running script using class: [' + str(clz) + ']')
    if argv is None:
        argv = sys.argv

    try:
        clz().on_request(argv, input_stream, output_stream)
    except Exception as err:
        logging.exception(err)
