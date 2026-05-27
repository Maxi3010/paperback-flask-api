
from typing import List
from flask_restx import Model

from .issue import Issue


class Newspaper(object):
# these attributes describe a newspaper - can have many issues
    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []
