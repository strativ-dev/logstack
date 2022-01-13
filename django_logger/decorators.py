import logging
import time
import traceback

file_error_logger = logging.getLogger('file_error_logger')
http_error_logger = logging.getLogger('http_error_logger')


def file_logger(function: function, project_name: str):
    '''
    Takes a function as argument, executes the function in a try catch block and logs the exception in error_log.log file if raise any or the function throws any.
    Also logs the successful function execution with execution time.
    Parameters:
        function -> function
        project_name -> str : Name of the project
    retunrs:
        result -> results returned from the executed function
    '''
    def wrapper(*args, **kwargs):
        result = None
        try:
            t1 = time.time()
            result = function(*args, **kwargs)
            execution_time = time.time() - t1
            file_error_logger.error(f'{str(function.__name__)}() executed successfully.', extra={'Project name': project_name,
                               'Execution duration': execution_time, 'log_type': 'Successful execution'})
        except Exception as e:
            file_error_logger.error(traceback.format_exc(), extra={'Project name': project_name,
                               'During': f'{str(function.__name__)}() execution.', 'log_type': 'Error'})
        return result

    return wrapper


def http_logger(function:function, project_name: str):
    '''
    Takes a function as argument, executes the function in a try catch block and logs the exception in remote server if raise any or the function throws any.
    Also logs the successful function execution with execution time.
    Parameters:
        function -> function
        project_name -> str : Name of the project
    retunrs:
        result -> results returned from the executed function
    '''
    def wrapper(*args, **kwargs):
        result = None
        try:
            t1 = time.time()
            result = function(*args, **kwargs)
            execution_time = time.time() - t1
            http_error_logger.error(f'{str(function.__name__)}() executed successfully.', extra={'Project name': project_name,
                               'Execution duration': execution_time, 'log_type': 'Successful execution'})
        except Exception as e:
            http_error_logger.error(traceback.format_exc(), extra={'Project name': project_name,
                               'During': f'{str(function.__name__)}() execution.', 'log_type': 'Error'})
        return result

    return wrapper
