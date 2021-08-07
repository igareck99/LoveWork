from datetime import time, date
import os
import django

def get_shedule_by_date(date_s: str,password,approved = None):
    from caljan.models import User_guest, User, Admin_shedule, Shedule, Tables
    from caljan.app_func import reformat_date

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

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject123456789.settings')
    django.setup()
    from caljan.app_func import reformat_date
    reformat_date('07-08-2021')
    print(get_shedule_by_date('07-08-2021', 'abcdef',approved=True))
