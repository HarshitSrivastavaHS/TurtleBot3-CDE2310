#cde2310

#this code is used to interface with ads1115

from smbus2 import SMBus
import time

#Enter i2c channel
i2c_ch = 1

#define i2c address

i2c_address = 0x48

#define registers that will be used 
reg_config = 0x01
reg_conversion = 0x00

#setup here
bus = SMBus(i2c_ch)
config = [0xC3, 0x83]



#continuously read data here
while True:
    bus.write_i2c_block_data(i2c_address, reg_config, config)
    time.sleep(0.01)
    result = bus.read_i2c_block_data(i2c_address, reg_conversion, 2) #block length 2
    print(bin(result[0]))
    print(bin(result[1]))

    value = ((result[0]) <<8 |result[1])

    print(bin(value))

    if value & 0x8000 != 0:
        value -= 1 << 16
    v = value * 4096 / 32768
    v = v / 1000

    print(f"A0:{v}V")
    time.sleep(1)