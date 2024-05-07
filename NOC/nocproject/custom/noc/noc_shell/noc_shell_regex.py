

from paramiko import AuthenticationException,SSHException
import paramiko
import time
import re
import ast
from my_pass import password_dpmo


def make_cmnd(cmnd):
    make = (f"""\nfrom noc.sa.models.managedobject import ManagedObject
from noc.core.mongo.connection import connect
connect()
import re
for mo in ManagedObject.objects.filter(is_managed=True):
        name = mo.name
        config = str(mo.config.read())
        result = re.findall(r"{cmnd}",config)
        if result != []:
              my_dict = {{name:result[0]}}
              print(my_dict)\n\n""")
    result = NocShell(make)
    return result


def NocShell(main_cmnd):

        try :

                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname='10.50.74.171', username='guestnocshell', password=password_dpmo, port=22)
                ssh1 = client.invoke_shell()
                ssh1.send('\nsudo -s\n')
                time.sleep(1)
                ssh1.send('\ncd /opt/noc\n')
                time.sleep(1)
                ssh1.send('\n./noc shell\n')
                time.sleep(1)
                ssh1.send(main_cmnd)
                time.sleep(10)
                output1=(ssh1.recv(65535).decode("utf-8"))
                target = re.findall(r"\{'\S+': '.+'}",output1)
                target.pop(0)
                my_list = [ast.literal_eval(s) for s in target]
                client.close()
                return my_list

        except Exception as err:
            print(err)



if __name__ == '__main__':
   input_result = input("Please eneter your regex: ")
   result = make_cmnd(input_result)
   print(result)


