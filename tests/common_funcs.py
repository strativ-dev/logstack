from src.logstack.handlers import DjangoCloudWatchHandler

def create_dcw_handler() -> object:
    '''
    creates an dummy handler and return handler data
    '''
    dcw_handler = DjangoCloudWatchHandler(
        'info',
        'group',
        'awsID',
        'awsKEY',
        'dhaka',
    )
    return dcw_handler
