import time
import redis

r = redis.Redis(host="127.0.0.1", port=6379, db=1)

begin = time.monotonic()
for i in range(10000):
    r.lpush("test", str(i))
end = time.monotonic()
print(end - begin)
