from models import db, Board, Feature


RASPBERRY_PI_FEATURES = [
    {
        "id": "gpio",
        "name": "GPIO",
        "description": "General-purpose input/output pins for hardware control.",
    },
    {
        "id": "i2c",
        "name": "I2C",
        "description": "Serial bus for sensors and peripheral communication.",
    },
    {
        "id": "spi",
        "name": "SPI",
        "description": "Serial peripheral interface for high-speed devices.",
    },
    {
        "id": "uart",
        "name": "UART",
        "description": "Serial communication interface for external devices.",
    },
    {
        "id": "wifi",
        "name": "Wi-Fi",
        "description": "Integrated wireless network connectivity.",
    },
    {
        "id": "bluetooth",
        "name": "Bluetooth",
        "description": "Integrated Bluetooth and BLE connectivity.",
    },
]


RASPBERRY_PI_4_DATA = {
    "id": "raspberry_pi_4",
    "name": "Raspberry Pi 4 Model B",
    "description": "Reference board preloaded as initial hardware target.",
    "toolchain": "yocto",
    "cross_compiler": "aarch64-poky-linux",
    "hardware_configuration": {
        "gpio_header": "40-pin",
        "wireless": ["wifi", "bluetooth"],
        "serial_interfaces": ["i2c", "spi", "uart"],
    },
}


def get_or_create_feature(feature_data):
    feature = db.session.get(Feature, feature_data["id"])

    if feature is None:
        feature = Feature(
            id=feature_data["id"],
            name=feature_data["name"],
            description=feature_data["description"],
        )
        db.session.add(feature)
    else:
        feature.name = feature_data["name"]
        feature.description = feature_data["description"]

    return feature


def get_or_create_board(board_data):
    board = db.session.get(Board, board_data["id"])

    if board is None:
        board = Board(
            id=board_data["id"],
            name=board_data["name"],
            description=board_data["description"],
            toolchain=board_data["toolchain"],
            cross_compiler=board_data["cross_compiler"],
            hardware_configuration=board_data["hardware_configuration"],
        )
        db.session.add(board)
    else:
        board.name = board_data["name"]
        board.description = board_data["description"]
        board.toolchain = board_data["toolchain"]
        board.cross_compiler = board_data["cross_compiler"]
        board.hardware_configuration = board_data["hardware_configuration"]

    return board


def seed_reference_data():
    features = []

    for feature_data in RASPBERRY_PI_FEATURES:
        feature = get_or_create_feature(feature_data)
        features.append(feature)

    board = get_or_create_board(RASPBERRY_PI_4_DATA)

    for feature in features:
        if feature not in board.features:
            board.features.append(feature)

    db.session.commit()
