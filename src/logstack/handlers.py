from django.conf import settings
import boto3


class DjangoCloudWatchHandler:
    def __init__(self, log_level, log_group_name) -> None:
        self.fields_config = {}
        self.log_level = log_level
        self.log_group_name = log_group_name
        if not hasattr(settings, 'LOGSTACK_SETTINGS'):
            raise Exception("LOGSTACK_SETTINGS not found in project's settings.py file")
        self.logstack_settings = settings.LOGSTACK_SETTINGS
        self.is_valid()
    
    def get_handler(self):
        logger_boto3_session = boto3.session.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )
        boto3_logs_client = boto3.client(logger_boto3_session, region_name=self.region_name)
        cloud_watch_handler = {
            'level': self.log_level,
            'class': 'watchtower.CloudWatchLogHandler',
            'log_group_name': self.log_group_name,
            'formatter': 'aws',
        }

    def _validate_and_set_values(self) -> None:
        '''
        Validates if all the fields are present as fields_config.
        then sets the fields as instance fields
        '''
        for key, value in self.fields_config.items():
            field_value_in_settings = self.logstack_settings.get(key)
            if value.get('required') and not field_value_in_settings:
                raise Exception(f"{key} is required but not given in LOGSTACK_SETTINGS")
            elif not value.get('required') and not field_value_in_settings:
                setattr(self, key, value.get('default'))
            elif field_value_in_settings:
                setattr(self, key, field_value_in_settings)
    
    def _setup_fields_config(self) -> None:
        '''
        Setups the fields_config
        '''
        self.fields_config['CLOUDWATCH_AWS_ID'] = {'required': True, 'type': str}
        self.fields_config['CLOUDWATCH_AWS_KEY'] = {'required': True, 'type': str}
        self.fields_config['AWS_DEFAULT_REGION'] = {'required': True, 'type': str}
    
    
    def is_valid(self) -> None:
        '''
        First setups the fields_config and then runs the validation
        '''
        self._setup_fields_config()
        self._validate_and_set_values()