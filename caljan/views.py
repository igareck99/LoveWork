from json import dumps
from random import randint, seed
from datetime import date
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from requests import get
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from json import dumps
from .serializers import *
from .errors import *
from caljan.models import *
from .app_func import generate_session_password
from .menu import *

@api_view(['POST'])
def add_feedback(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        session_password = data.get('session_password')
        if session_password is not None:
            checked = User_guest.objects.get(session_password=session_password)
        else:
            return m400(request)
        if session_password == '':
            return m403(request)
        data.update({'user': checked.id})
        seria = FeedbackSerializer(data=data)
        if seria.is_valid():
            seria.save()
            return JsonResponse(seria.data, status=status.HTTP_201_CREATED)
        return JsonResponse(seria.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_menu(request):
    if request.method == 'GET':
        data = JSONParser().parse(request)
        food_class = data.get('food_class')
        if food_class:
            try:
                data = serializers.serialize('json',
                                             Menu.objects.filter(food_class=Food_class.objects.get(name=food_class).id))
                return HttpResponse(data, content_type='application/json')
            except ObjectDoesNotExist:
                return m400(request)
        else:
            print(type(Menu.objects.all()))
            data = serializers.serialize('json', Menu.objects.all())
            return HttpResponse(data, content_type='application/json')


@api_view(['GET'])
def get_user_info(request):
    if request.method == 'GET':
        data = JSONParser().parse(request)
        session_password = data.get('session_password')
        user = User_guest.objects.filter(session_password=session_password).first()
        if user and user.session_password != '':
            d = {'name': user.name, 'bonus_amount': user.bonus_amount,
                 'b_date': '{}.{}.{}'.format(user.b_date.day, user.b_date.month, user.b_date.month)}
            data = dumps(d)
            return HttpResponse(data, content_type='application/json')
        else:
            return m403(request)


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        telephone = data.get('telephone')
        print(telephone)
        if telephone:
            seed(54)
            code = str(randint(100000, 999999))
            sender = 'INFORM'
            url = "http://smspilot.ru/api.php?send={}&to={}&from={}&apikey={}&format=json".format(code, telephone, sender, 'dfdf')
            r = get(url)
            try:
                stat = r.json().get('send')[0].get('status')
            except TypeError:
                return sms_error(request)
            else:
                register_user = Registaration_guest(telephone=telephone, code=code)
                register_user.save()
                data = dumps({'data': 'Сообщение было успешно отправлено'})
                return HttpResponse(data, content_type="application/json")


@api_view(['POST'])
def check_code(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        telephone = data.get('telephone')
        code = data.get('code')
        user_code = Registaration_guest.objects.filter(telephone=telephone).first()
        if user_code:
            if code is not None:
                if code == user_code.code:
                    c = generate_session_password()
                    while User_guest.objects.filter(session_password=c).first() is not None:
                        c = generate_session_password()
                    user = User_guest(phone=telephone, session_password=generate_session_password(), name='Guest')
                    user.save()
                    data = dumps({'data': 'Вы успешно зарегестрированы в системе'})
                    return HttpResponse(data, content_type="application/json")
                else:
                    data = dumps({'data': 'Неверный код'})
                    return HttpResponse(data, content_type="application/json")
            else:
                return m400(request)
        else:
            data = dumps({'data': 'Пользователю с таким номером не отправлялся код'})
            return HttpResponse(data, content_type="application/json")


@api_view(['POST'])
def user_data(request):#Данные отправляются даже если не изменены
    if request.method == 'POST':
        data = JSONParser().parse(request)
        session_password = data.get('session_password')
        name = data.get('name')
        b_date = data.get('b_date')
        if name is None or session_password is None or b_date is None:
            return m400(request)
        user = User_guest.objects.filter(session_password=session_password).first()
        if user is None or user.session_password == '':
            return m403(request)
        b_date = b_date.split('-')
        a = b_date[1][1::] if b_date[1][0] == '0' else b_date[1]
        b = b_date[0][1::] if b_date[2][0] == '0' else b_date[0]
        b_date = date(int(b_date[2]), int(a), int(b))
        print(b_date)
        user.b_date = b_date
        user.name = name
        user.save()
        data = dumps({'data': 'Данные пользователя успешно сохранены'})
        return HttpResponse(data, content_type="application/json")


@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        session_password = data.get('session_password')
        if session_password is None:
            return m400(request)
        user = User_guest.objects.filter(session_password=session_password).first()
        if user is None or user.session_password == '':
            return m403(request)
        user.session_password = ''
        user.save()
        data = dumps({'data': 'Пользователь Успешно разлогинился'})
        return HttpResponse(data, content_type="application/json")


@api_view(['POST'])
def webhook_selector(request):
    data = dumps({"response": 200})
    r = request.data
    if r.get('object') == 'product':
        if r.get('action') == 'changed':
            try:
                menu_changed(r.get('object_id'))
            except Exception:
                return HttpResponse(data, content_type="application/json")
        elif r.get('action') == 'added':
            try:
                menu_added(r.get('object_id'))
            except Exception:
                return HttpResponse(data, content_type="application/json")
    return HttpResponse(data, content_type="application/json")






