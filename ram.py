import json
data={}
with open('ram.json', 'r') as file:
    data = json.load(file)
    while True:
        for i, value in enumerate(data):
            print(f"{hex(i)}:{hex(value)}")
        inp=input("enter index or x to close: ")
        if inp=="x":
            break
        try:
            idx=int(inp,0)
        except ValueError:
            print("not a number")
            continue
        if idx>=0 and idx<len(data):
            data[idx]=int(input("enter value: "),0)

with open('ram.json', 'w') as file:
    json.dump(data,file)



