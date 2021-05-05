from django.apps import AppConfig
from .scheduler_dir import scheduler

class MainpageConfig(AppConfig):
    name = 'mainpage'

    # def ready(self):
    #     print("Starting Scheduler")
    #     scheduler.start()