from hazm import Normalizer
import datetime


def normalize_item(item, ad_type):
    for k, v in item.items():
        if k != 'url' and k != 'thumbnail' and isinstance(v, str) and k != 'title' and k != 'description':
            item[k] = remove_extra_character_and_normalize(v)
        elif k == 'title' or k == 'description':
            item[k] = normalize_text(v)

def normalize_text(text: str):
    n = Normalizer()
    try:
        text = n.normalize(text)
        text = text.replace('‌', ' ')
        text = text.replace('"', ' ')
        text = text.replace("'", ' ')
        text = text.replace("\\", ' ')
        return text
    except:
        return None

def remove_extra_character_and_normalize(text: str, listing=False, check_space=True):
    text = normalize_text(text)
    text = convert_digits(text)
    if check_space:
        text = check_space_with_digit(text)
    text = remove_extra("(", text)
    text = remove_extra(")", text)
    text = remove_extra("-", text)
    text = remove_extra("_", text)
    text = remove_extra(",", text)
    text = remove_extra("،", text)
    text = remove_extra("*", text)
    text = remove_extra("/", text)
    text = remove_extra(".", text)
    text = remove_extra("#", text)
    text = remove_extra("%", text)
    text = remove_extra("$", text)
    text = remove_extra("=", text)
    text = remove_extra("+", text)
    text = remove_extra("\\", text)
    text = remove_extra("<", text)
    text = remove_extra(">", text)
    text = remove_extra("|", text)
    text = remove_extra("[", text)
    text = remove_extra("]", text)
    text = remove_extra("{", text)
    text = remove_extra("}", text)
    if listing:
        return [t.strip() for t in text.split()]
    return " ".join([t.strip() for t in text.split()])


def remove_extra(key, text: str):
    c_index = text.find(key)
    if c_index + 1 >= len(text) or c_index <= 0:
        return text.replace(key, "")
    if text[c_index + 1] == " " or text[c_index - 1] == " ":
        return text.replace(key, "")
    return text.replace(key, " ")


def convert_digits(text: str):
    result = ""
    for c in text:
        if c == '۰':
            result += '0'
        elif c == '۱':
            result += '1'
        elif c == '۲':
            result += '2'
        elif c == '۳':
            result += '3'
        elif c == '۴':
            result += '4'
        elif c == '۵':
            result += '5'
        elif c == '۶':
            result += '6'
        elif c == '۷':
            result += '7'
        elif c == '۸':
            result += '8'
        elif c == '۹':
            result += '9'
        else:
            result += c
    return result


def normalize_and_compare(c1, c2):
    if isinstance(c1, str) and isinstance(c2, str):
        c1 = normalize_text(c1)
        c2 = normalize_text(c2)
    return c1 == c2


def check_space_with_digit(text: str):
    result = ""
    for t in text:
        if t.isdigit() and not result[-1:].isdigit() and result[-1:] != " ":
            result += " " + t

        elif result[-1:].isdigit() and not t.isdigit() and t != " ":
            result += " " + t

        else:
            result += t

    return result.strip()


def clean_number(data, int_type=True):
    data = convert_digits(str(data))
    if str(data) == "-1":
        if int_type:
            return int(data)
        return data
    clean_data = "-1"
    for c in str(data):
        if c.isdigit():
            if clean_data == "-1":
                clean_data = ""
            clean_data += c
    if int_type:
        return int(clean_data)
    return clean_data


def convert_alphabetic_number_to_integer(number):
    if number == 'بدون اتاق':
        return 0
    elif number == 'یک':
        return 1
    elif number == 'دو':
        return 2
    elif number == 'سه':
        return 3
    elif number == 'چهار':
        return 4
    else:
        return 5
