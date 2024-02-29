from gpiozero import DigitalOutputDevice, DigitalInputDevice
from pinout import *
from time import sleep

ce = DigitalOutputDevice(pin=ce_pin, active_high=False)
oe = DigitalOutputDevice(pin=oe_pin, active_high=False)
we = DigitalOutputDevice(pin=we_pin, active_high=False)

io: list[DigitalOutputDevice] = list()
adr: list[DigitalOutputDevice] = list()
for pin in io_pin_list:
    io.append(DigitalOutputDevice(pin=pin))
for pin in adr_pin_list:
    adr.append(DigitalOutputDevice(pin=pin))

var1 = int(input("0x"), 16)
var2 = int(input("0x"), 16)
input_var = int(input("0x"), 16)

if (
    (var1 > 0x8000 or var2 > 0x8000)
    or (var1 < 0x0000 or var2 < 0x0000)
    or (0 > input_var > 0xFF)
):
    print(var1, var2)
    exit()

for cadr in range(var1, var2):
    for i in range(15):
        adr[i].value = (cadr >> i) & 1
    ce.on()
    we.on()
    for i in range(8):
        io[i].value = (input_var >> i) & 1
    sleep(0.0001)
    we.off()
    print(hex(cadr))
    io[7].close()
    io7 = DigitalInputDevice(pin=io_pin_list[7], pull_up=False)
    oe.on()
    io7_value = io7.value
    while io7_value != (input_var >> 7) & 1:
        oe.off()
        print(hex(cadr), io7_value, (input_var >> 7) & 1)
        sleep(0.00005)
        oe.on()
        sleep(0.00001)
        io7_value = io7.value
    oe.off()
    ce.off()
    io7.close()
    io[7] = DigitalOutputDevice(pin=io_pin_list[7])
