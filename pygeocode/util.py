import json

def read_http(res):
    while True:
        data = res.read(4*1024*1024)
        if not data:
            break
        yield data

def read_json(res):
    data = [datum for datum in read_http(res)]
    data = ''.join(data)
    data = json.loads(data)

    return data
