def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def non_zero_date(date):
    date = str(date)
    if date[0] == "0":
        return date[1:]
    else:
        return date


def add_www(link):
    if "www." in link:
        return "www."
    else:
        return ""


def add_slash(href):
    if href[0] == "/":
        return ""
    else:
        return "/"


def trim_str(val, length):
    index = length
    if len(val) >= length:
        count = 10
        while count:
            try:
                if is_ascii(val[index]):
                    val = val[:index] + '...'
                    break
                count -= 1
                index -= 1
            except Exception as e:
                count -= 1
                index -= 1
                continue
    return val


def removeNewlines(var):
    return var.strip().replace("\n", " ")
