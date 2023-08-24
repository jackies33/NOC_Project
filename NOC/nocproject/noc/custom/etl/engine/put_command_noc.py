
import subprocess
import os
import re
import time


def put_command_extract():
            command1 = "/opt/noc"
            command2 = ("./noc etl extract NBRemoteSystem")
            os.chdir(command1)
            out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
            out1 = str(out2)
            find = re.findall(r"\[NBRemoteSystem\|managedobject\] \d+ records extracted", out1)
            if find != []:
                out = True
                return out
            else:
                out = False
                return out




def put_command_check():
            command1 = "/opt/noc"
            command2 = ("./noc etl check NBRemoteSystem")
            os.chdir(command1)
            out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
            out1 = str(out2)
            find = re.findall(r'NBRemoteSystem.\S+: \S+', out1)
            if find != []:
                out = True
                return out
            else:
                out = False
                return out

def put_command_load_add():
            command1 = "/opt/noc"
            command2 = ("./noc etl load NBRemoteSystem")
            os.chdir(command1)
            out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
            out1 = str(out2)
            find = re.findall(r"\[NBRemoteSystem\|managedobject\] Summary: [1-9]+ new", out1)
            if find != []:
                out = True
                return out
            else:
                out = False
                return out


def put_command_load_update():
    command1 = "/opt/noc"
    command2 = ("./noc etl load NBRemoteSystem")
    os.chdir(command1)
    out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
    out1 = str(out2)
    find = re.findall(r"\[NBRemoteSystem\|managedobject\] Summary: [0-9]+ new, [1-9]+ changed", out1)
    if find != []:
        out = True
        return out
    else:
        out = False
        return out





def put_command_wipe(man_obj):
            command1 = "/opt/noc"
            command2 = (f"./noc wipe managed_object {man_obj}")
            os.chdir(command1)
            out = str(subprocess.run(command2.split(), stdout=subprocess.PIPE))
            find = re.findall(r'Remove FTS index for sa.ManagedObject:', out)
            if find != []:
                out = True
                return out
            else:
                out = False
                return out


if __name__ == '__main__':
    print("put_command_noc.py_main")