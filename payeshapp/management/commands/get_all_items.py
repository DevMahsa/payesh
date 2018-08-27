from  datetime import datetime
from django.core.management.base import BaseCommand
from pyzabbix import ZabbixAPI
from payeshapp.models import Server
from django.db.models import Q

def get_items():

    zapi = login()

    for h in zapi.host.get(output="extend"):

        for host in Server.objects.filter(name=h['name']):
            # curr=Server.objects.filter(name=h['name'])
            # nameserver = curr.get(name__contains=h['name']).name.encode('utf-8') ==host.name
            for i in zapi.item.get(filter={'host': host.name}):
                host.date = datetime.now()
                mcafee(host, i)
                telnet(host, i)
                free_disk_c(host, i)
                free_disk_d(host, i)
                free_disk_e(host, i)
                free_disk_f(host, i)
                free_disk_g(host, i)
                free_disk_h(host, i)
                free_disk_i(host, i)
                open_ports(host, i)
                microsoft_update(host, i)
                local_users(host, i)
                event_log_max_size(host, i)
                sys_event(host, i)
                app_event(host, i)
                file_sharing_ports(host, i)
                win_xpr_date(host, i)
                software_version(host, i)
                anydesk(host, i)
                time_sync(host, i)
                firewall_status(host, i)
                smb_config(host, i)

                #if i['name'].encode('utf-8').lower().find('all open port')==0:
                 #   host.open_ports = i['lastvalue'].encode('utf-8')

            host.save()



def firewall_status(host, i):
    try:
        if i['name'].lower().find('firewall status') == 0:
            firewall = i['lastvalue'].split('EnableFirewall')[1].split('REG_DWORD')[1].split('0x1')
            if len(firewall) >= 2:
                host.firewall = "ON"
            else:
                host.firewall = "OFF"
    except IndexError:
        pass

def smb_config(host, i):
    try:
        if i['name'].lower().find('smb config') == 0:
            smb = i['lastvalue'].split('EnableSMB1Protocol')[1].split('EnableSMB2Protocol')[0].split('True')
            if len(smb) >= 2:
                host.smb1_config = "Enable"
            else:
                host.smb1_config = "Disable"
    except IndexError:
        pass

def time_sync(host, i):
    if i['name'].lower().find('time win sync') == 0:
        time = i['lastvalue'].split('time.ut.ac.ir')
        if len(time) >= 2:
            host.time_win_sync = "YES"
        else:
            host.time_win_sync = "NO"


def anydesk(host, i):
    if i['name'].lower().find('all program files x86') == 0:
        any_desk = i['lastvalue'].split('AnyDesk')

        if len(any_desk) >= 2:
            host.anydesk = "ON"
        else:
            host.anydesk = "OFF"

    if i['name'].lower().find('all process') == 0:
        any_desk = i['lastvalue'].split('AnyDesk')
        if len(any_desk) >= 2:
            host.anydesk = "OFF"
        else:
            host.anydesk = "ON"


def software_version(host, i):
    try:
        if i['name'].lower().find('software version') == 0:
            host.windows_version = i['lastvalue'].split('BuildLab')[2].split('REG_SZ')[1].split('.amd')[0]
    except IndexError:
        pass

def win_xpr_date(host, i):
    try:
        if i['name'].lower().find('win xpr date') == 0:
            host.win_active = i['lastvalue'].split(':')[1]
    except IndexError:
        pass

def free_disk_g(host, i):
    if i['name'].lower().find('free disk space logical g:') == 0:
        host.freediskg = i['lastvalue']+'%'

def free_disk_h(host, i):
    if i['name'].lower().find('free disk space logical h:') == 0:
        host.freediskh = i['lastvalue']+'%'


def free_disk_i(host, i):
    if i['name'].lower().find('free disk space logical i:') == 0:
        host.freediski = i['lastvalue']+'%'


def file_sharing_ports(host, i):
    if i['name'].lower().find('file sharing port') == 0:
        if i['lastvalue'].split('filesharing').__len__() >=2:
            host.file_sharing_port = "No Script Available"
        else:
            if i['lastvalue']=='0':
                host.file_sharing_port = i['lastvalue']
            else:
                newlist=i['lastvalue'].split(' ')
                del(host.file_sharing_port)
                for i in newlist:
                    ip=host.ip
                    if not i=='':
                        if not len(i.split('TCP'))>=2:
                            if not len(i.split('UDP'))>=2:
                                if not len(i.split(ip))>=2:
                                    if not len(i.split('0.0.0.0'))>=2:
                                        if not len(i.split('[::]:'))>=2:
                                            if not len(i.split('*:*'))>=2:
                                                if not len(i.split('LISTENING'))>=2:
                                                    if not len(i.split('\r'))>=2:
                                                        host.file_sharing_port +='\n'+ i +'\n'





def app_event(host, i):
    if i['name'].lower().find('app event') == 0:
        if i['lastvalue'].split('appevent').__len__() >= 2:
            host.new_app_event = "No Script Available"
        else:
            if i['lastvalue']=='0':
                host.new_app_event = i['lastvalue']
            else:
                host.new_app_event ='MachineName: '+i['lastvalue'].split('MachineName')[1].split('\r')[0].split(':')[1] +'\n'+'EventID: '+i['lastvalue'].split('EventID')[1].split('\r')[0].split(':')[1]+'\n'+'Time'+i['lastvalue'].split('Time')[1].split('\r')[0]+'\n'+'Time'+i['lastvalue'].split('Time')[2].split('\r')[0]


def sys_event(host, i):
    if i['name'].lower().find('sys event') == 0:
        if i['lastvalue'].split('sysevent').__len__() >= 2:
            host.new_system_event = "No Script Available"
        else:
            if i['lastvalue']=='0':
                host.new_system_event = i['lastvalue']
            else:
                host.new_system_event ='MachineName: '+i['lastvalue'].split('MachineName')[1].split('\r')[0].split(':')[1] +'\n'+'EventID: '+i['lastvalue'].split('EventID')[1].split('\r')[0].split(':')[1]+'\n'+'Time'+i['lastvalue'].split('Time')[1].split('\r')[0]+'\n'+'Time'+i['lastvalue'].split('Time')[2].split('\r')[0]




def event_log_max_size(host, i):
    if i['name'].lower().find('eventlog max size') == 0:
        host.eventlog_max_size = i['lastvalue']


def local_users(host, i):
    if i['name'].lower().find('local users') == 0:
        if i['lastvalue'].split('localuser').__len__() >= 2:
            host.local_user = "No Script Available"
        else:
            host.local_user = i['lastvalue']


def microsoft_update(host, i):
    if i['name'].lower().find('microsoft update') == 0:
        host.microsoft_update = i['lastvalue']


def open_ports(host, i):
    if i['name'].lower().find('ports open firewall rules') == 0:
        host.open_port = i['lastvalue']


def free_disk_f(host, i):
    if i['name'].lower().find('free disk space logical f:') == 0:
        host.freediskf = i['lastvalue']+'%'


def free_disk_e(host, i):
    if i['name'].lower().find('free disk space logical e:') == 0:
        host.freediske = i['lastvalue']+'%'


def free_disk_d(host, i):
    if i['name'].lower().find('free disk space logical d:') == 0:
        host.freediskd = i['lastvalue']+'%'


def free_disk_c(host, i):
    if i['name'].lower().find('free disk space logical c:') == 0:
        host.freediskc = i['lastvalue']+'%'


def telnet(host, i):
    if i['name'].lower().find('telnet service') == 0:
        if i['lastvalue']=='0':
            host.telnet = 'OFF'
        else:
            host.telnet = 'ON'



def mcafee(host, i):
    if i['name'].lower().find('mcafee task manager') == 0:
        if i['lastvalue'] == '0':
            host.mcafee = 'ON'
        else:
            host.mcafee = 'OFF'


def login():
    zapi = ZabbixAPI("http://192.168.112.157:4720")
    zapi.login("riri", "rayta")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        get_items()


