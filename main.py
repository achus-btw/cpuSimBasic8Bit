import json
RAM={}
BUS=0b0;
REGISTERS={
    "pc":0,
    "mar":0,
    "regA":0,
    "regB":0,
    "op":0,
    "ir":0,
    "flag":0b10
}
StateControls=[
    "hlt",
    "pcInc",
    "pcJ",
    "pco",
    "mi",
    "ri",
    "ro",
    "iri",
    "iro"
    "rAi",
    "rAo",
    "rBi",
    "aluo",
    "alusub",
    "oRegIn",
    "flagI"
]
#todo:encode microcode(rom data) into the instruction lookup
InstructionLokup={}


with open('ram.json', 'r') as file:
    data = json.load(file)
    RAM=data

def checkLimits():
    REGISTERS["pc"]=REGISTERS["pc"] & 0xFF
    REGISTERS["mar"]=REGISTERS["mar"] & 0x0F
    REGISTERS["regA"]=REGISTERS["regA"] & 0xFF
    REGISTERS["regB"]=REGISTERS["regB"] & 0xFF
    REGISTERS["op"]=REGISTERS["op"] & 0xFF
    REGISTERS["ir"]=REGISTERS["ir"] & 0xFF
    REGISTERS["flag"]=REGISTERS["flag"] & 0b10




