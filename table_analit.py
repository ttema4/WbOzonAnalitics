import pandas as pd


def get_sheet_name(route_to_file):
    try:
        df = pd.ExcelFile(route_to_file)
        return df.sheet_names[0]
    except:
        return 'ОшибкаИмени'


def analits_wb(route_to_file, parent=None, main=None):
    HEADERS_FROM = ['Артикул поставщика', 'Обоснование для оплаты', 'Кол-во',
                    'Цена розничная с учетом согласованной скидки',
                    'К перечислению Продавцу за реализованный Товар', 'Количество доставок',
                    'Количество возврата', 'Услуги по доставке товара покупателю', 'Доплаты']
    HEADERS_TO = ['id позиции', 'Кол-во продаж', 'Кол-во доставок', 'Кол-во возвратов', 'Цена с учетом скидки',
                  'Сумма к перечислению', 'Затраты на доставку', 'Сумма доплат', 'За вычетом логистики и доплат']
    COUNT_ANALIZED_COLS = 8
    df = pd.read_excel(route_to_file)
    df = df.dropna(how='all')

    data = []
    for x in HEADERS_FROM:
        data.append(df[x].tolist())
    analized_data = {}
    for x in set(df['Артикул поставщика'].tolist()):
        analized_data[x] = [0] * COUNT_ANALIZED_COLS

    for i in range(len(data[0])):
        line = []
        for j in range(len(data)):
            line.append(data[j][i])
        if line[1] == 'Логистика':
            new_line = analized_data[line[0]].copy()
            new_line[1] += line[5]  # кол-во доставок
            new_line[2] += line[6]  # кол_во возвратов
            new_line[5] += line[7]  # затраты на доставку
            analized_data[line[0]] = new_line
        elif line[1] == 'Доплаты':
            new_line = analized_data[line[0]].copy()
            new_line[6] += line[8]  # доплат на сумму
            new_line[2] += line[6]  # кол_во возвратов
            analized_data[line[0]] = new_line
        elif line[1] == 'Продажа':
            new_line = analized_data[line[0]].copy()
            new_line[0] += 1  # кол-во продаж
            new_line[2] += line[6]  # кол_во возвратов
            new_line[3] += line[3]  # цена с учетом скидки
            new_line[4] += line[4]  # к перечислению
            analized_data[line[0]] = new_line
        else:
            new_line = analized_data[line[0]].copy()
            new_line[4] += line[4]  # к перечислению
            new_line[2] += line[6]  # кол_во возвратов
            analized_data[line[0]] = new_line

    new_data = []
    for x in analized_data.keys():
        new_line = analized_data[x].copy()
        new_line[3] = round(new_line[3], 1)  # округления и подсчет итоговой суммы
        new_line[4] = round(new_line[4], 1)
        new_line[5] = round(new_line[5], 1)
        new_line[6] = round(new_line[6], 1)
        new_line[7] = round(new_line[4] - new_line[5] - new_line[6], 2)
        new_data.append([x] + new_line)
    new_data.sort(key=lambda x: x[0])
    new_data.append(
        [len(new_data)] + [sum([new_data[j][i] for j in range(len(new_data))]) for i in range(1, len(new_data[0]))])
    return new_data


def analits_ozon(route_to_file):
    pass

#  print(analits_wb('Книга1.xlsx'))
