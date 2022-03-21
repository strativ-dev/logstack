import pytest
from src.logstack.loggers import DjangoLogger
from .common_funcs import create_dcw_handler

def test_django_logger_for_aws_cloud_watch():
    dcw_handler = create_dcw_handler()
    django_logger = DjangoLogger()
    django_logger.set_cloud_watch_logger(
        cloud_watch_handler=dcw_handler,
        handler_name='watchlog',
        logger_name='watchlog',
    )
    logging_conf = django_logger.get_logging_configuration()
    handler_data = dcw_handler.get_handler_data()
    assert logging_conf['handlers']['watchlog']['level'] == handler_data['level']
    assert logging_conf['handlers']['watchlog']['log_group_name'] == handler_data['log_group_name']
    assert logging_conf['handlers']['watchlog']['formatter'] == handler_data['formatter']
    assert logging_conf['handlers']['watchlog']['class'] == handler_data['class']

    assert logging_conf['loggers']['watchlog']['level'] == handler_data['level']
    assert 'watchlog' in logging_conf['loggers']['watchlog']['handlers']
    assert logging_conf['loggers']['watchlog']['propogate'] == False