from datetime import time, date, timedelta
import os
from math import fabs
import django


def get_shedule_by_date(date_s: str,password,approved = None):
    try:
        admin = User.objects.get(password=password)
    except Exception:
        return 'Неверный пароль'
    try:
        date_s = reformat_date(date_s)
    except Exception:
        return 'Неверный формат даты'
    if approved is None:
        l = Shedule.objects.filter(visit_day__day=date_s.day, visit_day__month=date_s.month, visit_day__year=date_s.year)
        if l is not None:
            s = ''
            cnt = 1
            for x in l:
                s += '{}:\n{}\nCтол номер {}\n{}\n{}\n{}\n\n'.format(cnt, x.visit_time, x.table.id, x.guest.name, x.guest.phone, x.comment)
                cnt+=1
            print(s)
    else:
        l = Shedule.objects.filter(visit_day=date_s).filter(approved=approved)
        if l is not None:
            s = ''
            cnt = 1
            for x in l:
                s += '{}:\n{}\nCтол номер {}\n{}\n{}\n{}\n\n'.format(cnt, x.visit_time, x.table.id, x.guest.name, x.guest.phone, x.comment)
                cnt += 1
            print(s)


def approve_shedule(id_shedule):
    s = Shedule.objects.get(id=id_shedule)
    s.approved = True
    s.save()


def shedule_sign_up(session_password: str, table_id: int, date_s: str, time_s, comment=''):
    try:
        u = User_guest.objects.get(session_password=session_password)
    except Exception:
        return 'Неверный пароль'
    try:
        date_s = reformat_date(date_s)
    except Exception:
        return 'Неверный формат даты'
    time_s = reformat_time(time_s)
    if type(time_s) != time:
        return 'Неверный формат времени'
    shedule_list = Shedule.objects.filter(visit_day__day=date_s.day, visit_day__month=date_s.month, visit_day__year=date_s.year)\
                                  .filter(table_id=table_id)
    for x in shedule_list:
        if fabs(x.visit_time.hour*60 + x.visit_time.minute - (time_s.hour*60+time_s.minute)) < 120:
            return 'Это стол на это время уже занят'


    shedule = Shedule()
    shedule.guest = u
    shedule.visit_time = time_s
    shedule.visit_day = date_s
    shedule.table_id = table_id
    shedule.comment = comment
    shedule.approved = False
    shedule.save()
    return 'Вы успешно записаны. Ожидайте подтверждения брони от администратора'

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject123456789.settings')
    django.setup()
    from caljan.app_func import reformat_date, reformat_time
    from caljan.models import User_guest, User, Admin_shedule, Shedule, Tables
    #print(get_shedule_by_date('07-08-2021', 'abcdef',approved=True))
    print(shedule_sign_up('abcrt', 3, '07-08-2021', '19:14'))
