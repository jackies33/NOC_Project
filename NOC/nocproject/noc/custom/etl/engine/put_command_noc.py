
import subprocess
import os
import re


class NOC_SHELL():


        """

        Class for execute noc shell commands for different purposes

        """

        def __init__(self, man_obj = None):
            self.command1 = "/opt/noc"
            self.man_obj = man_obj


        def put_command_extract(self):
                    command2 = ("./noc etl extract NBRemoteSystem")
                    os.chdir(self.command1)
                    out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
                    out1 = str(out2)
                    find = re.findall(r"\[NBRemoteSystem\|managedobject\] \d+ records extracted", out1)
                    if find != []:
                        out = True
                        return out
                    else:
                        out = False
                        return out




        def put_command_check(self):
                    command2 = ("./noc etl check NBRemoteSystem")
                    os.chdir(self.command1)
                    out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
                    out1 = str(out2)
                    find = re.findall(r'NBRemoteSystem.\S+: \S+', out1)
                    if find != []:
                        out = True
                        return out
                    else:
                        out = False
                        return out

        def put_command_load_add(self):
                    command2 = ("./noc etl load NBRemoteSystem")
                    os.chdir(self.command1)
                    out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
                    out1 = str(out2)
                    find = re.findall(r"\[NBRemoteSystem\|managedobject\] Summary: [1-9]+ new", out1)
                    if find != []:
                        out = True
                        return out
                    else:
                        out = False
                        return out


        def put_command_load_update(self):
            command2 = ("./noc etl load NBRemoteSystem")
            os.chdir(self.command1)
            out2 = subprocess.run(command2.split(), stdout=subprocess.PIPE)
            out1 = str(out2)
            find = re.findall(r"\[NBRemoteSystem\|managedobject\] Summary: [0-9]+ new, [1-9]+ changed", out1)
            if find != []:
                out = True
                return out
            else:
                out = False
                return out





        def put_command_wipe(self,*args):
                    command2 = (f"./noc wipe managed_object {self.man_obj}")
                    os.chdir(self.command1)
                    out = str(subprocess.run(command2.split(), stdout=subprocess.PIPE))
                    find = re.findall(r'Remove FTS index for sa.ManagedObject:', out)
                    if find != []:
                        out = True
                        return out
                    else:
                        out = False
                        return out


if __name__ == '__main__':
    shell = NOC_SHELL()
    shell.put_command_extract()