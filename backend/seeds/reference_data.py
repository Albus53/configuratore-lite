from models import db, Board, Feature


RASPBERRY_PI_FEATURES = [
    {
        "id": "gpio",
        "name": "GPIO",
        "description": "General-purpose input/output pins for hardware control.",
        "category": "hardware_io",
    },
    {
        "id": "pwm",
        "name": "PWM",
        "description": "Pulse-width modulation output for motors, LEDs, and signal control.",
        "category": "hardware_io",
    },
    {
        "id": "i2c",
        "name": "I2C",
        "description": "Serial bus for sensors and peripheral communication.",
        "category": "hardware_communication",
    },
    {
        "id": "spi",
        "name": "SPI",
        "description": "Serial peripheral interface for high-speed devices.",
        "category": "hardware_communication",
    },
    {
        "id": "uart",
        "name": "UART",
        "description": "Serial communication interface for external devices.",
        "category": "hardware_communication",
    },
    {
        "id": "wifi",
        "name": "Wi-Fi",
        "description": "Integrated wireless network connectivity.",
        "category": "hardware_communication",
    },
    {
        "id": "bluetooth",
        "name": "Bluetooth",
        "description": "Integrated Bluetooth and BLE connectivity.",
        "category": "hardware_communication",
    },
    {
        "id": "ethernet",
        "name": "Gigabit Ethernet",
        "description": "Wired network connectivity through the on-board Ethernet port.",
        "category": "hardware_communication",
    },
    {
        "id": "usb_2_0",
        "name": "USB 2.0",
        "description": "USB 2.0 ports for keyboards, mice, serial adapters, and legacy peripherals.",
        "category": "hardware_communication",
    },
    {
        "id": "usb_3_0",
        "name": "USB 3.0",
        "description": "High-speed USB 3.0 ports for storage devices and other fast peripherals.",
        "category": "hardware_communication",
    },
    {
        "id": "hdmi_display",
        "name": "HDMI Display",
        "description": "Micro-HDMI display output for external monitors and TVs.",
        "category": "hmi",
    },
    {
        "id": "dsi_display",
        "name": "DSI Display",
        "description": "Display Serial Interface support for compatible Raspberry Pi display panels.",
        "category": "hmi",
    },
    {
        "id": "csi_camera",
        "name": "CSI Camera",
        "description": "Camera Serial Interface support for compatible Raspberry Pi camera modules.",
        "category": "hmi",
    },
    {
        "id": "audio_output",
        "name": "Audio Output",
        "description": "Analog and digital audio output for speakers, headphones, and multimedia setups.",
        "category": "hmi",
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
        "networking": ["ethernet", "wifi", "bluetooth"],
        "serial_interfaces": ["i2c", "spi", "uart"],
        "gpio_functions": ["gpio", "pwm"],
        "usb_ports": ["usb_2_0", "usb_2_0", "usb_3_0", "usb_3_0"],
        "display_outputs": ["hdmi_display", "dsi_display"],
        "camera_interfaces": ["csi_camera"],
        "audio_outputs": ["audio_output"],
    },
}


def get_or_create_feature(feature_data):
    feature = db.session.get(Feature, feature_data["id"])

    if feature is None:
        feature = Feature(
            id=feature_data["id"],
            name=feature_data["name"],
            description=feature_data["description"],
            category=feature_data["category"],
        )
        db.session.add(feature)
    else:
        feature.name = feature_data["name"]
        feature.description = feature_data["description"]
        feature.category = feature_data["category"]

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
