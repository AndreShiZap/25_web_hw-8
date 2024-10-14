from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__istartswith=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_tags(tags: str) -> list[str | None]:
    print(f"Find by {tags}")
    tag = tags.split(",")
    result = []
    for i in range(len(tag)):
        quotes = Quote.objects(tags__istartswith=tag[i].strip())
        result.append([q.quote for q in quotes])
    return result


@cache
def find_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__istartswith=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    while True:
        command = input("enter command: ").split(":")
        if command[0] == "exit":
            break
        elif command[0] == "name":
            print(find_author(command[1].strip()))
        elif command[0] == "tag":
            print(find_tag(command[1].strip()))
        elif command[0] == "tags":
            print(find_tags(command[1].strip()))
        else:
            print(f"Unknown command: {command}")
