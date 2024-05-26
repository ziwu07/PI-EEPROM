from gpiozero import DigitalOutputDevice, DigitalInputDevice
from EEPROM_INFO import *
from time import sleep
import sys, os

ce = DigitalOutputDevice(pin=CE_PIN, active_high=False)
oe = DigitalOutputDevice(pin=OE_PIN, active_high=False)
we = DigitalOutputDevice(pin=WE_PIN, active_high=False)

io: list[DigitalOutputDevice] = list()
adr: list[DigitalOutputDevice] = list()
for pin in IO_PINS:
    io.append(DigitalOutputDevice(pin=pin))
for pin in ADDR_PINS:
    adr.append(DigitalOutputDevice(pin=pin))

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = input("file:")


file_size = os.path.getsize(filename=file_name)
if file_size != EEPROM_SIZE:
    print(file_size)
    exit()

file = open(file_name, "rb")
data_arr = []
byte = file.read(1)
while byte:
    data_arr.append(int.from_bytes(byte))
    byte = file.read(1)

for page_value in range(0, EEPROM_SIZE >> 6):
    # set page addr
    for i in range(0, 9):
        adr[i + 6].value = (page_value >> i) & 1

    ce.on()
    # set addr in page
    for i in range(0, 6):
        adr[i].value = 0

    last_adr = 0
    addr = page_value << 6
    data = data_arr[addr]
    # set data
    for i in range(8):
        io[i].value = (data >> i) & 1

    # for 64 addr in current page
    for cadr in range(0x1, 0b1000000):
        we.on()
        addr += 1
        sleep(0.000001)
        # swap addr
        for i in range(0, int.bit_count(cadr ^ last_adr)):
            adr[i].toggle()
        last_adr = cadr
        we.off()
        # set data
        data = data_arr[addr]
        for i in range(8):
            io[i].value = (data >> i) & 1
        sleep(0.000001)

    we.on()
    sleep(0.000001)
    we.off()


    io[7].close()
    io7 = DigitalInputDevice(pin=IO_PINS[7], pull_up=False)
    oe.on()
    io7_value = io7.value

    while io7_value != (data >> 7) & 1:
        oe.off()
        sleep(0.00005)
        oe.on()
        sleep(0.00001)
        io7_value = io7.value

    oe.off()
    ce.off()
    io7.close()
    io[7] = DigitalOutputDevice(pin=IO_PINS[7])
