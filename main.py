import time
from pyrogram import Client
import random
from config import num_of_users, first_username, second_username, third_username, fourth_username, time_sleep, acc_for_notification, mcap, stars_for_each, parsing_cooldown, max_supply, tg_number_for_parse_acc, tg_number_for_buy_acc
from loguru import logger

# API ключи, можно взять на https://my.telegram.org/auth

parsing_acc_api_id = 1111111
parsing_acc_api_hash = "11111111"

acc_with_stars_api_id = 111111
acc_with_stars_api_hash = "11111111"

#список что бы не обращать внимание на подарки которые уже вышли
gift_list = [5879737836550226478, 5882125812596999035, 5882252952218894938, 5859442703032386168, 5857140566201991735,
             5856973938650776169, 5846226946928673709, 5846192273657692751, 5845776576658015084, 5825801628657124140,
             5825480571261813595, 5843762284240831056, 5841689550203650524, 5841632504448025405, 5841391256135008713,
             5839038009193792264, 5841336413697606412, 5837063436634161765, 5836780359634649414, 5837059369300132790,
             5821384757304362229, 5821205665758053411, 5821261908354794038, 5782984811920491178, 5782988952268964995,
             5783075783622787539, 5167939598143193218, 5170594532177215681, 5825895989088617224, 5913517067138499193,
             5915550639663874519, 5915521180483191380, 5915733223018594841, 5915502858152706668, 5913442287462908725,
             5936013938331222567, 5933671725160989227, 5933629604416717361, 5933531623327795414, 5936085638515261992,
             5936043693864651359, 5935936766358847989, 5936017773737018241, 5933590374185435592, 5981026247860290310,
             5980789805615678057, 5981132629905245483, 5983471780763796287, 5983259145522906006, 5983484377902875708,
             6001473264306619020, 6003735372041814769, 6003643167683903930, 6001538689543439169, 6003767644426076664,
             6003373314888696650, 6023752243218481939, 6023679164349940429, 6023917088358269866, 6028426950047957932, 6028283532500009446]

def buy_nft(num_of_gifts, gif_id):
    with Client("acc_with_stars", acc_with_stars_api_id, acc_with_stars_api_hash) as app2:
        for i in range(num_of_gifts):
            try:
                if num_of_users == 1:
                    time.sleep(time_sleep)
                    app2.send_star_gift(first_username, star_gift_id=gif_id)
                if num_of_users == 2:
                    time.sleep(time_sleep)
                    app2.send_star_gift(first_username, star_gift_id=gif_id)
                    time.sleep(time_sleep)
                    app2.send_star_gift(second_username, star_gift_id=gif_id)
                if num_of_users == 3:
                    time.sleep(time_sleep)
                    app2.send_star_gift(first_username, star_gift_id=gif_id)
                    time.sleep(time_sleep)
                    app2.send_star_gift(second_username, star_gift_id=gif_id)
                    time.sleep(time_sleep)
                    app2.send_star_gift(third_username, star_gift_id=gif_id)
                if num_of_users == 4:
                    time.sleep(time_sleep)
                    app2.send_star_gift(first_username, star_gift_id=gif_id)
                    time.sleep(time_sleep)
                    app2.send_star_gift(second_username, star_gift_id=gif_id)
                    time.sleep(time_sleep)
                    app2.send_star_gift(third_username, star_gift_id=gif_id)
                    time.sleep(time_sleep)
                    app2.send_star_gift(fourth_username, star_gift_id=gif_id)
            except Exception as e:
                logger.error(f"подарок не был отправлен, повторяем попытку, ошибка:{e}")

# Функція для витягання id та emoji з даних
def extract_gift_info(gifts):
    for gift in gifts:
        if gift.id not in gift_list:
            if gift.is_limited == True:
                print(gift)
                gift_list.insert(0, gift.id)
                market_cup = int(gift.price)*int(gift.total_amount)*0.015
                app.send_message(acc_for_notification, f"{gift.id, gift.sticker.emoji, market_cup}")
                if market_cup <= mcap:
                    if int(gift.total_amount) <= int(max_supply):
                        num_of_gifts_false = round(stars_for_each/gift.price)
                        remainder = num_of_gifts_false % num_of_users
                        if remainder == 0:
                            nearest_number = num_of_gifts_false  # Якщо число вже ділиться націло
                        elif remainder <= num_of_users / 2:
                            nearest_number = num_of_gifts_false - remainder  # Округлення вниз
                        else:
                            nearest_number = num_of_gifts_false + (num_of_users - remainder)  # Округлення вгору
                        gifts_per_acc = nearest_number/num_of_users
                        buy_nft(int(gifts_per_acc), gift.id)


# Функція для знаходження нових подарунків
def find_new_gifts(current, previous):
    previous_ids = {gift["id"] for gift in previous}
    return [gift for gift in current if gift["id"] not in previous_ids]

print("сейчас прийдёт код на аккаунт для парсинга")
with Client("parsing_acc", parsing_acc_api_id, parsing_acc_api_hash, phone_number=tg_number_for_parse_acc) as app:
    app.send_message("me", "скрипт запущен")
    print("сейчас прийдёт код на аккаунт для покупки")
    with Client("acc_with_stars", acc_with_stars_api_id, acc_with_stars_api_hash, phone_number=tg_number_for_buy_acc) as app2:
        pass
    while True:
        try:
            time.sleep(parsing_cooldown)
            current_gifts = app.get_star_gifts()
            extract_gift_info(current_gifts)
            current_time = time.strftime("%H:%M:%S", time.localtime())
            logger.success(f'Парсинг проводится успешно {current_time}')
        except Exception as e:
            pass
