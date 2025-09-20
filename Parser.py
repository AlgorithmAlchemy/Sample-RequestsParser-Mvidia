import csv
import json
import logging
import requests
import sqlite3
import time
import urllib3

urllib3.disable_warnings()

translator = Translator()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.FATAL)

db = sqlite3.connect('bd.sqlite')
connect = db.cursor()


# Функция для создания таблиц
def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS xboxe_id (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        item_id TEXT,
        UNIQUE (item_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS playstation_id_ps5 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        item_id TEXT,
        UNIQUE (item_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS playstation_id_ps4 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        item_id TEXT,
        UNIQUE (item_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nintendo_id (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        item_id TEXT,
        UNIQUE (item_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        item_id TEXT,
        tovar_price TEXT,
        tovar_category TEXT,
        UNIQUE (item_id)
    )''')


create_tables(cursor)

cookies = {
    'CACHE_INDICATOR': 'false',
    'COMPARISON_INDICATOR': 'false',
    'HINTS_FIO_COOKIE_NAME': '2',
    'MAIN_PAGE_VARIATION_1': '2',
    'MVID_2_exp_in_1': '2',
    'MVID_AB_SERVICES_DESCRIPTION': 'var4',
    'MVID_ADDRESS_COMMENT_AB_TEST': '2',
    'MVID_BLACK_FRIDAY_ENABLED': 'true',
    'MVID_CALC_BONUS_RUBLES_PROFIT': 'false',
    'MVID_CART_MULTI_DELETE': 'false',
    'MVID_CATALOG_STATE': '1',
    'MVID_CITY_ID': 'CityCZ_975',
    'MVID_FILTER_CODES': 'true',
    'MVID_FILTER_TOOLTIP': '1',
    'MVID_FLOCKTORY_ON': 'true',
    'MVID_GEOLOCATION_NEEDED': 'true',
    'MVID_GET_LOCATION_BY_DADATA': 'DaData',
    'MVID_GIFT_KIT': 'true',
    'MVID_GUEST_ID': '20867510091',
    'MVID_IS_NEW_BR_WIDGET': 'true',
    'MVID_KLADR_ID': '7700000000000',
    'MVID_LAYOUT_TYPE': '1',
    'MVID_LP_SOLD_VARIANTS': '0',
    'MVID_NEW_ACCESSORY': 'true',
    'MVID_NEW_DESKTOP_FILTERS': 'true',
    'MVID_NEW_LK': 'true',
    'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
    'MVID_NEW_LK_LOGIN': 'true',
    'MVID_NEW_LK_MENU_BUTTON': 'true',
    'MVID_NEW_LK_OTP_TIMER': 'true',
    'MVID_NEW_MBONUS_BLOCK': 'true',
    'MVID_NEW_SUGGESTIONS': 'true',
    'MVID_PDP_MAP_DEFAULT': '1',
    'MVID_PROMO_CATALOG_ON': 'true',
    'MVID_REGION_ID': '1',
    'MVID_REGION_SHOP': 'S002',
    'MVID_SERVICES': '111',
    'MVID_SERVICES_MINI_BLOCK': 'var2',
    'MVID_TAXI_DELIVERY_INTERVALS_VIEW': 'old',
    'MVID_TIMEZONE_OFFSET': '3',
    'MVID_WEBP_ENABLED': 'true',
    'NEED_REQUIRE_APPLY_DISCOUNT': 'true',
    'PICKUP_SEAMLESS_AB_TEST': '2',
    'PRESELECT_COURIER_DELIVERY_FOR_KBT': 'true',
    'PROMOLISTING_WITHOUT_STOCK_AB_TEST': '2',
    'searchType2': '2',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_gid': 'GA1.2.529201000.1655041498',
    '_ym_uid': '1655041498167988451',
    '_ym_d': '1655041498',
    'st_uid': '825b7d5ee39c6bbbbfd256545a2ea1cc',
    'tmr_lvid': '72ec0c03a55fa32f34f772c41eb0f420',
    'tmr_lvidTS': '1655041498610',
    'advcake_track_id': '7dac8892-29f9-4099-9131-71f2bdd7d472',
    'advcake_session_id': 'f11f66c1-eb0e-d5f8-110e-7a6c4fac0c95',
    'gdeslon.ru.__arc_domain': 'gdeslon.ru',
    'gdeslon.ru.user_id': 'a20a3d27-1187-4339-894d-d392de61e8f3',
    '_ym_isad': '2',
    'afUserId': 'c77ae91f-b332-4397-8027-94726b809298-p',
    'flocktory-uuid': 'd8c1e6fa-ad4b-4b7b-8845-56c7377b6714-4',
    'AF_SYNC': '1655041499962',
    'adrdel': '1',
    'adrcid': 'A5hrWSi919zaE4KM6YUC5UA',
    'uxs_uid': 'db3eabc0-ea55-11ec-be9a-0120f2de5bab',
    'flacktory': 'no',
    'MVID_ENVCLOUD': 'primary',
    '__lhash_': 'fe64d44a4010d930ed63e4ca7cf67e50',
    'SMSError': '',
    'authError': '',
    '_dc_gtm_UA-1873769-1': '1',
    '_dc_gtm_UA-1873769-37': '1',
    'mindboxDeviceUUID': '7caa7169-b131-45dc-a220-949a5e206e90',
    'directCrm-session': '%7B%22deviceGuid%22%3A%227caa7169-b131-45dc-a220-949a5e206e90%22%7D',
    '_ga_CFMZTSS5FM': 'GS1.1.1655044522.2.1.1655045526.0',
    '_ga_BNX5WPP3YK': 'GS1.1.1655044522.2.1.1655045526.6',
    '_ga': 'GA1.2.86733540.1655041498',
    'tmr_detect': '0%7C1655045529970',
    'tmr_reqNum': '57',
    'JSESSIONID': 'Dhf4vl9htkTyTk3jc5xWLFmhJTY4L2z3dQcB1vMMmx1LnCgTvMys!-1855659811',
    'bIPs': '-1707567431',
    'ADRUM_BT': 'R:53|g:718f0ee4-2152-4f75-8fd6-e76cd009bb12879945',
}

headers = {
    'Host': 'www.mvideo.ru',
    'Sec-Ch-Ua': '"-Not.A/Brand";v="8", "Chromium";v="102"',
    'Accept': 'application/json',
    'X-Set-Application-Id': '3eed2cf1-93ad-4d90-ac2c-77f44d7ef6eb',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.mvideo.ru/playstation-4327/ps5-igry-22780',
    'Accept-Language': 'en-US,en;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'CACHE_INDICATOR=false; COMPARISON_INDICATOR=false; HINTS_FIO_COOKIE_NAME=2; MAIN_PAGE_VARIATION_1=2; MVID_2_exp_in_1=2; MVID_AB_SERVICES_DESCRIPTION=var4; MVID_ADDRESS_COMMENT_AB_TEST=2; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CALC_BONUS_RUBLES_PROFIT=false; MVID_CART_MULTI_DELETE=false; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_975; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GET_LOCATION_BY_DADATA=DaData; MVID_GIFT_KIT=true; MVID_GUEST_ID=20867510091; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7700000000000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=0; MVID_NEW_ACCESSORY=true; MVID_NEW_DESKTOP_FILTERS=true; MVID_NEW_LK=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_LOGIN=true; MVID_NEW_LK_MENU_BUTTON=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_NEW_SUGGESTIONS=true; MVID_PDP_MAP_DEFAULT=1; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=1; MVID_REGION_SHOP=S002; MVID_SERVICES=111; MVID_SERVICES_MINI_BLOCK=var2; MVID_TAXI_DELIVERY_INTERVALS_VIEW=old; MVID_TIMEZONE_OFFSET=3; MVID_WEBP_ENABLED=true; NEED_REQUIRE_APPLY_DISCOUNT=true; PICKUP_SEAMLESS_AB_TEST=2; PRESELECT_COURIER_DELIVERY_FOR_KBT=true; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; searchType2=2; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _gid=GA1.2.529201000.1655041498; _ym_uid=1655041498167988451; _ym_d=1655041498; st_uid=825b7d5ee39c6bbbbfd256545a2ea1cc; tmr_lvid=72ec0c03a55fa32f34f772c41eb0f420; tmr_lvidTS=1655041498610; advcake_track_id=7dac8892-29f9-4099-9131-71f2bdd7d472; advcake_session_id=f11f66c1-eb0e-d5f8-110e-7a6c4fac0c95; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=a20a3d27-1187-4339-894d-d392de61e8f3; _ym_isad=2; afUserId=c77ae91f-b332-4397-8027-94726b809298-p; flocktory-uuid=d8c1e6fa-ad4b-4b7b-8845-56c7377b6714-4; AF_SYNC=1655041499962; adrdel=1; adrcid=A5hrWSi919zaE4KM6YUC5UA; uxs_uid=db3eabc0-ea55-11ec-be9a-0120f2de5bab; flacktory=no; MVID_ENVCLOUD=primary; __lhash_=fe64d44a4010d930ed63e4ca7cf67e50; SMSError=; authError=; _dc_gtm_UA-1873769-1=1; _dc_gtm_UA-1873769-37=1; mindboxDeviceUUID=7caa7169-b131-45dc-a220-949a5e206e90; directCrm-session=%7B%22deviceGuid%22%3A%227caa7169-b131-45dc-a220-949a5e206e90%22%7D; _ga_CFMZTSS5FM=GS1.1.1655044522.2.1.1655045526.0; _ga_BNX5WPP3YK=GS1.1.1655044522.2.1.1655045526.6; _ga=GA1.2.86733540.1655041498; tmr_detect=0%7C1655045529970; tmr_reqNum=57; JSESSIONID=Dhf4vl9htkTyTk3jc5xWLFmhJTY4L2z3dQcB1vMMmx1LnCgTvMys!-1855659811; bIPs=-1707567431; ADRUM_BT=R:53|g:718f0ee4-2152-4f75-8fd6-e76cd009bb12879945',
}

params_ps5 = {
    'categoryId': '22780',
    'offset': '0',
    'limit': '72',
    'doTranslit': 'true',
}

params_ps4 = {
    'categoryId': '4331',
    'offset': '0',
    'limit': '24',
    'filterParams': 'WyJjYXRlZ29yeSIsIiIsImlncnktZGx5YS1wbGF5c3RhdGlvbi00LXBzNC00MzQzIl0=',
    'doTranslit': 'true',
}

params_xboxe = {
    'categoryId': '4338',
    'offset': '0',
    'limit': '24',
    'doTranslit': 'true',
}

params_nintendo = {
    'categoryId': '4929',
    'offset': '0',
    'limit': '24',
    'doTranslit': 'true',
}

params_id_list = [params_xboxe, params_ps5, params_ps4, params_nintendo]  # перечисляем параметры
bd_names = ["xboxe_id", "playstation_id_ps5", "playstation_id_ps4", "nintendo_id"]
platforms = ['PS4', 'PS5', 'Xbox One', 'Xbox', 'Nintendo Switch', 'Nintendo']
end_data = []


# Loading JSON for comparison

def get_games_1c():
    with open('data.json') as f:
        games = []
        templates = json.load(f)

        products = templates['products']

        for product in products:
            game = {}
            game['name'] = product['name']
            game['price'] = product['priceCache']

            for platform in platforms:
                if platform in game['name']:
                    games.append(game)
                    break

        return games  # return the dictionary


def sort_data():
    for i in range(len(end_data) - 1):
        for j in range(i + 1, len(end_data)):
            if end_data[j]['price_difference'] > end_data[i]['price_difference']:
                end_data[j], end_data[i] = end_data[i], end_data[j]


def create_exel():
    print_count = 0
    count = 0
    cursor = db.execute(f'''SELECT * FROM items''')  # We take all the items from the BD for comparison.
    parse_full_list = {}
    parse_list = []
    for itr in cursor:
        parse_original_name = str(itr[1])
        parse_price = str(itr[3])
        game_type = str(itr[4])

        if parse_price is not None:
            if parse_price == "None":
                continue

            parse_name = str(itr[1]).replace("Игра для", "").replace("Игра ", "").replace("PS4 игра ", "") \
                .replace("PS5 игра ", "").replace("Xbox игра ", "").replace("Дополнение для игры . ", "") \
                .replace("Xbox игра ", "").replace("Xbox One игра ", "").strip()

            parse_full_list[parse_name] = {"parse_original_name": parse_name, "type": game_type,
                                           "price": parse_price}

            count += 1

    high_key = list(parse_full_list.keys())
    high_key = high_key[-1]

    json_game = get_games_1c()  # upload our json
    json_double = []
    count = 0
    for jsg in json_game:
        json_original_name = str(jsg['name'])
        json_game_name_type = ""
        if "PS5" in json_original_name:
            json_game_name_type = "PS5"
        elif "PS4" in json_original_name:
            json_game_name_type = "PS4"
        elif "Xbox One" in json_original_name:
            json_game_name_type = "Xbox One"
        elif "Xbox" in json_original_name and "Xbox One" not in json_original_name:
            json_game_name_type = "Xbox"
        elif "Nintendo" in json_original_name and "Nintendo Switch" not in json_original_name:
            json_game_name_type = "nintendo_id"
        elif "Nintendo Switch" in json_original_name:
            json_game_name_type = "Nintendo Switch"
        else:
            continue

        if "Подписка" in json_original_name:
            continue
        if "Цифровая версия игры" in json_original_name:
            continue
        if "Набор для игры" in json_original_name:
            continue
        if "Дополнение для игры" in json_original_name:
            continue
        if "Игровая валюта Xbox" in json_original_name:
            continue
        if "Игровая консоль" in json_original_name:
            continue
        if "TRADE IN" in json_original_name:
            continue
        if "Б/У" in json_original_name:
            continue
        if "Trade" in json_original_name:
            continue

        json_game_name = str(jsg['name']).replace("[PS4]", "").replace("[ Xbox One]", "").replace("PS4", "") \
            .replace(" [Xbox]", "".replace(" [PS5]", "").replace("[PS5]", "")) \
            .replace("[Nintendo Switch]", "").replace("(TRADE IN)", "") \
            .replace("[, русская документация]", "").replace("  (Trade-in)", "") \
            .replace("Microsoft Xbox", "").replace("[PS5] – Trade-in | Б/У", "") \
            .replace(" (только для VR) ", "").replace("[PS5]", "").replace("[Xbox One]", "") \
            .replace("(Хиты PlayStation) ", "").replace("[Nintendo Switch, русская версия]", "") \
            .replace(" – Trade-in | Б/У", "").replace(" [, русская версия]", "").replace("Комплект игр ", "") \
            .replace("дополнение", "").replace("[Xbox One, английская версия] ", "") \
            .replace(" [, русские субтитры]", "").replace("[Nintendo Switch, русские субтитры]", "") \
            .replace("[Xbox Series X] ", "").replace("[Xbox One]", "").replace("[Xbox Series X]", "") \
            .replace(" (512 ГБ) ", "").replace("(1TB)", "").replace("(512 ГБ)", "") \
            .replace("(поддержка VR)", "").strip()

        json_price = str(jsg['price'])

        if count == high_key:
            continue

        # matches = [match for match in parse_full_list if json_game_name in match]
        matches = []

        for match in parse_full_list:  # Comparing the SKL and JSON databases
            if json_game_name in match:
                if parse_full_list[match]['type'] == json_game_name_type:
                    end_data.append({'name': json_original_name, 'price_difference':
                        int(json_price) - int(parse_full_list[match]['price'])})

                    print(f"convert step: {print_count}")
                    print_count += 1

                    matches.append([json_original_name, int(json_price) - int(parse_full_list[match]['price'])])

        count += 1

        if not matches:
            continue
        if len(matches) >= 2:  # removed matches with more than 2 elements
            continue
        if matches in json_double:
            continue
        else:
            json_double.append(matches)

        strin = str(matches[0])

    sort_data()

    with open('result.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')
        writer.writerow(['Название', 'Разница в цене'])
        for data in end_data:
            writer.writerow([data['name'], data['price_difference']])


# we go through all the pages collecting the ID
# we parse the PS5
def parse_id():
    cnt = 0
    print_count = 0
    table_name = None
    for itr_param in params_id_list:
        # BD name depending on parsing parameters
        if itr_param['categoryId'] == "22780":
            table_name = "playstation_id_ps5"
        elif itr_param['categoryId'] == "4331":
            table_name = "playstation_id_ps4"
        elif itr_param['categoryId'] == "4338":
            table_name = "xboxe_id"
        elif itr_param['categoryId'] == "4929":
            table_name = "nintendo_id"

        while True:
            print(f"parse_id step: {print_count}")
            print_count += 1

            cnt += 72
            try:
                response = requests.get('https://www.mvideo.ru/bff/products/listing', params=itr_param, cookies=cookies,
                                        headers=headers, verify=False)
            except requests.exceptions.ConnectionError:
                time.sleep(30)  # если банят
                response = requests.get('https://www.mvideo.ru/bff/products/listing', params=itr_param, cookies=cookies,
                                        headers=headers, verify=False)

            response = json.loads(response.text)

            # If everything is parsed, we exit the loop.
            if not response['body']['products']:
                cnt = 0
                break

            for item_id in response['body']['products']:
                item_name = None
                inf_list = (item_name, item_id)
                try:
                    db.execute(f'''INSERT INTO {table_name}(item_name, item_id) VALUES(?,?)''', inf_list)
                    db.commit()
                except sqlite3.IntegrityError:
                    pass
            itr_param['offset'] = str(cnt)
            time.sleep(5)
        cnt = 0
        if table_name is None:
            break


# parse the game name
def parse_info():
    print_count = 0
    for tovar_category in bd_names:

        print(tovar_category)

        # This is what we send to the user
        json_data = {
            'productIds': [
            ],
            'mediaTypes': [
                'images',
            ],
            'category': True,
            'status': True,
            'brand': True,
            'propertyTypes': [
                'KEY',
            ],
            'propertiesConfig': {
                'propertiesPortionSize': 5,
            },
            'multioffer': False,
        }

        # We are collecting a table with IDs to extract information.
        id_listok = []
        cnt = 0
        cursor = db.execute(f'''SELECT * FROM {tovar_category}''')
        for i in cursor:
            print(f"parse_info step: {print_count}")
            print_count += 1

            id_listok.append(i[2])

            if cnt >= 70:
                json_data['productIds'] = id_listok

                try:
                    response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies,
                                             headers=headers, json=json_data)
                except requests.exceptions.ConnectionError:
                    time.sleep(30)  # if they ban
                    response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies,
                                             headers=headers, json=json_data)

                response = json.loads(response.text)

                cnt = 0
                id_listok = []

                for item_ifno in response['body']['products']:
                    item_name = item_ifno['name']
                    item_price = None
                    item_id = item_ifno['productId']
                    # We extract the true product category to populate the database.
                    tovar_category = str(item_name)
                    if "Подписка" in item_name:
                        continue
                    if "Цифровая версия игры" in item_name:
                        continue
                    if "Набор для игры" in item_name:
                        continue
                    if "Дополнение для игры" in item_name:
                        continue
                    if "Игровая валюта Xbox" in item_name:
                        continue

                    if "Xbox игра" in tovar_category:
                        tovar_category = 'Xbox'
                    elif "Xbox One" in tovar_category:
                        tovar_category = 'Xbox One'
                    elif "PS4" in tovar_category:
                        tovar_category = 'PS4'
                    elif "PS5" in tovar_category:
                        tovar_category = 'PS5'
                    elif "Nintendo" in tovar_category and "Nintendo Switch" not in tovar_category:
                        tovar_category = 'Nintendo'
                    elif "Nintendo Switch" in tovar_category:
                        tovar_category = 'Nintendo Switch'
                    else:
                        continue

                    inf_list = (item_name, item_id, item_price, tovar_category)

                    try:
                        db.execute(f'''INSERT INTO items(item_name, item_id, tovar_price, tovar_category) 
                        VALUES(?,?,?,?)''', inf_list)
                        db.commit()
                    except sqlite3.IntegrityError:
                        pass
                time.sleep(5)

            cnt += 1
        json_data['productIds'] = id_listok

        # we send the rest
        try:
            response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies,
                                     headers=headers, json=json_data)
        except requests.exceptions.ConnectionError:
            time.sleep(30)  # если банят
            response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies,
                                     headers=headers, json=json_data)

        response = json.loads(response.text)


        for item_ifno in response['body']['products']:
            item_name = item_ifno['name']
            item_price = None
            item_id = item_ifno['productId']
            tovar_category = str(item_name)
            if "Подписка" in item_name:
                continue
            if "Цифровая версия игры" in item_name:
                continue
            if "Набор для игры" in item_name:
                continue
            if "Дополнение для игры" in item_name:
                continue
            if "Игровая валюта Xbox" in item_name:
                continue

            if "Xbox игра" in tovar_category:
                tovar_category = 'Xbox'
            elif "Xbox One" in tovar_category:
                tovar_category = 'Xbox One'
            elif "PS4" in tovar_category:
                tovar_category = 'PS4'
            elif "PS5" in tovar_category:
                tovar_category = 'PS5'
            elif "Nintendo" in tovar_category and "Nintendo Switch" not in tovar_category:
                tovar_category = 'Nintendo'
            elif "Nintendo Switch" in tovar_category:
                tovar_category = 'Nintendo Switch'
            else:
                continue

            inf_list = (item_name, item_id, item_price, tovar_category)

            try:
                db.execute(f'''INSERT INTO items(item_name, item_id, tovar_price, tovar_category) 
                VALUES(?,?,?,?)''', inf_list)
                db.commit()
            except sqlite3.IntegrityError:
                pass


def price_parse():
    print_count = 0
    # This is what we send to the user
    params = {
        'productIds': '',
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    # We are collecting a table with IDs to extract information.
    id_str = ""
    cnt = 0
    cursor = db.execute(f'''SELECT * FROM items''')
    for i in cursor:
        print(f"price_parse step: {print_count}")
        print_count += 1

        id_str += i[2] + ","
        if cnt >= 70:
            params['productIds'] = id_str

            try:
                response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                        headers=headers, verify=False)
            except requests.exceptions.ConnectionError:
                time.sleep(30)
                response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                        headers=headers, verify=False)
            response = json.loads(response.text)

            for item_ifno in response['body']['materialPrices']:
                item_price = item_ifno['price']['salePrice']
                item_id = item_ifno['productId']
                db.execute(f'''UPDATE items SET tovar_price = {item_price} WHERE item_id = {item_id}''')
                db.commit()
            cnt = 0
            id_str = ""
            time.sleep(1)
        cnt += 1

    # we send the rest
    params['productIds'] = id_str

    try:
        response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                headers=headers, verify=False)
    except requests.exceptions.ConnectionError:
        time.sleep(30)
        response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                headers=headers, verify=False)
    response = json.loads(response.text)

    for item_ifno in response['body']['materialPrices']:
        item_price = item_ifno['price']['salePrice']
        item_id = item_ifno['productId']
        db.execute(f'''UPDATE items SET tovar_price = {item_price} WHERE item_id = {item_id}''')
        db.commit()


def clear_data(tables):
    for table in tables:
        db.execute(f'DELETE FROM {table}')
    db.commit()
    print("Delete complete")


def parse_actions(action):
    if action == 1:
        parse_id()
    elif action == 2:
        parse_info()
    elif action == 3:
        price_parse()
    elif action == 4:
        parse_info()
        price_parse()
    elif action in (5, 55):
        if action == 5:
            clear_data(['xboxe_id', 'playstation_id', 'nintendo_id', 'items'])
        parse_id()
        parse_info()
        price_parse()
        create_exel()
    elif action == 555:
        create_exel()
    elif action in (6, 7):
        if action == 6:
            clear_data(['xboxe_id', 'playstation_id', 'nintendo_id', 'items'])
        else:
            clear_data(['xboxe_id', 'playstation_id', 'nintendo_id'])
    elif action == 8:
        db.execute('DELETE FROM items')
        db.commit()
        print("Delete complete")
    elif action == 9:
        print("bb")
        exit()
    else:
        print("error!")


def main():
    tables_to_clear = ['xboxe_id', 'playstation_id', 'nintendo_id', 'items']

    while True:
        action = int(input(f"\n#################################################"
                           f"\nWelcome to mvidia parser $creator @ponchikilol$"
                           f"\nParsing tovar id - 1"
                           f"\nParsing tovar name - 2"
                           f"\nParsing tovar price - 3"
                           f"\nParsing tovar name and price - 4"
                           f"\n\nDelete all data and Parsing all date & convert csv - 5"
                           f"\n(No drop base date)Parsing all data & convers csv - 55"
                           f"\nOnly convert data to csv - 555"
                           f"\n\nDelete all date - 6"
                           f"\nDelete id base - 7"
                           f"\nDelete info base (name/price) - 8"
                           f"\n\nClose program - 9"
                           "\nPlease enter num: "))

        parse_actions(action)


main()
