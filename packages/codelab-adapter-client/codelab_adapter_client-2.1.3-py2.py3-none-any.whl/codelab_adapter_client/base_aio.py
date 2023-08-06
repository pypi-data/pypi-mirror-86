import zmq
import zmq.asyncio
import time
import logging
import sys
import msgpack
from abc import ABCMeta, abstractmethod
from pathlib import Path
import asyncio
import argparse

from codelab_adapter_client.topic import *
# from codelab_adapter_client.topic import ADAPTER_TOPIC, SCRATCH_TOPIC, NOTIFICATION_TOPIC, EXTS_OPERATE_TOPIC
from codelab_adapter_client.utils import threaded, TokenBucket, ZMQ_LOOP_TIME
from codelab_adapter_client.session import _message_template

logger = logging.getLogger(__name__)


class MessageNodeAio(metaclass=ABCMeta):
    def __init__(
        self,
        name='',
        logger=logger,
        codelab_adapter_ip_address=None,
        subscriber_port='16103',
        publisher_port='16130',
        subscriber_list=[SCRATCH_TOPIC, NODES_OPERATE_TOPIC],
        loop_time=ZMQ_LOOP_TIME,  # todo config by user
        connect_time=0.3,
        external_message_processor=None,
        receive_loop_idle_addition=None,
        event_loop=None,
        token=None,
        bucket_token=100,
        bucket_fill_rate=100):
        '''
        :param codelab_adapter_ip_address: Adapter IP Address -
                                      default: 127.0.0.1
        :param subscriber_port: codelab_adapter subscriber port.
        :param publisher_port: codelab_adapter publisher port.
        :param loop_time: Receive loop sleep time.
        :param connect_time: Allow the node to connect to adapter
        :param token: for safety
        :param bucket_token/bucket_fill_rate: rate limit
        '''
        self.last_pub_time = time.time()
        self.bucket_token = bucket_token
        self.bucket_fill_rate = bucket_fill_rate
        self.bucket = TokenBucket(bucket_token, bucket_fill_rate)
        self._running = True  # use it to receive_loop
        self.logger = logger
        if name:
            self.name = name
        else:
            self.name = type(self).__name__
        self.token = token
        self.subscriber_list = subscriber_list
        self.receive_loop_idle_addition = receive_loop_idle_addition
        self.external_message_processor = external_message_processor
        self.connect_time = connect_time

        if codelab_adapter_ip_address:
            self.codelab_adapter_ip_address = codelab_adapter_ip_address
        else:
            # check for a running CodeLab Adapter
            # determine this computer's IP address
            self.codelab_adapter_ip_address = '127.0.0.1'

        self.subscriber_port = subscriber_port
        self.publisher_port = publisher_port
        self.loop_time = loop_time

        self.logger.info(
            '\n************************************************************')
        self.logger.info('CodeLab Adapter IP address: ' +
                         self.codelab_adapter_ip_address)
        self.logger.info('Subscriber Port = ' + self.subscriber_port)
        self.logger.info('Publisher  Port = ' + self.publisher_port)
        self.logger.info('Loop Time = ' + str(loop_time) + ' seconds')
        self.logger.info(
            '************************************************************')

        if event_loop:
            self.event_loop = event_loop
        else:
            self.event_loop = asyncio.get_event_loop()

        # 放在init 可能会有线程问题, 但如此依赖允许在消息管道建立之前，发送消息。
        # establish the zeromq sub and pub sockets and connect to the adapter
        self.context = zmq.asyncio.Context()  # zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        connect_string = "tcp://" + self.codelab_adapter_ip_address + ':' + self.subscriber_port
        self.subscriber.connect(connect_string)

        self.publisher = self.context.socket(zmq.PUB)
        connect_string = "tcp://" + self.codelab_adapter_ip_address + ':' + self.publisher_port
        self.publisher.connect(connect_string)

    def __str__(self):
        return self.name

    def get_publisher(self):
        return self.publisher

    async def set_subscriber_topic(self, topic):
        """
        This method sets a subscriber topic.
        You can subscribe to multiple topics by calling this method for
        each topic.
        :param topic: A topic string
        """

        if not type(topic) is str:
            raise TypeError('Subscriber topic must be string')
        # todo: base.py
        self.subscriber.setsockopt(zmq.SUBSCRIBE, topic.encode())

    async def pack(self, data):
        return msgpack.packb(data, use_bin_type=True)

    async def unpack(self, data):
        return msgpack.unpackb(data, raw=False)

    async def publish_payload(self, payload, topic=''):
        """
        This method will publish a  payload and its associated topic
        :param payload: Protocol message to be published
        :param topic: A string value
        """
        # self.logger.debug(f"publish_payload begin-> {time.time()}")
        # make sure the topic is a string
        if not type(topic) is str:
            raise TypeError('Publish topic must be string', 'topic')

        if self.bucket.consume(1):
            message = await self.pack(payload)

            pub_envelope = topic.encode()
            await self.publisher.send_multipart([pub_envelope, message])
        else:
            now = time.time()
            if (now - self.last_pub_time > 1):
                error_text = f"publish error, rate limit!({self.bucket_token}, {self.bucket_fill_rate})"  # 1 /s or ui
                self.logger.error(error_text)
                await self.pub_notification(error_text, type="ERROR")
                self.last_pub_time = time.time()

        # self.logger.debug(f"publish_payload end-> {time.time()}") # fast!

    async def receive_loop(self):
        """
        This is the receive loop for adapter messages.
        This method may be overwritten to meet the needs
        of the application before handling received messages.
        """

        if self.subscriber_list:
            for topic in self.subscriber_list:
                await self.set_subscriber_topic(topic)

        while self._running:
            # NOBLOCK
            try:
                data = await self.subscriber.recv_multipart(zmq.NOBLOCK)
                # data = await self.subscriber.recv_multipart()
                try:
                    # some data is invalid
                    topic = data[0].decode()
                    payload = await self.unpack(data[1])
                except Exception as e:
                    self.logger.error(str(e))
                    # todo
                await self.message_handle(topic, payload)
            except zmq.error.Again:
                await asyncio.sleep(self.loop_time)

    async def start_the_receive_loop(self):
        self.receive_loop_task = self.event_loop.create_task(
            self.receive_loop())

    async def message_handle(self, topic, payload):
        """
        Override this method with a custom adapter message processor for subscribed messages.
        :param topic: Message Topic string.
        :param payload: Message Data.
        """
        print('this method should be overwritten in the child class')

    # noinspection PyUnresolvedReferences

    async def clean_up(self):
        """
        Clean up before exiting.
        """
        self._running = False
        # print('clean_up!')
        await asyncio.sleep(0.1)
        # await self.publisher.close()
        # await self.subscriber.close()
        # await self.context.term()


class AdapterNodeAio(MessageNodeAio):
    '''
    CodeLab Adapter AdapterNodeAio
    '''
    def __init__(self,
                 start_cmd_message_id=None,
                 is_started_now=True,
                 *args,
                 **kwargs):
        '''
        :param codelab_adapter_ip_address: Adapter IP Address -
                                      default: 127.0.0.1
        :param subscriber_port: codelab_adapter subscriber port.
        :param publisher_port: codelab_adapter publisher port.
        :param loop_time: Receive loop sleep time.
        :param connect_time: Allow the node to connect to adapter
        '''
        super().__init__(*args, **kwargs)

        self.ADAPTER_TOPIC = ADAPTER_TOPIC  # message topic: the message from adapter
        self.SCRATCH_TOPIC = SCRATCH_TOPIC  # message topic: the message from scratch
        if not hasattr(self, 'TOPIC'):
            self.TOPIC = ADAPTER_TOPIC  # message topic: the message from adapter
        if not hasattr(self, 'NODE_ID'):
            self.NODE_ID = "eim"
        if not hasattr(self, 'HELP_URL'):
            self.HELP_URL = "http://adapter.codelab.club/extension_guide/introduction/"
        if not hasattr(self, 'WEIGHT'):
            self.WEIGHT = 0

        if not start_cmd_message_id:
            # node from cmd, extension from param
            parser = argparse.ArgumentParser()
            parser.add_argument("--start-cmd-message-id", dest="message_id", default=None,
                        help="start cmd message id, a number or uuid(string)")
            args = parser.parse_args()
            start_cmd_message_id = args.message_id

        self.start_cmd_message_id = start_cmd_message_id 
        self.logger.debug(f"start_cmd_message_id -> {self.start_cmd_message_id}")
        if is_started_now and self.start_cmd_message_id:
            # self.event_loop.create_task(self.started())
            pass # 放到程序中启动确认
            self.event_loop.run_until_complete(self.started())

        

    async def started(self):
        '''
        started notify
        todo await
        '''
        # request++ and uuid, Compatible with them.
        await self.pub_notification(f"{self.NODE_ID} started")
        try:
            int_message = int(self.start_cmd_message_id)
            await self.send_reply(int_message)
        except ValueError:
            # task
            await self.send_reply(self.start_cmd_message_id)
            

    async def send_reply(self, message_id, content="ok"):
        response_message = self.message_template()
        response_message["payload"]["message_id"] = message_id
        response_message["payload"]["content"] = content
        await self.publish(response_message)

    def generate_node_id(self, filename):
        '''
        extension_eim.py -> extension_eim
        '''
        node_name = Path(filename).stem
        return self._node_name_to_node_id(node_name)

    def _node_name_to_node_id(self, node_name):
        return f'eim/{node_name}'

    # def extension_message_handle(self, f):
    async def extension_message_handle(self, topic, payload):
        """
        the decorator for adding current_extension handler
        
        self.add_handler(f, type='current_extension')
        return f
        """
        self.logger.info("please set the  method to your handle method")

    async def exit_message_handle(self, topic, payload):
        await self.pub_extension_statu_change(self.NODE_ID, "stop")
        if self._running:
            stop_cmd_message_id = payload.get("message_id", None)
            await self.terminate(stop_cmd_message_id=stop_cmd_message_id)

    def message_template(self):
        # _message_template(sender,username,node_id,token) dict
        template = _message_template(self.name, self.NODE_ID, self.token)
        return template

    async def publish(self, message):
        assert isinstance(message, dict)
        topic = message.get('topic')
        payload = message.get("payload")
        if not topic:
            topic = self.TOPIC
        if not payload.get("node_id"):
            payload["node_id"] = self.NODE_ID
        # self.logger.debug(f"{self.name} publish: topic: {topic} payload:{payload}")

        await self.publish_payload(payload, topic)

    async def pub_notification(self,
                               content,
                               topic=NOTIFICATION_TOPIC,
                               type="INFO"):
        '''
        type
            ERROR
            INFO
        {
            topic: 
            payload: {
                content:
            }
        }
        '''
        node_id = self.NODE_ID
        payload = self.message_template()["payload"]
        payload["type"] = type
        payload["content"] = content
        await self.publish_payload(payload, topic)

    async def pub_extension_statu_change(self, node_name, statu):
        topic = NODE_STATU_CHANGE_TOPIC
        node_id = self.NODE_ID
        payload = self.message_template()["payload"]
        payload["node_name"] = node_name
        payload["content"] = statu
        await self.publish_payload(payload, topic)

    async def message_handle(self, topic, payload):
        """
        Override this method with a custom adapter message processor for subscribed messages.
        :param topic: Message Topic string.
        :param payload: Message Data.

        all the sub message
        process handler

        default sub: [SCRATCH_TOPIC, NODES_OPERATE_TOPIC]
        """
        if self.external_message_processor:
            # handle all sub messages
            # to handle websocket message
            await self.external_message_processor(topic, payload)

        if topic == NODES_OPERATE_TOPIC:
            '''
            分布式: 主动停止 使用node_id
                extension也是在此关闭，因为extension也是一种node
            UI触发关闭命令
            '''
            command = payload.get('content')
            if command == 'stop':
                '''
                to stop node/extension
                '''
                # 暂不处理extension
                self.logger.debug(f"node stop message: {payload}")
                self.logger.debug(f"node self.name: {self.name}")
                # payload.get("node_id") == self.NODE_ID to stop extension
                # f'eim/{payload.get("node_name")}' == self.NODE_ID to stop node (generate extension id)
                if payload.get("node_id") == self.NODE_ID or payload.get(
                        "node_id") == "all" or self._node_name_to_node_id(
                            payload.get("node_name")) == self.NODE_ID:
                    self.logger.info(f"stop {self}")
                    await self.exit_message_handle(topic, payload)
            return

        if topic in [SCRATCH_TOPIC]:
            '''
            x 接受来自scratch的消息
            v 接受所有订阅主题的消息
            插件业务类
            '''
            if payload.get("node_id") == self.NODE_ID:
                await self.extension_message_handle(topic, payload)
                '''
                handlers = self.get_handlers(type="current_extension")
                for handler in handlers:
                    handler(topic, payload)
                '''

    async def terminate(self, stop_cmd_message_id=None):
        '''
        stop by thread
        await 
        
        # await self.clean_up() # todo 同步中运行异步
        print(f"{self} terminate!")
        # self.logger.info(f"{self} terminate!")
        await self.clean_up()
        self.logger.info(f"{self} terminate!")
        '''

        if self._running:
            self.logger.info(f"stopped {self.NODE_ID}")
            await self.pub_notification(f"{self.NODE_ID} stopped")  # 会通知给 UI
            if stop_cmd_message_id:
                await self.send_reply(stop_cmd_message_id)
                await asyncio.sleep(0.1)
            # super().terminate()
            await self.clean_up()