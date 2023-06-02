from typing import List

import redis

from .nlp import WordCounter


class RedisClient:
    def __init__(self) -> None:
        self.client = redis.Redis(host="localhost", port=6379, db=0)

    def add_document(self, doc_name: str, sentences: List[str]):
        self.client.json().set(f"document:{doc_name}", "$", sentences)

    def read_document(self, doc_name: str) -> List[str]:
        return self.client.json().get(f"document:{doc_name}")

    def delete_document(self, doc_name: str):
        return self.client.json().delete(f"document:{doc_name}")

    def update_counter(self, other_counter: WordCounter):
        counter = self.client.json().get("counter")
        # Counter not yet added
        if counter is not None:
            word_counter = WordCounter.from_dict(counter)
            word_counter += other_counter
        else:
            word_counter = other_counter
        self.client.json().set("counter", "$", word_counter.to_dict())
