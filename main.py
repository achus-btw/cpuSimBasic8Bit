import json
from os import register_at_fork, stat
from types import resolve_bases
RAM={}
BUS=0b0;
running=True
MicroStep=5;
REGISTERS={
    "pc":0,
    "mar":0,
    "regA":0,
    "regB":0,
    "op":0,
    "ir":0,
    "flag":0b10
}

#################################################
############Control Lines As bitMasks############
#################################################
HLT=0x1<<0
MI=0x1<<1
RI=0x1<<2
RO=0x1<<3
FI=0x1<<4
IO=0x1<<5
II=0x1<<6
AI=0x1<<7
AO=0x1<<8
EO=0x1<<9
SU=0x1<<10
BI=0x1<<11
OI=0x1<<12
CE=0x1<<13
CO=0x1<<14
J=0x1<<15
opCodeDictionary={
    "LDA":0,
    "ADD":1,
    "SUB":2,
    "STA":3,
    "LDI":4,
    "JMP":5,
    "JC":6,
    "JZ":7,
    "OUT":8,
    "HALT":9
}


LI=[CO|MI,RO|II|CE] #load instruction
InstructionLokupPerStep=[
    {#0b00:zero,carry
    0x0:LI+[IO|MI,RO|AI,0],
    0x1:LI+[IO|MI,RO|BI,EO|AI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|FI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|SU|FI],
    0x3:LI+[IO|MI,RI|AO,0],
    0x4:LI+[IO|AI,0,0],
    0x5:LI+[IO|J,0,0],
    0x6:LI+[0,0,0],
    0x7:LI+[0,0,0],
    0x8:LI+[AO|OI,0,0],
    0x9:LI+[HLT,0,0],
    },
    {#0b01:zero,carry
    0x0:LI+[IO|MI,RO|AI,0],
    0x1:LI+[IO|MI,RO|BI,EO|AI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|FI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|SU|FI],
    0x3:LI+[IO|MI,RI|AO,0],
    0x4:LI+[IO|AI,0,0],
    0x5:LI+[IO|J,0,0],
    0x6:LI+[IO|J,0,0],
    0x7:LI+[0,0,0],
    0x8:LI+[AO|OI,0,0],
    0x9:LI+[HLT,0,0],
    },
    {#0b10:zero,carry
    0x0:LI+[IO|MI,RO|AI,0],
    0x1:LI+[IO|MI,RO|BI,EO|AI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|FI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|SU|FI],
    0x3:LI+[IO|MI,RI|AO,0],
    0x4:LI+[IO|AI,0,0],
    0x5:LI+[IO|J,0,0],
    0x6:LI+[0,0,0],
    0x7:LI+[IO|J,0,0],
    0x8:LI+[AO|OI,0,0],
    0x9:LI+[HLT,0,0],
    },
    {#0b11:zero,carry
    0x0:LI+[IO|MI,RO|AI,0],
    0x1:LI+[IO|MI,RO|BI,EO|AI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|FI],
    0x2:LI+[IO|MI,RO|BI,EO|AI|SU|FI],
    0x3:LI+[IO|MI,RI|AO,0],
    0x4:LI+[IO|AI,RI|AO,0],
    0x5:LI+[IO|J,0,0],
    0x6:LI+[IO|J,0,0],
    0x7:LI+[IO|J,0,0],
    0x8:LI+[AO|OI,0,0],
    0x9:LI+[HLT,0,0],
    },
]


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
    REGISTERS["flag"]=REGISTERS["flag"] & 0b11
def step():
    global MicroStep,running,BUS
    MicroStep=(MicroStep+1) % 0x05
    opCode=(REGISTERS['ir']>>4)&0b1111
    print(f"Flag: {REGISTERS['flag']}, OpCode: {opCode}, Step: {MicroStep}")
    state = InstructionLokupPerStep[REGISTERS["flag"]][opCode][MicroStep]
    aluOut=(REGISTERS["regA"]+REGISTERS["regB"]) & 0xFF
    if state & SU:
        aluOut=(REGISTERS["regA"]-REGISTERS["regB"]) & 0xFF

    if (state & HLT):
        running=False
    
    #output processes
    #writing to bus
    if state &AO:
        BUS=REGISTERS["regA"]
    if state & (EO):
        BUS=aluOut
    if state & RO:
        BUS=RAM[REGISTERS["mar"]]
    if state & IO:
        BUS= REGISTERS["ir"]&0x0f
    if state & CO:
        BUS = REGISTERS["pc"] & 0xFF
    ##reading from BUS
    if state & CE:
        REGISTERS['pc']=(REGISTERS['pc']+1)&0xff
    if state & MI:
        REGISTERS['mar']=BUS & 0xf
    if state & RI:
        RAM[REGISTERS["mar"]]=BUS
    if state & FI:
        REGISTERS["flag"]
    if state & II:
        REGISTERS["ir"]=BUS
    if state & AI:
        REGISTERS["regA"]=BUS
    if state & BI:
        REGISTERS["regB"]=BUS
    if state & OI:
        REGISTERS["op"]=BUS
    if state & J:
        REGISTERS["pc"]=BUS & 0xFF



    

def printState():
    output = ", ".join([f"{k:>3}: 0x{v:02x}" for k, v in REGISTERS.items()])
    print(f"reg: {output}")
    print(f"microStep:{MicroStep}")
    print(f"ram: {list(map(hex, RAM))}")


def main():
    printState()
    while True:
        checkLimits()
        input()
        step()
        printState()
    
if __name__ == "__main__":
    main()
