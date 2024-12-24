import os
import csv
from operator import itemgetter


class PriceMachine:
    def __init__(self):
        # Список с данными из прайс-листов
        self.data = []
        # Максимальная длина имени товара для выравнивания вывода
        self.name_length = 0

    def load_prices(self, folder_path='data/'):
        """
        Загрузка данных из прайс-листов в указанном каталоге.
        """
        for filename in os.listdir(folder_path):
            if 'price' not in filename.lower():
                continue  # Пропускаем файлы без слова "price"

            with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                product_index = None
                price_index = None
                weight_index = None

                # Поиск индексов нужных столбцов
                for i, header in enumerate(headers):
                    if header.lower() in ['название', 'продукт', 'товар', 'наименование']:
                        product_index = i
                    elif header.lower() in ['цена', 'розница']:
                        price_index = i
                    elif header.lower() in ['вес', 'масса', 'фасовка']:
                        weight_index = i

                if product_index is None or price_index is None or weight_index is None:
                    print(f"В файле {filename} отсутствуют необходимые столбцы.")
                    continue

                for row in reader:
                    try:
                        name = row[product_index]
                        price = float(row[price_index])
                        weight = float(row[weight_index])
                        price_per_kg = round(price / weight, 2)
                        self.data.append((name, price, weight, filename, price_per_kg))
                        self.name_length = max(len(name), self.name_length)
                    except ValueError:
                        print(f"Ошибка при обработке строки в файле {filename}.")
                        continue

    def find_text(self, search_text):
        """
        Поиск товаров по фрагменту названия.
        Возвращает список позиций, отсортированных по цене за килограмм.
        """
        results = [(i + 1, *row) for i, row in enumerate(self.data) if search_text.lower() in row[0].lower()]
        return sorted(results, key=itemgetter(-1))  # Сортируем по цене за килограмм

    def export_to_html(self, output_file='price_list.html'):
        """
        Экспорт данных в HTML-файл.
        """
        sorted_data = sorted(self.data, key=lambda x: x[1])
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Анализ прайс-листов</title>
    </head>
    <body>
        <h1>Результаты анализа прайс-листов</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>№</th>
                    <th>Наименование</th>
                    <th>Цена</th>
                    <th>Вес</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
            </thead>
            <tbody>
    ''')

            for i, (name, price, weight, filename, price_per_kg) in enumerate(sorted_data, start=1):
                f.write(f'''
    <tr>
    <td>{i}</td>
    <td>{name}</td>
    <td>{price:.2f}</td>
    <td>{weight:.2f}</td>
    <td>{os.path.basename(filename)}</td>
    <td>{price_per_kg:.2f}</td>
    </tr>
    ''')

            f.write('''
            </tbody>
        </table>
    </body>
    </html>
    ''')


# Основной блок программы
if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices('data/')
    pm.export_to_html('price_list.html')

    while True:
        print(f"----------------------------------------------------------------------------------------------")
        user_input = input("Введите фрагмент названия товара для поиска (или 'exit' для завершения): ")
        if user_input.lower() == 'exit':
            break

        results = pm.find_text(user_input)
        if len(results) > 0:
            print(f"Найдено {len(results)} позиций:")
            print(f"----------------------------------------------------------------------------------------------")
            print(f"№   {'Наименование':<{pm.name_length}} {'Цена':>10} {'Вес':>5} {'Файл':>11} {'Цена за кг.':>20}")
            print(f"----------------------------------------------------------------------------------------------")
            for index, name, price, weight, filename, price_per_kg in results:
                print(
                    f"{index:<3} {name:<{pm.name_length}} {price:>10,.2f} {weight:>5,.2f} {os.path.basename(filename):<20} {price_per_kg:>10,.2f}")
        else:
            print("Товар не найден.")

    print("\nРабота завершена.")