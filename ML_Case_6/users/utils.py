import re
import math

from typing import Optional

PERCENT_DAYS = 3.65


def get_age(value: str) -> Optional[float]:
    numbers = re.findall('\d+', value)

    if not numbers:
        return 0.0

    years = int(numbers[0])
    days = int(numbers[1]) if len(numbers) > 1 else 0

    if days > 0:
        percent = math.ceil(days / PERCENT_DAYS)
        return years + percent / 100

    return float(years)


def get_race(value: str) -> int:
    """

    """
    if value == 'black or african American':
        return 1

    if value == 'asian':
        return 2

    if value == 'american indian or alaska native':
        return 3

    return 0
