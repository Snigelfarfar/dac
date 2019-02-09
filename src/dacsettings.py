def dacDefaultSettings():
    default = {
        "time": {
            "wakeup": "07:00",
            "bulb": "07:00",
            "coffee": "07:05",
        },
        "timer": {
            "snooze": "5",
            "bulb": 75,
        },
        "status": {
            "wakeup": "ON",
            "bulb": "ON",
            "coffee": "ON"
        },
        "trigger": {
            "wakeup": "ON",
            "bulb": "ON",
            "coffee": "ON"
        },
        "silence": {
            "challenge": "55555",
            "response": "empty",
            "completed": False, 
        },
        "api": {
            "homeassistant": {
                "bulb": {
                    "id": "switch.switch_2"
                    }
                }    
        }


    }
    return default
