import time
from .cli import PhoenixClient
from .rabbitmq import RabbitMqService
from .const import BrokerType
import uuid
from .exception import ServerException
import logging

logger = logging.getLogger(__name__)


class Receiver(object):

    def __init__(self, app, service):
        # 调用应用
        self.app = app
        # 调用服务名称
        self.service = service

    def to_json(self):
        return {
            "receiver": {
                "app": self.app,
                "service": self.service
            }
        }


class Client(object):

    def __init__(self, api_url, app):
        """
        :param app: 当前应用名称
        :param api_url: phoenix api 地址
        """
        self.app = app
        self.api_url = api_url
        self.broker_url = None
        self.broker_type = None

    def init_config(self):
        """
            初始化配置
        :return:
        """
        logger.info("*** start init config")
        self.get_broker()

    def get_broker_address(self):
        count = 0
        while count < 3:
            if not self.broker_url:
                self.init_config()
                if self.broker_url:
                    return self.broker_url
                else:
                    count += 1
                    continue
            else:
                return self.broker_url
        raise ServerException(code=1003, traceback="broker url is none")

    def get_broker_type(self):
        count = 0
        while count < 3:
            if not self.broker_type:
                self.init_config()
                if self.broker_type:
                    return self.broker_type
                else:
                    count += 1
                    continue
            else:
                return self.broker_type
        raise ServerException(code=1003, traceback="broker type is none")

    def get_message_id(self):
        return uuid.uuid4().hex

    def get_broker(self):
        phoenix_client = PhoenixClient(endpoint=self.api_url)
        infos = phoenix_client.get_broker_info()
        logger.debug("*** get broker infos %s" % infos)
        if infos:
            info = infos[0]
            logger.debug(info)
            self.broker_url = info.get("address")
            self.broker_type = info.get("type")
        else:
            logger.debug("*** get broker infos %s" % infos)

    def send_task(self, params, receiver, callback_url="", message_id=""):
        """
            发送任务
        :param message_id:
        :param params:
        :param receiver:
        :return:
        """
        if not message_id:
            message_id = self.get_message_id()
        parameter = {
            "message_id": message_id,
            "create_timestamp": time.time(),
            "source": self.app,
            "m_type": "task",
            "callback_url": callback_url
        }

        message_data = {
            "parameter": parameter
        }
        message_data.update(receiver.to_json())
        message_data.update({"content": params})
        self.push(message_id=message_id, params=message_data)
        return message_id

    def send_workflow(self, params, workflow_name, callback_url="", message_id="", first_multi=False):
        """
            发送
        :param first_multi: 开始任务是否 同种类型任务并行
        :param message_id:
        :param params:
        :param workflow_name:
        :param callback_url:
        :return:
        """
        if not message_id:
            message_id = self.get_message_id()
        parameter = {
            "message_id": message_id,
            "create_timestamp": time.time(),
            "source": self.app,
            "callback_url": callback_url,
            "m_type": "workflow",
            "workflow_name": workflow_name,
        }
        message_data = {}
        if first_multi:
            # 初始任务并行
            if not isinstance(params, list):
                raise ServerException(code=1005)
            parameter["step_result"] = [params]
            # 首任务参数
            message_data["content"] = {"first": params}
        else:
            message_data.update({"content": params})
        message_data["parameter"] = parameter
        self.push(message_id=message_id, params=message_data)
        return message_id

    def push(self, message_id, params):
        """
            发送消息
        :param message_id:
        :param params:
        :return:
        """
        if self.get_broker_type() == BrokerType.Rabbitmq:
            RabbitMqService.push(message_id=message_id, params=params, address=self.get_broker_address())
        else:
            raise ServerException(code=1002, traceback="broker %s is not support" % self.broker_type)
