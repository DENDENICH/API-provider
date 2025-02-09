import re
# Из названия класса модели в название таблицы в БД

def camel_case_to_snake_case(camel_case: str) -> str:
    """
    Преобразует CamelCase в snake_case

    :param camel_case: Название в CamelCase
    :return: Название в snake_case
    """
    # snake_case = re.sub(r'([A-Z])', r'_\1', camel_case).lower()
    chars = []
    for i, char in enumerate(camel_case):
        if i and char.isupper():
            i_nxt = i + 1
            # если следующий элемент заглавной буквы или индекс уже превышает длинну строки
            flag = i_nxt >= len(camel_case) or camel_case[i_nxt].isupper()
            prev_char = camel_case[i - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append('_')
        chars.append(char.lower())

    return ''.join(chars)
