from django.core.management.base import BaseCommand
from payeshapp.models import SslData
import pandas as pd


def read_from_csv():
    where_file()


def where_file():
    file = '/home/payesh/payesh/ssl_data.csv'
    xl = pd.read_csv(file)
    read_csv_action(file)


def read_csv_action(file):
    i = 0
    for i in range(list(pd.read_csv(file)._values).__len__()):
        hostip = list(pd.read_csv(file)._values[i])[0]
        addr = list(pd.read_csv(file)._values[i])[1]
        save_distinct(hostip, addr)


def save_distinct(hostip, addr):
    if not SslData.objects.filter(hostip=hostip):
        ssl_data = SslData(hostip=hostip, addr=addr)
        ssl_data.save()


class Command(BaseCommand):
    def handle(self, **options):
        read_from_csv()

