# -*- coding: utf-8 -*-
# pip3 install kafka-python
from kafka.admin import KafkaAdminClient


BOOTSTRAP_SERVERS = '192.168.32.128:9092'
kafka_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)


def get_kafka_consumergroup():
    consumergrouplist = kafka_client.list_consumer_groups()
    consumer_group = []
    for group_name, consumer_flag in consumergrouplist:
        if 'consumer' in consumer_flag:
            consumer_group.append(group_name)
    print('ConsumerGroup list: {}'.format(consumer_group))
    return consumer_group


def get_consumer_client_host():
    consumer_and_topic = dict()
    group_consumer_and_topic = dict()
    consumer_host_ip = set()
    consumer_group = get_kafka_consumergroup()
    consumer_group_info = kafka_client.describe_consumer_groups(consumer_group)
    for line in consumer_group_info:
        consumer_group_name = line.group
        for consumer_member in line.members:
            topics = set()
            consumer_ip = consumer_member.client_host
            consumer_host_ip.add(consumer_member.client_host)
            for topic in consumer_member.member_metadata.subscription:
                topics.add(topic)
            if consumer_ip in consumer_and_topic.keys():
                consumer_and_topic[consumer_ip] = topics | consumer_and_topic[consumer_ip]
            else:
                consumer_and_topic[consumer_ip] = topics
        group_consumer_and_topic[consumer_group_name] = consumer_and_topic
    print('Consumer list is: {}'.format(consumer_host_ip))
    return group_consumer_and_topic, consumer_host_ip


def get_consumers_topics(consumer_dict):
    for k, v in consumer_dict.items():
        print('ConsumerGroup is: {}'.format(k))
        for k1, v1 in v.items():
            print(k1)
            for topic in v1:
                print(topic)


def main():
    get_consumers_topics(get_consumer_client_host())


if __name__ == '__main__':
    main()
