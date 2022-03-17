import pytest
import boto3
from src.logstack.handlers import DjangoCloudWatchHandler

def __create_dcw_handler() -> object:
    '''
    creates an dummy handler and return handler data
    '''
    dcw_handler = DjangoCloudWatchHandler(
        'info',
        'group',
        'adadas123',
        'asdadkey',
        'dhaka'
    )
    return dcw_handler

def test_django_cloud_watch_handler():
    handler = __create_dcw_handler()
    handler_data = handler.get_handler_data()
    assert handler_data['level'] == 'info'
    assert handler_data['log_group_name'] == 'group'
    assert handler_data['formatter'] == 'aws'
    assert handler_data['class'] == 'watchtower.CloudWatchLogHandler'