import pika
import time
import uuid
from alice import get_sentences
from bcolors import bcolors


class AliceRpcClient(object):

    def __init__(self):
        params = pika.ConnectionParameters(host='localhost')
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
                exchange='',
                routing_key='alice_nouns',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id),
                body=str(n))

        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)


if __name__ == '__main__':

    sentences = get_sentences('chap1_alice.txt')
    alice_rpc = AliceRpcClient()

    for i, sentence in enumerate(sentences):
        print(bcolors.BOLD + sentence + bcolors.ENDC)
        time.sleep(2)

        response = alice_rpc.call(sentence)
        for noun in response[2:-1].split():
            print(bcolors.BLUE + str(noun) + bcolors.ENDC)
            time.sleep(1)
