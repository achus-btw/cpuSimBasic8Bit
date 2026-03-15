import json
marSize=4;
ramSize=2**marSize;
#ram file

with open('ram.json','w') as file:
    data=[0]*ramSize
    json.dump(data,file)

