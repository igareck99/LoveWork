from .keys import api_key, photo_prefix
from requests import get
from .models import Menu, Food_class,Workshop


def menu_changed(r: str):
    url = 'https://joinposter.com/api/menu.getProduct?token={}&product_id={}'.format(api_key, r)
    req = get(url).json()
    req = req.get('response')
    obj = Menu.objects.get(parent_id=str(r))
    if obj is not None:
        if req.get('category_name') is not None:
            if req.get('category_name') == 'Top screen':
                obj.food_class = Food_class.objects.get(parent_id=999)
            elif req.get('category_name') != 'Top screen':
                obj.food_class = Food_class.objects.get(name=req.get('category_name'))
            else:
                pass
        obj.name = req.get('product_name')
        obj.price = req.get('spots')[0].get('price')[:-2]
        obj.parent_id = req.get('product_id')
        if req.get('workshop') !='0':
            obj.workshop = Workshop.objects.get(id=int(req.get('workshop')))
        else:
            obj.workshop = Workshop.objects.get(workshop_name='Общий')
        if req.get('photo') is not None:
            obj.photo = photo_prefix + req.get('photo')
        obj.save()
    print('Menu Object was changed successfully')


def menu_added(r):
    url = 'https://joinposter.com/api/menu.getProduct?token={}&product_id={}'.format(api_key, r)
    req = get(url).json()
    req = req.get('response')
    obj = Menu()
    if req.get('category_name') is not None:
        if req.get('category_name') == 'Top screen':
            obj.food_class = Food_class.objects.get(parent_id=999)
        elif req.get('category_name') != 'Top screen':
            obj.food_class = Food_class.objects.get(name=req.get('category_name'))
        else:
            pass
        obj.name = req.get('product_name')
        obj.price = req.get('spots')[0].get('price')[:-2]
        obj.parent_id = req.get('product_id')
        if req.get('workshop') != '0':
            obj.workshop = Workshop.objects.get(id=int(req.get('workshop')))
        else:
            obj.workshop = Workshop.objects.get(workshop_name='Общий')
        if req.get('photo') is not None:
            obj.photo = photo_prefix + req.get('photo')
        obj.save()
    print('Menu Object was created successfully')
