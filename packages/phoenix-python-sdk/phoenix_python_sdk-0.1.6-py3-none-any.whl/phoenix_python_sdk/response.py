from .exception import ServerException


def generate_success_json_data(result):
    """
        正确返回
    :param result:
    :return:
    """
    return {
        "errno": 0,
        "results": result
    }


def generate_error_json_data(errno, error_message):
    """
        失败返回
    :param error_message:
    :param errno:
    :return:
    """
    return {
        "errno": errno,
        "message": error_message
    }


def generate_retry_json_data(result={}, delay=1):
    """
        重试返回
    :param result: 返回结果
    :param delay: 等待多长时间重试
    :return:
    """
    return {
        "retry": True,
        "delay": delay,
        "errno": 0,
        "results": result
    }


def generate_next_is_multi_json_data(result=[]):
    """
        下一步是并发执行返回
    :param result:
    :return:
    """
    if isinstance(result, list):

        return {
            "errno": 0,
            "results": result
        }
    raise ServerException(code=1004)