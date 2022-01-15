from optparse import Option
import os
from typing import Optional

class DjangoLogger:
    
    def __init__(self, base_dir: str, host: Optional[str] = None, url: Optional[str] = None, method: Optional[str] =None) -> None:
        '''
        Takes the base directory of the project to use it as log file storage location.
        Parameters:
            base_dir -> str: base direÎctory of the project.
            host -> str (Optional): This is the url (with port if port is not 80) of remote server where the logs will be forwarded.
            url -> str (Optional but mandatory if host is provided) Url of the remote server without port.
            method -> str (Optional) Http method name in which logs will be forwarded to the remote server.
        Returns:
            None    
        '''
        self.BASE_DIR = base_dir
        self.host = host
        self.url = url
        self.method = method
        self.use_http_handler = True if self.host and self.url and self.method else False
        self._get_settings()

    def _get_settings(self) -> None:
        '''
        Performs the initial setup by invoking supporting setting methods
        Parameters:
            No parameters
        Returns:
            None    
        '''
        if not os.path.exists(f'{self.BASE_DIR}/logs'):
            os.makedirs(f'{self.BASE_DIR}/logs')
        self._handler_setting()

    def _handler_setting(self) -> None:
        '''
        Setups the handlers
        Parameters:
            No parameters
        Returns:
            None
        '''
        self.file_debug_handler_setting = {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(self.BASE_DIR, 'logs', 'debug_log.log'),
                    'formatter': 'backend'
                }
        if self.use_http_handler:
            self.http_error_handler_setting = {
                        'level': 'ERROR',
                        'class': 'logging.handlers.HTTPHandler',
                        'host': self.host,
                        'url': self.url,
                        'method': self.method
                    }
        self.file_error_handler_setting = {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(self.BASE_DIR, 'logs', 'error_log.log'),
                'formatter': 'json'
            }            
        self.console_handler_setting = {
                    'class': 'logging.StreamHandler'
                }  

    def get_logger_settings(self) -> dict:
        '''
        Returns the logger settings for django project
        Parameters:
            No Parameters
        Returns:
            CUSTOM_LOGGING -> dict
        '''
        CUSTOM_LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'backend': {
                    'format': '{asctime} {levelname} {message}',
                    'style': '{',
                },
                'json':{
                    '()': 'json_log_formatter.JSONFormatter',
                },
            },
            'filters': {
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'handlers': {
                'file_debug': self.file_debug_handler_setting,
                'file_error': self.file_error_handler_setting,
                'console': self.console_handler_setting
            },
            'loggers': {
                '': {
                    'handlers': ['file_debug'],
                    'level': 'DEBUG',
                    'propagate': False,
                },
                'file_error_logger': {
                    'handlers': ['file_error'],
                    'level': 'ERROR',
                    'propagate': False
                },
            }
        }
        if self.use_http_handler:
            CUSTOM_LOGGING['handlers']['http_error_handler'] = self.http_error_handler_setting
            CUSTOM_LOGGING['loggers']['http_error_logger'] = {
                'handlers': ['http_error_handler'],
                'level': 'ERROR',
                'propagate': False
            }
        return CUSTOM_LOGGING

# LOGGING_CONFIG = None ##uncommneting this line will make problem to write logs to file
