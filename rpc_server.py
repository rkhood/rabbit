import pika
from alice import get_nouns
from bcolors import bcolors


def on_request(ch, method, props, body):
    body = body.decode()
    nouns = get_nouns(str(body))
    print(bcolors.RED + 'got nouns' + bcolors.ENDC)

    ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id = props.correlation_id),
            body=' '.join(nouns))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':

    params = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='alice_nouns')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='alice_nouns', on_message_callback=on_request)

    print('Awaiting RPC request')
    channel.start_consuming()
    connection.close()
