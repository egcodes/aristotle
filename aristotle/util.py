def is_ascii(self, s):
    return all(ord(c) < 128 for c in s)


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
            except:
                count -= 1
                index = length - 10
                continue
    return val
