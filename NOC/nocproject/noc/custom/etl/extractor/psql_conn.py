
import psycopg2
from noc.custom.etl.engine.my_pass import netbox_pass,netbox_url

class psql_conn():
        conn = psycopg2.connect(
                            host=netbox_url ,
                            database="netbox",
                            user="netbox",
                            password=netbox_pass,
                            sslmode='disable',
                        )


        def postgre_conn_locations_add(self):
            cur = self.conn.cursor()
            cur.execute("SELECT id , name , parent_id, level, tree_id FROM dcim_location;")
            locations = (cur.fetchall())

            return locations

        def parser(self):
            lst = self.postgre_conn_locations_add()
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
                        child.append((ch[0], f'| {par[1]} || {ch[1]} | '))

                    elif ch[3] == 2 and ch[4] == par[4]:
                        for ch_p in child_tupe:
                            if ch_p[0] == ch[2]:
                                child.append((ch[0], f'| {par[1]} || {ch_p[1]} || {ch[1]} |'))
            return child


        def get_result(self,id):
            prerezult = self.parser()
            for pr in prerezult:
                if pr[0] == id:
                  return pr[1]
                else:
                    continue


