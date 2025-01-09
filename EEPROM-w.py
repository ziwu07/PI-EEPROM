from gpiozero import DigitalOutputDevice, DigitalInputDevice
from EEPROM-INFO import *
from time import sleep

ce = DigitalOutputDevice(pin=CE_PIN, active_high=False)
oe = DigitalOutputDevice(pin=OE_PIN, active_high=False)
we = DigitalOutputDevice(pin=WE_PIN, active_high=False)

io: list[DigitalOutputDevice] = list()
adr: list[DigitalOutputDevice] = list()
for pin in IO_PINS:
    io.append(DigitalOutputDevice(pin=pin))
for pin in ADDR_PINS:
    adr.append(DigitalOutputDevice(pin=pin))

adr1 = int(input("0x"), 16)
adr2 = int(input("0x"), 16)
input_var = int(input("0x"), 16)

if (
    (adr1 > 0x8000 or adr2 > 0x8000)
    or (adr1 < 0x0000 or adr2 < 0x0000)
    or (0 > input_var > 0xFF)
):
    print(adr1, adr2)
    exit()

for cadr in range(adr1, adr2):
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
    io7 = DigitalInputDevice(pin=IO_PINS[7], pull_up=False)
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
    io[7] = DigitalOutputDevice(pin=IO_PINS[7])
