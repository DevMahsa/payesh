from django.core.management.base import BaseCommand
from payeshapp.models import SqlDataAuth
import pandas as pd


def read_from_csv():
    where_file()


def where_file():
    file = '/home/payesh/payesh/sql_data.csv'
    xl = pd.read_csv(file)
    read_csv_action(file)


def read_csv_action(file):
    i = 0
    for i in range(list(pd.read_csv(file)._values).__len__()):
        name = list(pd.read_csv(file)._values[i])[0]
        host = list(pd.read_csv(file)._values[i])[1]
        server = list(pd.read_csv(file)._values[i])[2]
        port = list(pd.read_csv(file)._values[i])[3]
        user = list(pd.read_csv(file)._values[i])[4]
        password = list(pd.read_csv(file)._values[i])[5]
        save_distinct(host, name, password, port, server, user)


def save_distinct(host, name, password, port, server, user):
    if not SqlDataAuth.objects.filter(name__iexact=name):
        sql_data_auth = SqlDataAuth(name=name, host=host, server=server, port=port, user=user, password=password)
        sql_data_auth.save()


class Command(BaseCommand):
    def handle(self, **options):
        read_from_csv()

