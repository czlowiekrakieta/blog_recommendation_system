from .models import Calculations
from celery import task

@task
def calculate_things():
    print("its going on")
    c = Calculations.objects.get(pk=1)
    c.execute()

@task
def working():
    print("lalalallalalalla______________")
    return "its happening"