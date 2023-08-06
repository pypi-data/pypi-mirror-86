import json

module = 'Python JSON Handler - hJson'


def save(filename, data):
    print(f'[hJson] [Try] Saving "{filename}"...')
    with open(filename, encoding='utf-8', mode='w') as f:
        json.dump(data, f, sort_keys=True,
                  separators=(',', ' : '), ensure_ascii=False)
    print(f'[hJson] [Success] Saved "{filename}"!')
    return data


def load(filename):
    print(f'[hJson] [Try] Loading "{filename}"...')
    with open(filename, encoding='utf-8', mode='r') as f:
        data = json.load(f)
    print(f'[hJson] [Success] Loaded "{filename}"!')
    return data


def check(filename):
    print(f'[hJson] [Try] Checking whether "{filename}" exists...')
    try:
        load(filename)
        print(f'[hJson] [Success] Found "{filename}"!')
        return True
    except FileNotFoundError:
        print(f'[hJson] [Fail] "{filename}" does not exist..?')
        return False
    except json.decoder.JSONDecodeError:
        print(f'[hJson] [Fail] "{filename}" is not a valid Json file..?')
        return False
