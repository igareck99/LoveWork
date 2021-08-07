import os
import django
from requests import get


def get_categories():
    from caljan.models import Food_class
    from caljan.keys import api_key, photo_prefix
    reserv_obj = Food_class()
    reserv_obj.name = 'Главный экран'
    reserv_obj.parent_id = 999
    reserv_obj.save()
    r = get('https://joinposter.com/api/menu.getCategories?token={}'.format(api_key))
    for x in r.json().get('response'):
        food = Food_class()
        food.name = x.get('category_name')
        food.parent_id = x.get('category_id')
        if x.get('photo') is not None:
            food.category_photo = photo_prefix + x.get('photo')
        food.save()


def get_menu():
    from caljan.keys import api_key, photo_prefix
    from caljan.models import Menu, Food_class, Workshop
    r = get('https://joinposter.com/api/menu.getProducts?token={}'.format(api_key))
    for x in r.json().get('response'):
        obj = Menu()
        if x.get('category_name') is not None:
            if x.get('category_name') == 'Top screen':
                obj.food_class = Food_class.objects.get(parent_id=999)
            else:
                print(x.get('category_name'))
                obj.food_class = Food_class.objects.get(name=x.get('category_name'))
        obj.name = x.get('product_name')
        obj.price = x.get('cost')
        obj.parent_id = x.get('product_id')
        if x.get('workshop') !='0':
            obj.workshop = Workshop.objects.get(id=int(x.get('workshop')))
        else:
            obj.workshop = Workshop.objects.get(workshop_name='Общий')
        if x.get('photo') is not None:
            obj.photo = photo_prefix + x.get('photo')
        obj.save()


def get_tables():
    from caljan.keys import api_key
    from caljan.models import Tables
    r = get('https://joinposter.com/api/spots.getTableHallTables?token={}'.format(api_key))
    for x in r.json().get('response'):
        obj = Tables()
        obj.table_title = x.get('table_title')
        obj.table_num = x.get('table_num')
        obj.save()


def get_workshop():
    from caljan.keys import api_key
    from caljan.models import Workshop
    obj = Workshop()
    obj.workshop_id = 9999
    obj.workshop_name = 'Общий'
    obj.save()
    r = get('https://joinposter.com/api/menu.getWorkshops?token={}'.format(api_key))
    for x in r.json().get('response'):
        obj = Workshop()
        obj.workshop_id = id(obj)
        obj.workshop_name = x.get('workshop_name')
        obj.save()

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject123456789.settings')
    django.setup()
    get_categories()
    get_workshop()
    get_menu()
    get_tables()
