class Record:
    
    def __init__(self,line):
        self.when = line[0:19]#change to find date format
        self.rain_accum = line[line.find("Rc")+3:line.find(",",line.find("Rc"))-1]
        self.rain_dur = line[line.find("Rd")+3:line.find(",",line.find("Rd"))-1]
        self.rain_inten = line[line.find("Ri")+3:line.find(",",line.find("Ri"))-1]
        self.air_temp = line[line.find("Ta")+3:line.find(",",line.find("Ta"))-1]
        self.supply_V = line[line.find("Vs")+3:line.find(",",line.find("Vs"))-1]
        self.ref_V = line[line.find("Vr")+3:line.find(",",line.find("Vr"))-1]
