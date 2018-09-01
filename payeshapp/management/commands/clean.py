from payeshapp.models import *

LastCpu.objects.filter(server = WindowsServer.objects.get(name = 'liferay-new')).all().delete()
LastMemory.objects.filter(server = WindowsServer.objects.get(name = 'liferay-new')).all().delete()
WindowsServer.objects.get(name = 'liferay-new').delete()


