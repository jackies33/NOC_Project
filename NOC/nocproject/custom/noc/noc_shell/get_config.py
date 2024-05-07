


import pandas as pd

##### for get config by ip address from csv file


def parse_config(ip_address):
    df = pd.read_csv('configs_output.csv')
    filtered_df = df[df['IP Address'] == ip_address]
    if len(filtered_df) == 0:
        result_main = False
        result =f"\not found config for ip address: {ip_address}\n"
        result_share = [result_main,result]
    else:
        name = filtered_df.iloc[0]['Name']
        config = filtered_df.iloc[0]['Config']
        result = f"\nConfig for MO >>> {name} <<< has writen in file - 'my_config.conf'\n"
        result_share = [config,result]

    return result_share


if __name__ == '__main__':
    ip_address = input("Enter ip_address(0.0.0.0): ")
    result = parse_config(ip_address)
    if result[0] == False:
        print(result[1])
    else:

        with open('my_config.conf', 'w') as my_file:
            print(result[1])
            my_file.write(result[0])
            my_file.close()


