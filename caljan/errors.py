from django.http import *

def m403(request):
    return HttpResponseForbidden("<h2>403. Вы не авторизованы в системе</h2>")


def m400(request):
    return HttpResponseBadRequest("<h2>400. У вас хуево с параметрами в json</h2>")


def sms_error(request):
    return HttpResponseBadRequest("<h2>Произошла ошибка при отправке SMS</h2>")

