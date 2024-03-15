import datetime
from celery import shared_task

from .models import Valute
from .parsing import parsing_course


@shared_task()
def update_or_create_valute_list():
    parsing_course()
