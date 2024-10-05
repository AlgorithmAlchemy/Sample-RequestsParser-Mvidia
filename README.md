# MVideo Parser

Этот проект предназначен для парсинга данных о товарах с сайта MVideo. Он позволяет извлекать идентификаторы товаров, названия и цены, а также сохранять их в базе данных SQLite.

## Установка

1. Клонируйте этот репозиторий:

   ```bash
   git clone <https://github.com/AlgorithmAlchemy/MvidiaRequestsParser/tree/main>
2. Перейдите в директорию проекта:
   ```bash
   cd <имя директории>
3. Установите зависимости:

   pip install -r requirements.txt

### Использование
Для запуска парсера выполните:
   ```bash
python Parser.py
```


Где `Parser.py` — это имя вашего основного Python файла.

При запуске программы вам будет предложено выбрать действие:

- **Parsing tovar id** - парсинг идентификаторов товаров.
- **Parsing tovar name** - парсинг названий товаров.
- **Parsing tovar price** - парсинг цен товаров.
- **Parsing tovar name and price** - парсинг названий и цен товаров.
- **Delete all data and Parsing all date & convert csv** - удалить все данные и выполнить парсинг.
- **No drop base date - Parsing all data & convert csv** - выполнить парсинг без удаления данных.
- **Only convert data to csv** - только конвертация данных в CSV.
- **Delete all date** - удалить все данные из базы.
- **Delete id base** - удалить только идентификаторы.
- **Delete info base (name/price)** - удалить только информацию о названиях и ценах.
- **Close program** - закрыть программу.

### Примечания

- Убедитесь, что у вас установлены все необходимые библиотеки из `requirements.txt`.
- Обязательно проверьте, что ваши куки и заголовки для запросов правильно настроены.


