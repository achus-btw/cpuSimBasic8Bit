# a basic cpu simator
this is a practice project to understand basics of 
a cpu and its functioning

> it uses python to emulate a basic computer using registers and buses
> the current design choice is to keep registers py dicts
> and logging the data for easy inspection as csv in seperate file

## user guide
 - ### running the sim
 - run `python3 main.py` to start the sim
 - to step through the simulation press ENTER key
 - by default it advances only a clock cycle
 - change simulationStepSize flag at top of main.py to 5 in order to step through a command [to:do]
 - ### editing the program
 - run `python3 ram.py` to edit the ram data
 - refer to code in main.py for opCodes
