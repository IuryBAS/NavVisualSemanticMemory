KITCHEN_OBJECT_CLASS_LIST = [
    #test "Toaster",
    #test "Microwave",
    "Fridge",
    "CoffeeMachine",
    #"GarbageCan",
    #"Box",
    "Bowl",
    #novos
    "HousePlant",
    "StoveKnob", 
    "Sink",
    "TableTop",
    "Potato",
    "Bread",
    "Tomato",
    "Knife",
    "Container",
    "ButterKnife",
    "Lettuce",
    "Pan", 
    "StoveBurner",
    "Plate",
    #test "Mug",
    #test "Apple",
    #"Cup",
    "Spoon"
]

LIVING_ROOM_OBJECT_CLASS_LIST = [
    #"Pillow",
    #"Laptop",
    "Television",
    #"GarbageCan",
    "Box",
    #"Bowl",
    #novos
    "HousePlant",
    "Chair",
    "TableTop",
    "Cloth",
    "NewsPaper",
    "KeyChain",
    "WateringCan",
    "PaintingHanger" 
    #test "Statue"
]

BEDROOM_OBJECT_CLASS_LIST = [
    "HousePlant", 
    "Lamp", 
    "Book", 
    "AlarmClock",
    #novos
    "Painting",
    "CellPhone",
    "LightSwitch",
    "Candle",
    "TableTop",
    "Statue",
    "CreditCard",
    "KeyChain",
    "Bowl",
    "Pen",
    "Box",
    "Pencil",
    "Blinds",
    "Laptop"
]


BATHROOM_OBJECT_CLASS_LIST = [
    "Sink",
    "ToiletPaper",
    "SoapBottle",
    "LightSwitch",
    "SprayBottle",
    "Painting",
    "Candle",
    #"LightSwitch",
    "TowelHolder",
    "Watch"
]

FULL_OBJECT_CLASS_LIST = (
    KITCHEN_OBJECT_CLASS_LIST
    + LIVING_ROOM_OBJECT_CLASS_LIST
    + BEDROOM_OBJECT_CLASS_LIST
    + BATHROOM_OBJECT_CLASS_LIST
)


MOVE_AHEAD = "MoveAhead"
ROTATE_LEFT = "RotateLeft"
ROTATE_RIGHT = "RotateRight"
LOOK_UP = "LookUp"
LOOK_DOWN = "LookDown"
DONE = "Done"

DONE_ACTION_INT = 5
GOAL_SUCCESS_REWARD = 5
STEP_PENALTY = -0.01
