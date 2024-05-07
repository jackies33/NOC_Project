

import pandas as pd
import ast


columns_mapping = {
    1: 'name',
    2: 'ip_address',
    3: 'description',
    4: 'tags',
    5: 'mo_profile',
    6: 'sa_profile',
    7: 'platform',
    8: 'adm_dom',
    9: 'segment',
    10: 'pool'
}

def search_csv_by_tags(tag):
    csv_file = "output_all_managed_objects.csv"
    try:
        df = pd.read_csv(csv_file)
        df['tags'] = df['tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
        result = df[df['tags'].apply(lambda x: tag in x)]
        if not result.empty:
            print("\nOK\n")
            return (result.to_string(index=False))
        else:
            print("Нет строк с заданным тегом.")
            return False
    except FileNotFoundError:
        print("Файл не найден.")
        return False
    except Exception as e:
        print("Произошла ошибка:", e)
        return False


def search_csv(field_num, value):
    try:
        csv_file = "output_all_managed_objects.csv"
        df = pd.read_csv(csv_file)
        field = columns_mapping.get(field_num)
        if field != 'tags':
            filtered_df = df[df[field].str.contains(value, case=False, na=False)]
            if not filtered_df.empty:
                    print("\nOK\n")
                    return (filtered_df.to_string(index=False))
            else:
                print("Нет совпадений для заданных критериев.")
                return False
        elif field == 'tags':
            result = search_csv_by_tags(value)
            return result
        else:
            print("Некорректный номер поля.")
            return False
    except FileNotFoundError:
        print("Файл не найден.")
        return False
    except Exception as e:
        print("Произошла ошибка:", e)
        return False



if __name__ == "__main__":
    print("Выберите поле для поиска:")
    for num, column in columns_mapping.items():
        print(f"{num}: {column}")
    field_num = int(input("Введите номер поля: "))
    value = input("Введите значение для поля: ")
    result = search_csv(field_num, value)
    if result == False:
        with open('MO_data.txt', 'w') as my_file:
            my_file.write('None')
            my_file.close()
    else:
        with open('MO_data.txt', 'w') as my_file:
            my_file.write(str(result))
            my_file.close()
