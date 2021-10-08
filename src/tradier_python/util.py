def ensure_list(data, key1, key2=None):
    if key2 is None:
        key2 = key1[:-1]

    if data[key1].get(key2) is None:
        data[key1][key2] = []
    elif not isinstance(data[key1].get(key2), list):
        data[key1][key2] = [data[key1][key2]]
    return data
