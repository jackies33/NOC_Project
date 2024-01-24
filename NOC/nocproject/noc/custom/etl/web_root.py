

import time
import datetime
from flask import Flask, request, make_response
import json
from engine.put_command_noc import NOC_SHELL
from engine.tg_bot import telega_bot


''' 
for daemon setup script
create  - >> "mcedit etc/systemd/system/web_root.service"
copy in web_root.service ->> 
_______________________________

[Unit]
Description=Listen and classifier web hooks from netbox App

[Service]
ExecStart=/usr/bin/python3 /opt/noc/custom/etl/web_root.py
StandardOutput=file:lweb_root/output.log
StandardError=file:/var/log/web_root/error.log
Restart=always

[Install]
WantedBy=multi-user.target
_________________________________

<<----copy in web_root.service

run next commands -->>>
_____________________________
sudo systemctl daemon-reload
sudo systemctl enable web_root.service
sudo systemctl start web_root.service

______________________________

<<--- run next commands

'''





app = Flask(__name__)
@app.route('/webhook', methods=['POST'])

#create listener web hooks from netbox

def webhook():
            data = request.get_json()
            json_dump = json.dumps(data)
            print(json_dump)
            result = parser_webhooks(data) # call func , where we will be pars recieved data from web hook from netbox
            try:
                for rec in result:
                    print(rec)
            except TypeError:
                print(f'in {object.__name__} not enough data')
            response = {
                'fulfillmentText': 'success'
            }
            return make_response(json.dumps(response))

def parser_webhooks(file_json):


          try:
            event = file_json['event']
            time1 = file_json['timestamp']
            target = file_json['model']
            data_device_all = file_json['data']
            data_device_id = 'device_id: ' + (str(data_device_all['id']))
            data_device_name = data_device_all['name']
            data_device_created = data_device_all['created']
            data_device_primary_ip = data_device_all['primary_ip']
            primary_ip = data_device_primary_ip['address']
            print(event, time1,target, data_device_id,data_device_created,data_device_all)
            #everything above parse and collecting data from web hook , and then call the func to figure out the data
            classifier_and_executor(event, time1,target, data_device_id,data_device_created,data_device_all,primary_ip)
            return event, time1, target, data_device_id, primary_ip, data_device_name ,data_device_created
          except TypeError:
            print(f'in {object.__name__} not enough data')
            #check_update()


def classifier_and_executor(event,time1,target,data_device_id,data_device_created,data_device_all,primary_ip):
            split_create1 = data_device_created.split('.')[0]
            split_time = time1.split('.')[0]
            dt_create = datetime.datetime.strptime(split_create1, "%Y-%m-%dT%H:%M:%S")
            dt_wh = datetime.datetime.strptime(split_time, "%Y-%m-%d %H:%M:%S")
            dt_count = dt_create + datetime.timedelta(seconds=30)
            #find out if an "update" has arrived (it should be an "update" to create an ip address) within 40 seconds after the "create" event
            man_obj = data_device_all['name']
            noc_shell = NOC_SHELL(man_obj)
            if event == "updated" and target == 'device' and primary_ip != None:
                if dt_wh > dt_count:
                    print('its update')
                    time.sleep(4)
                    # change_var(int(data_device_all['id']))
                    out = noc_shell.put_command_extract()
                    if out == True:
                        out1 = noc_shell.put_command_check()
                        if out1 == True:
                            out_complete = noc_shell.put_command_load_update()
                            if out_complete == True:
                                vc_enable = data_device_all['virtual_chassis']
                                if vc_enable != None:
                                    vc_name = vc_enable['name']
                                    print(f'Sucessfull update Managed_object - {vc_name} in noc-system')
                                    message = (f'Noc.handler[ "Event_Update Device" ]\n Device Name - [ "{vc_name}" ] \n ip_address - [ "{primary_ip}" ] \n Time: [ "{datetime.datetime.now()}" ]')
                                    sender = telega_bot(message)
                                    sender.tg_sender()
                                else:
                                    print(f'Sucessfull update Managed_object - {man_obj} in noc-system')
                                    message = (f'Noc.handler[ "Event_Update Device" ]\n Device Name - [ "{man_obj}" ] \n ip_address - [ "{primary_ip}" ] \n Time: [ "{datetime.datetime.now()}" ]')
                                    sender = telega_bot(message)
                                    sender.tg_sender()

                                # put_command_clear_mappings()
                            if out_complete == False:
                                print(f'Not success Update Managed_object - {man_obj} !!!!')
                        elif out1 == False:
                            print(f'Not success check(extract) Managed_object - {man_obj} !!!!')
                    elif out == False:
                        print(f"Not success extract - {man_obj} !!!")

                elif dt_wh < dt_count:
                    print('its create')
                    time.sleep(4)
                    #change_var(int(data_device_all['id']))
                    out = noc_shell.put_command_extract()
                    if out == True:
                        out1 = noc_shell.put_command_check()
                        if out1 == True:
                            out_complete = noc_shell.put_command_load_add()
                            if out_complete == True:
                                print(f'Sucessfull load Managed_object - {man_obj} in noc-system')
                                message = (f'Noc.handler[ "Event_Add Device" ]\n Device Name - [ "{man_obj}" ] \n ip_address - [ "{primary_ip}" ] \n Time: [ "{datetime.datetime.now()}" ]')
                                sender=telega_bot(message)
                                sender.tg_sender()

                                #put_command_clear_mappings()
                            if out_complete == False:
                                print(f'Not success load Managed_object - {man_obj} !!!!')
                        elif out1 == False:
                            print(f'Not success check(extract) Managed_object - {man_obj} !!!!')
                    elif out == False:
                        print(f"Not success extract - {man_obj} !!!")

            elif event == "created" and target == 'device':
                print(f"need a check for update Managed_object - {man_obj}!!!")
            elif event == "deleted" and target == 'device':
                vc_enable = data_device_all['virtual_chassis']
                if vc_enable != None:
                    vc_name = vc_enable['name']
                    print(f"check deleted Managed_object - {vc_name}")
                    message = (f'Netbox.handler[ "Event_Delete Device" ]\n Device Name - [ "{man_obj}" ] \n ip_address - [ "{primary_ip}" ] \n Time: [ "{datetime.datetime.now()}" ]')
                    sender = telega_bot(message)
                    sender.tg_sender()
                    noc_shell = NOC_SHELL(vc_name)
                    out_delete = noc_shell.put_command_wipe()
                    if out_delete == True:
                        message = (f'Noc.handler[ "Event_Delete Device" ]\n Device Name - [ "{vc_name}" ] \n ip_address - [ "{primary_ip}" ] \n Time: [ "{datetime.datetime.now()}" ]')
                        sender = telega_bot(message)
                        sender.tg_sender()
                    elif out_delete == False:
                        print(f'Not success delete Managed_object - {vc_name} !!!!')
                else:
                    print(f"check deleted Managed_object - {man_obj}")
                    message = (f'Netbox.handler[ "Event_Delete Device" ]\n Device Name - [ "{man_obj}" ] \n ip_address - [ "{primary_ip}" ] \n Time: [ "{datetime.datetime.now()}" ]')
                    sender = telega_bot(message)
                    sender.tg_sender()
                    out_delete = noc_shell.put_command_wipe()
                    if out_delete == True:
                        message = (f'Noc.handler[ "Event_Delete Device" ]\n Device Name - [ "{man_obj}" ] \n ip_address - [ "{primary_ip}" ] \n Time: [ "{datetime.datetime.now()}" ]')
                        sender = telega_bot(message)
                        sender.tg_sender()
                    elif out_delete == False:
                        print(f'Not success delete Managed_object - {man_obj} !!!!')
            else:
                pass

if __name__ == '__main__':
    app.run(host='10.50.74.171', port=3501)

