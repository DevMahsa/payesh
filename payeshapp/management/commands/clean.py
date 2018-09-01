from payeshapp.models import *

LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'rtisdb')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'rtisdb')).all().delete()
WindowsServer.objects.get(name = 'rtisdb').delete()

LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'always on db')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'always on db')).all().delete()
WindowsServer.objects.get(name = 'always on db').delete()


LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'rtis-platform')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'rtis-platform')).all().delete()
WindowsServer.objects.get(name = 'rtis-platform').delete()


LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'rtisapp')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'rtisapp')).all().delete()
WindowsServer.objects.get(name = 'rtisapp').delete()



LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'diningapp182')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'diningapp182')).all().delete()
WindowsServer.objects.get(name = 'diningapp182').delete()



LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'dining180')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'dining180')).all().delete()
WindowsServer.objects.get(name = 'dining180').delete()



LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'diningdb181')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'diningdb181')).all().delete()
WindowsServer.objects.get(name = 'diningdb181').delete()



LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'elk')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'elk')).all().delete()
WindowsServer.objects.get(name = 'elk').delete()



LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'sdr')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'sdr')).all().delete()
WindowsServer.objects.get(name = 'sdr').delete()




LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'dcomd')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'dcomd')).all().delete()
WindowsServer.objects.get(name = 'dcomd').delete()




LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'LTC')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'LTC')).all().delete()
WindowsServer.objects.get(name = 'LTC').delete()





LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'plesk_linux_244')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'plesk_linux_244')).all().delete()
WindowsServer.objects.get(name = 'plesk_linux_244').delete()

