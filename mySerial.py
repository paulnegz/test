# import serial
# serrial using UART
# with serial.Serial(port="/dev/ttyAMA0", baudrate=9600, timeout=.1) as arduino_serial:
#     def send(value):
#         arduino_serial.write(bytes(value, 'utf-8'))
#         arduino_serial.close()

from periphery import Serial

# serial using USB
uart1 = Serial("/dev/ttyS1", 115200)
uart1.flush()
def send(value):
    try: 
        uart1.write(bytes(value, 'utf-8'))
    except KeyboardInterrupt:
        uart1.close()
