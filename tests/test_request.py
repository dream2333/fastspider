import redis

# 连接Redis
client = redis.Redis(host="127.0.0.1", port=6379, db=0)

# 定义RedisStream名称
stream_name = "request_stream"


# 定义生产者向RedisStream中推送请求的函数
def push_request(url):
    request = {"url": url}
    client.xadd(stream_name, request, nomkstream=True)


def consume_messages():
    while True:
        messages = client.xreadgroup(
            "group1", "consumer1", {stream_name: ">"}, count=1, block=200
        )
        if not messages:
            break
        for stream, message_list in messages:
            for message in message_list:
                request = message[1]
                request_id = message[0]
                # 处理请求
                process_request(request)
                # 确认已经处理完请求
                client.xack(stream_name, "group1", request_id)


# 定义处理请求的函数
def process_request(request):
    # 处理请求
    # 如果请求失败，可以将请求重新推送到RedisStream中
    # 如果消费者下线，请求会被保留在RedisStream中，直到有新的消费者连接并处理请求
    print(request)


# 创建消费者组
try:
    client.xgroup_create(stream_name, "group1", mkstream=True)
except redis.exceptions.ResponseError:
    print("消费者组已存在")
for i in range(5):
    push_request(f"index{i}")

# result = client.xinfo_stream(stream_name,"group1")
# pprint(result)
# result = client.xinfo_groups(stream_name)
# pprint(result)
# result = client.xpending(stream_name,"group1")
# pprint(result)

# 启动消费者
consume_messages()
