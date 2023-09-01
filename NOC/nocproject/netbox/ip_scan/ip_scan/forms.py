

from django import forms
from .psql_conn import postgresql_connections

psql = postgresql_connections()


def get_par_tuples_location():
    lst = psql.postgre_conn_locations()
    par_tuple = []
    for par in lst:
        if par[2] == None:
            par_tuple.append((par[0],par[1]))


    return par_tuple


def get_ch_tuples_location():
    lst = psql.postgre_conn_locations_add()
    child = []
    tuples_parent = []
    child_tupe = []
    last_values = [t[-1] for t in lst]
    duplicates = list(set([x for x in last_values if last_values.count(x) > 1]))
    new_lst = []
    for i in range(len(lst)):
        if lst[i][-1] in duplicates:
            new_lst.append(lst[i])
    for p in new_lst:
        if p[2] == None:
            tuples_parent.append(p)
    for ch in new_lst:
        if ch[2] != None:
            child_tupe.append(ch)

    for ch in child_tupe:
        for par in tuples_parent:
            if ch[3] == 1 and ch[4] == par[4]:
                # print(ch)
                child.append((ch[0], f'| {par[1]} || {ch[1]} |'))

            elif ch[3] == 2 and ch[4] == par[4]:
                for ch_p in child_tupe:
                    if ch_p[0] == ch[2]:
                        child.append((ch[0], f'| {par[1]} || {ch_p[1]} || {ch[1]} |'))
    child.insert(0,('','--------'))
    return child


class IpAddressForm(forms.Form):

    #choices_manufacturer = psql.postgre_conn_manufacturer()
    choices_platform = psql.postgre_conn_platform()
    choices_device_type = psql.postgre_conn_device_type()
    #choices_site_name = psql.postgre_conn_site()
    choices_device_role = psql.postgre_conn_device_role()
    choices_tenants = psql.postgre_conn_tenant()
    choices_management = [(1,'Active'),(2,'Offline')]


    ip_address = forms.CharField(label='IP address', max_length=20,help_text='primary ip address for network device management', widget=forms.TextInput(attrs={'class': 'myfield'}))
    #manufacturer = forms.ChoiceField(label='Vendor' , choices=choices_manufacturer,help_text="Vendor's name", widget=forms.Select(attrs={'class': 'myfield'}))
    platform = forms.ChoiceField(label='Platform' , choices=choices_platform,help_text="Platform", widget=forms.Select(attrs={'class':'myfield'}))
    device_type = forms.ChoiceField(label='Device type' , choices=choices_device_type,help_text='network equipment vendor name', widget=forms.Select(attrs={'class': 'myfield'}))
    #site_name = forms.ChoiceField(label='Site name' , choices=choices_site_name,help_text='network device location name', widget=forms.Select(attrs={'class': 'myfield'}))
    locations = forms.ChoiceField(label='Locations', choices=get_par_tuples_location(),help_text='Location geo',widget=forms.Select(attrs={'class': 'myfield'}))
    locations_add = forms.ChoiceField(label='Locations_additionally',choices=get_ch_tuples_location(),required=False,widget=forms.Select(attrs={'class': 'myfield'}))
    device_role = forms.ChoiceField(label='Device role' , choices=choices_device_role,help_text='the role of the network device in the topology', widget=forms.Select(attrs={'class': 'myfield'}))
    tenants = forms.ChoiceField(label='Tenants', choices=choices_tenants,help_text='Ministerstvo', widget=forms.Select(attrs={'class': 'myfield'}))
    management = forms.ChoiceField(label='Management state', choices=choices_management, help_text='State of device',widget=forms.Select(attrs={'class': 'myfield'}))
    my_button = forms.CharField(label= '', widget=forms.TextInput(attrs={'type': 'submit', 'value': 'Create new device','class': 'mybutton'}))

