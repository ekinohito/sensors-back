from enum import Enum
from random import uniform

from pydantic import BaseModel


class RandomType(str, Enum):
    uniform = 'uniform'
    smart = 'smart'

    def __call__(self, min_y, max_y, prev):
        randoms = {
            "uniform": uniform(min_y, max_y),
            "smart": (uniform(min_y, prev) + uniform(prev, max_y)) / 2
        }
        return randoms[self.value]


class NumbersQuery(BaseModel):
    quantity: int = 11
    min_y: float = 1
    max_y: float = 6
    sleep: float = 0.5
    random: RandomType = RandomType.uniform


class PointsQuery(BaseModel):
    quantity: int = 11
    min_x: float = 0
    max_x: float = 10
    min_y: float = 1
    max_y: float = 6
    sleep: float = 0.5
    random: RandomType = RandomType.uniform
