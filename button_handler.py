from host_system import get_system_version
from enum import Enum, auto

class EventType(Enum):
    RISING = auto()
    FALLING = auto()

if get_system_version() == 'Linux':
    import RPi.GPIO as GPIO # module can not be imported in Windows


class ButtonHandler:
    def __init__(self):
        self.connected_handler = None
    
    def initialize(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        
        button_pins = [16]
        for button_pin in button_pins:
            GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(
                button_pin,
                GPIO.RISING,
                callback=lambda _: self.handle_pin_event(
                    pin=button_pin,
                    event_type=EventType.RISING
                )
            )
            # GPIO.add_event_detect(
            #     button_pin,
            #     GPIO.FALLING,
            #     callback=lambda _: self.handle_pin_event(
            #         pin=button_pin,
            #         event_type=EventType.FALLING
            #     )
            # )
        
    def connect(self, handler:callable):
        self.connected_handler = handler
    
    def handle_pin_event(self, pin: int, event_type: EventType):
        if event_type == EventType.RISING:
            print('Button event: RISING')
        if event_type == EventType.RISING:
            print('Button event: FALLING')
        
        if self.connected_handler is None:
            print('No ButtonHandler connected yet.')
        else:
            self.connected_handler(pin, event_type)





button_handler = ButtonHandler()