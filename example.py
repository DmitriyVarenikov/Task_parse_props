from re import search, findall, sub, match

text = 'гост190113-86ост13616'

# Регулярное выражение для поиска подстрок "гост" или "ост", за которыми следуют цифры
pattern = r'(?:гост|ост)\d+'

# Находим все совпадения
matches = findall(pattern, text)

# Если есть совпадения, берем последнее
last_match = matches[-1] if matches else None

print(last_match)  # Выводит 'гост13616'

data = []
with open(r"test.txt", "r") as file:
    for i in file:
        data.append(i.strip())

for i in data:
    # Находим все совпадения
    matches = findall(pattern, i)

    # Если есть совпадения, берем последнее
    last_match = matches[-1] if matches else None

    print(last_match, "------", i)  # Выводит 'гост13616'