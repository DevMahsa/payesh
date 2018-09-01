from  datetime import datetime
from django.core.management.base import BaseCommand
from pyzabbix import ZabbixAPI
from payeshapp.models import LinuxServer

def get_items():

    zapi = login()

    for h in zapi.host.get(output="extend"):

        for host in LinuxServer.objects.filter(name=h['name']):

            for i in zapi.item.get(filter={'host': host.name}):
                host.date = datetime.now()
                time_sync(host, i)
                firewall_status(host, i)

            host.save()



def firewall_status(host, i):
    try:
        if i['name'].lower().find('firewall status deb based') ==0:
            firewall = i['lastvalue'].split('running')
            if len(firewall) >= 2:
                host.firewall = "ON"
            else:
                host.firewall = "OFF"
        elif i['name'].lower().find('firewall status rpm based') ==0:
            firewall = i['lastvalue'].split('running')
            if len(firewall) >= 2:
                host.firewall = "ON"
            else:
                host.firewall = "OFF"
        elif i['name'].lower().find('firewall alternative') == 0:
            firewall = i['lastvalue'].split('running')
            if len(firewall) >= 2:
                host.firewall = "ON"
            else:
                host.firewall = "OFF"
    except IndexError:
        pass


def time_sync(host, i):

    if i['name'].lower().find('is time sync')==0:
        time = i['lastvalue'].split('192.168.20.23')
        if len(time) >= 2:
            host.ut_time_sync = "YES"
        else:
            host.ut_time_sync = "NO"




def login():
    zapi = ZabbixAPI("http://192.168.112.157:4720")
    zapi.login("ririlinux", "ririlinux")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        get_items()


