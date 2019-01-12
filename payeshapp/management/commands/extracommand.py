# import subprocess
# import shlex
# subprocess.run(shlex.split('cat /etc/passwd | grep "/bin/bash"'))
# subprocess.run(['cat', '/etc/passwd'])
#
import os
# os.system("cat /etc/passwd | grep '/bin/bash'")
import subprocess
value=subprocess.check_output(['/home/mahsa/PycharmProjects/payesh/payesh/user.sh'])
# os.system('chage -l mahsa')
mylist = ""
temp = str(value).split(':x:')
mylist += temp[0]
for j in range(1, len(temp)):
        user = temp[j].split('/bin/bash')[1]
        command = str('chage -l'+user)
        os.system(command=command)
        mylist += user
flist = mylist.split('\n')
print(flist)
