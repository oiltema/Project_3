import datetime

from django.shortcuts import render

from .models import Valute
from .parsing import parsing_course



def valute_list(request):
    start = datetime.datetime.now()
    parsing_course(time=4)
    valute = Valute.objects.all()
    result_html = None
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
    stop = datetime.datetime.now()
    print(stop - start)
    return render(request, 'course_valute/valute_list.html', context)
