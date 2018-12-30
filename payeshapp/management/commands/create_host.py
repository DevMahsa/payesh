from pyzabbix import ZabbixAPI
import csv
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer

zapi = ZabbixAPI("https://zmonitor.ut.ac.ir")
zapi.login(user="mahsa_", password="Pooya871^")
arq = csv.reader(open('/home/mahsa/PycharmProjects/payesh/payesh/hosts.csv'))
linhas = sum(1 for linha in arq)
f = csv.reader(open('/home/mahsa/PycharmProjects/payesh/payesh/hosts.csv'), delimiter=',')
bar = ProgressBar(maxval=linhas,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
i = 0
try:
    for [hostname,name,ip] in f:
        hostcriado = zapi.host.create(
            host= hostname,
            name = name,
            status= 0,
            interfaces=[{
                "type": 1,
                "main": "1",
                "useip": 1,
                "ip": ip,
                "dns": "192.168.20.14",
                "port": 10050
            }],
            groups=[{
                "groupid": 83
            }],
            templates=[{
                "templateid": 10104
            }]
        )
        i += 1
        bar.update(i)
except Exception as e:
    print(e)
bar.finish
print (" ")