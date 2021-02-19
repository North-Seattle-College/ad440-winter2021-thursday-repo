# Prototype of an Azure Function (running locally) that accesses 
# Azure Redis cache [nsc-redis-dev-usw2-Thursday] and GETs/SETs data from 
# that cache. (Run Redis locally using Docker)

import logging
import redis

# Azure cache for Redis local access - DEVELOP
REDIS_PORT = 6379
REDIS_HOST = '127.0.0.1'
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Azure cache for Redis access - PRODUCTION
# REDIS_PORT = 6380
# REDIS_HOST = 'nsc-redis-dev-usw2-thursday.redis.cache.windows.net'
# REDIS_KEY = ''
# cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_KEY, ssl=True)

# Get and set data from cache object
print("Ping returned : " + str(cache.ping()))
print("SET Message: " + str(cache.setex("Message01", 5, "Hello World")))
print("GET Message: " + (cache.get("Message01")).decode("utf-8"))
print("SET Message: " + str(cache.set("Message01", "Thank you for looking.")))
print("GET Message: " + (cache.get("Message01")).decode("utf-8"))
