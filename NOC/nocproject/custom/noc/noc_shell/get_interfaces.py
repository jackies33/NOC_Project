
import pandas as pd
import ast



columns_mapping = {
    1: 'name',
    2: 'ip_address'
}

def extract_interfaces(field_num,name):
    csv_file = "output_interfaces.csv"
    try:
        df = pd.read_csv(csv_file)
        field = columns_mapping.get(field_num)
        result = df[df[field] == name]['interfaces'].values
        if len(result) > 0:
            interfaces_data = ast.literal_eval(result[0])
            if len(interfaces_data) > 0:
                with open('interfaces_data.txt', 'w') as f:
                    for interface in interfaces_data:
                        f.write(f"iface_name: {interface.get('iface_name', '')}\n")
                        f.write(f"iface_mac: {interface.get('iface_mac', '')}\n")
                        f.write(f"iface_description: {interface.get('iface_description', '')}\n\n")
                print("\n\nOK\n\n")
            else:
                print("Для указанного имени нет данных интерфейсов.")
        else:
            print("Имя не найдено в файле CSV.")
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print("Произошла ошибка:", e)



if __name__ == "__main__":
    print("Выберите поле для поиска:")
    for num, column in columns_mapping.items():
        print(f"{num}: {column}")
    field_num = int(input("Введите номер поля: "))
    value = input("Введите значение для поля: ")
    extract_interfaces(field_num,value)