import datetime

from django.shortcuts import render

from .models import Valute
from .parsing import parsing_course
from .tasks import update_or_create_valute_list


def valute_list(request):
    valute = Valute.objects.all()
    result_html = None
    print(f'Дата обновления: {valute.first().date_update.day}')
    if datetime.date.today().day - valute.first().date_update.day != 0:
        valute.delete()
        print('start worker')
        update_or_create_valute_list.delay()
    if request.method == 'POST':
        number = request.POST['input_number']
        code_in = Valute.objects.get(country_code=request.POST['select_in'])
        code_to = Valute.objects.get(country_code=request.POST['select_to'])
        result = round(int(number) * float(code_in.value) / float(code_to.value), 2)
        result_html = {'result': result, 'number': number, 'code_in': code_in, 'code_to': code_to}

    context = {
        'valute': valute,
        'today': datetime.date.today(),
        'result': result_html
    }
    return render(request, 'course_valute/valute_list.html', context)
