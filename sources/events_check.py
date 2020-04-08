import evdev
from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice("/dev/input/event16")
print(gamepad)
for event in gamepad.read_loop():
    #print(categorize(event))
    if event.type == ecodes.EV_KEY:
        print(event.value)
        print(event.code)