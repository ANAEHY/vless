# update_vless.py — автообновление Vless ключей с проверкой
import socket
import random
import time

# Запасные ключи (твои реальные запасные — добавь 10–50 штук)
BACKUP_KEYS = [
   "vless://681a694f-7242-4410-b7a0-57106933637d@5.175.134.3:81?type=xhttp&security=reality&fp=&pbk=Rb6WZ6zv_UlQcRiy33kUft1JlTKZ2KGgJt-CvVC5pSI&sid=cf&sni=xapi.ozon.ru&host=xapi.ozon.ru&mode=auto#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%20%5BSNI-RU%5D%20xapi.ozon.ru",
  "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpvWklvQTY5UTh5aGNRVjhrYTNQYTNB@82.38.31.62:8080?#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Noord%29%20%5BBL%5D",
  "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprMWRCT21PQjRvcWk3VW1wMzdhMWJR@82.38.31.214:8080#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Noord%29%20%5BBL%5D",
  "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprMWRCT21PQjRvcWk3VW1wMzdhMWJR@82.38.31.217:8080#%F0%9F%87%B3%F0%9F%87%B1%20The%20Netherlands%2C%20Amsterdam%20%28Amsterdam-Noord%29%20%5BBL%5D",
  
]

def is_key_alive(key: str) -> bool:
    try:
        # Парсим host и port из vless://uuid@host:port?...
        parts = key.split('@')[1].split(':')
        host = parts[0]
        port_str = parts[1].split('?')[0]
        port = int(port_str)

        # Тест подключения (timeout 5 сек)
        sock = socket.create_connection((host, port), timeout=5)
        sock.close()
        print(f"Живой ключ: {key[:50]}...")
        return True
    except Exception as e:
        print(f"Мёртвый ключ: {key[:50]}... → {e}")
        return False

def update_keys():
    input_file = "vless.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and line.startswith("vless://")]

        if not lines:
            print("Нет ключей в файле")
            return

        new_lines = []
        replaced_count = 0

        for line in lines:
            if is_key_alive(line):
                new_lines.append(line)
            else:
                if BACKUP_KEYS:
                    replacement = random.choice(BACKUP_KEYS)
                    new_lines.append(replacement)
                    replaced_count += 1
                    print(f"Заменён → {replacement[:50]}...")
                else:
                    new_lines.append(line)  # если нет запасных — оставляем как есть

        # Перезаписываем файл
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")

        print(f"Обновлено! Заменено: {replaced_count}/{len(lines)} ключей")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    print("Запуск теста...")
    update_keys()
