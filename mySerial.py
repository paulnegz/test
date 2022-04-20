from periphery import Serial
# serial using USB
uart1 = Serial("/dev/ttyS1", 115200)
uart1.flush()
def send(value):
    try: 
        uart1.write(bytes(value, 'utf-8'))
    except KeyboardInterrupt:
        uart1.close()
