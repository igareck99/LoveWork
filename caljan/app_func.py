import random
import string
from datetime import date, time

def generate_session_password(length=16):
    letters = string.ascii_letters
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def reformat_date(data: str):
    try:
        data = data.split('-')
        a = data[1][1::] if data[1][0] == '0' else data[1]
        b = data[0][1::] if data[2][0] == '0' else data[0]
        return date(year=int(data[2]), month=int(a), day=int(b))
    except Exception:
        return 'Неверный формат даты'

def reformat_time(data: str):
    try:
        data = data.split(':')
        a = int(data[0][1] if data[0][0]== '0' else data[0])
        b = int(data[1][1] if data[1][0] == '0' else data[1])
        return time(hour=a, minute=b)
    except Exception:
        return 'Неверный формат времени'