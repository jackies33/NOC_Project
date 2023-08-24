


class classifier():


        def classifier_AuthProf(self,device_type,device_tenant):
                    if device_type == "NE20E-S2F" and device_tenant == "P/PE":
                        authprof = "3"
                        return authprof
                    else:
                        authprof = "2"
                        return authprof


        def classifier_AuthScheme(self,custom_field):
                    connection_scheme = custom_field['Connection_scheme']
                    if connection_scheme == 'ssh':
                        AuthScheme = '2'
                        return AuthScheme
                    elif connection_scheme == 'telnet':
                        AuthScheme = '1'
                        return AuthScheme

