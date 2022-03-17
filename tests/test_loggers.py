import pytest
from src.logstack.loggers import DjangoLogger
from .common_funcs import create_dcw_handler

def test_django_logger_for_aws_cloud_watch():
    dcw_handler = create_dcw_handler()
    django_logger = DjangoLogger()
    django_logger.set_cloud_watch_logger(dcw_handler)
    logging_conf = django_logger.get_logging_configuration()
    handler_data = dcw_handler.get_handler_data()
    assert logging_conf['handlers']['cloudwatch']['level'] == handler_data['level']
    assert logging_conf['handlers']['cloudwatch']['log_group_name'] == handler_data['log_group_name']
    assert logging_conf['handlers']['cloudwatch']['formatter'] == handler_data['formatter']
    assert logging_conf['handlers']['cloudwatch']['class'] == handler_data['class']

    assert logging_conf['loggers']['cloudwatch']['level'] == handler_data['level']
    assert 'cloudwatch' in logging_conf['loggers']['cloudwatch']['handlers']
    assert logging_conf['loggers']['cloudwatch']['propogate'] == False