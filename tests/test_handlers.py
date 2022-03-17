import pytest
from .common_funcs import create_dcw_handler


def test_django_cloud_watch_handler():
    handler = create_dcw_handler()
    handler_data = handler.get_handler_data()
    assert handler_data['level'] == 'info'
    assert handler_data['log_group_name'] == 'group'
    assert handler_data['formatter'] == 'aws'
    assert handler_data['class'] == 'watchtower.CloudWatchLogHandler'