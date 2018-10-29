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
            firewall2 = i['lastvalue'].split('exited')

            if len(firewall2) >= 2:
                host.firewall = "ON"
            else:
                host.firewall = "OFF"
        elif i['name'].lower().find('firewall status rpm based') ==0:
            firewall1 = i['lastvalue'].split('running')
            if len(firewall1) >= 2:
                host.firewall = "ON"

            else:
                host.firewall = "OFF"
        elif i['name'].lower().find('firewall alternative') == 0:
            firewall1 = i['lastvalue'].split('running')
            firewall2 = i['lastvalue'].split('exited')
            if len(firewall1) >= 2 :
                host.firewall = "ON"

            elif  len(firewall2) >= 2:
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
    zapi = ZabbixAPI("https://zmonitor.ut.ac.ir")
    zapi.session.verify = False
    zapi.login("ririlinux", "ririlinux")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        get_items()


