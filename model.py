from enum import Enum
from random import uniform

from pydantic import BaseModel, conint, confloat


class RandomType(str, Enum):
    uniform = 'uniform'
    smart = 'smart'

    def __call__(self, min_y, max_y, prev):
        randoms = {
            "uniform": uniform(min_y, max_y),
            "smart": (uniform(min_y, prev) + uniform(prev, max_y)) / 2
        }
        return randoms[self.value]


class RandomQuery(BaseModel):
    quantity: conint(ge=2) = 11
    sleep: confloat(ge=0) = 0.5
    random: RandomType = RandomType.uniform


class NumbersQuery(RandomQuery):
    min_y: float = 1
    max_y: float = 6


class PointsQuery(RandomQuery):
    min_x: float = 0
    max_x: float = 10
    min_y: float = 1
    max_y: float = 6
