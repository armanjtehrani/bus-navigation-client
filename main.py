import _thread
import time

from bus import *


BUS_TOKENS = [
"oiuytr", #hengam
 "iuytre",
 "uytrew",
"zxcvbn",#Res
"xcvbnm",
"mnbvcx",
"qwerty",#Bahg
"wertyu",
"ertyui",
]



ALL_BUS_TOKENS = [
 "oiuytr", #hengam
 "iuytre",
 "uytrew",
 "ytrewq",
 "qazwsx",
 "wsxedc",
 "edcrfv",
 "rfvtgb",
"zxcvbn",#Res
"xcvbnm",
"mnbvcx",
"nbvcxz",
"lkjhgf",
"kjhgfd",
"jhgfds",
"hgfdsa",
"poiuyt",
"qwerty",#Bahg
"wertyu",
"ertyui",
"rtyuio",
"tyuiop",
"asdfgh",
"sdfghj",
"dfghjk",
"fghjkl",
]


if __name__ == "__main__":
    bus_list = []
    for token in BUS_TOKENS:
        bus_list.append(Bus(token))
    for bus in bus_list:
        bus.start()
