import json

with open('/home/ashish/Desktop/relationship books/data.json') as f:
    data = json.load(f)

cnt = 1
for item in data:
    print(str(cnt) + ":")
    print(item['title'])
    print(item['author'])
    cnt += 1