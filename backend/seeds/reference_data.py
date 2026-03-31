from models import db, Board, Feature


FEATURES_DATA = [
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
        "id": "ble",
        "name": "Bluetooth LE",
        "description": "Bluetooth Low Energy connectivity for low-power wireless devices.",
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
    {
        "id": "adc",
        "name": "ADC",
        "description": "Analog-to-digital converter inputs for reading analog sensors and variable signals.",
        "category": "hardware_io",
    },
    {
        "id": "can",
        "name": "CAN",
        "description": "Controller Area Network interface for robust industrial communication.",
        "category": "hardware_communication",
    },
    {
        "id": "usb_host",
        "name": "USB Host",
        "description": "USB host port support for external peripherals such as storage, hubs, and input devices.",
        "category": "hardware_communication",
    },
    {
        "id": "usb_client",
        "name": "USB Client",
        "description": "USB device/client port support for power, flashing, networking, and development workflows.",
        "category": "hardware_communication",
    },
    {
        "id": "micro_sd_storage",
        "name": "microSD Storage",
        "description": "microSD slot support for removable storage and alternate boot media.",
        "category": "system_logic",
    },
    {
        "id": "emmc_storage",
        "name": "eMMC Storage",
        "description": "On-board eMMC storage for booting and persistent system images.",
        "category": "system_logic",
    },
    {
        "id": "lcd_interface",
        "name": "LCD Interface",
        "description": "Parallel LCD interface support for compatible display expansion boards.",
        "category": "hmi",
    },
    {
        "id": "touch_panel",
        "name": "Touch Panel",
        "description": "Touch input support for interactive displays and graphical interfaces.",
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

RASPBERRY_PI_4_FEATURE_IDS = [
    "gpio",
    "pwm",
    "i2c",
    "spi",
    "uart",
    "wifi",
    "bluetooth",
    "ethernet",
    "usb_2_0",
    "usb_3_0",
    "hdmi_display",
    "dsi_display",
    "csi_camera",
    "audio_output",
]


BEAGLEBONE_DATA = {
    "id": "beaglebone",
    "name": "BeagleBone Black",
    "description": "Reference BeagleBone target modeled on documented BeagleBone Black hardware capabilities.",
    "toolchain": "yocto",
    "cross_compiler": "arm-poky-linux-gnueabi",
    "hardware_configuration": {
        "expansion_headers": ["P8", "P9"],
        "networking": ["ethernet"],
        "serial_interfaces": ["i2c", "spi", "uart", "can"],
        "gpio_functions": ["gpio", "pwm", "adc"],
        "usb_ports": ["usb_client", "usb_host"],
        "storage": ["emmc_storage", "micro_sd_storage"],
        "display_outputs": ["hdmi_display", "lcd_interface"],
        "audio_outputs": ["audio_output"],
    },
}

BEAGLEBONE_FEATURE_IDS = [
    "gpio",
    "pwm",
    "adc",
    "i2c",
    "spi",
    "uart",
    "can",
    "ethernet",
    "usb_host",
    "usb_client",
    "micro_sd_storage",
    "emmc_storage",
    "hdmi_display",
    "lcd_interface",
    "audio_output",
]


STM32_DISCOVERY_DATA = {
    "id": "stm32",
    "name": "STM32MP157F-DK2 Discovery Kit",
    "description": "Reference STM32 Discovery target modeled on documented STM32MP157F-DK2 hardware capabilities.",
    "toolchain": "yocto",
    "cross_compiler": "arm-poky-linux-gnueabi",
    "hardware_configuration": {
        "expansion_connectors": ["arduino_uno_v3", "raspberry_pi_shield"],
        "networking": ["ethernet", "wifi", "ble"],
        "usb_ports": ["usb_client", "usb_host", "usb_host", "usb_host", "usb_host"],
        "storage": ["micro_sd_storage"],
        "display_outputs": ["hdmi_display", "dsi_display"],
        "input_interfaces": ["touch_panel"],
        "audio_outputs": ["audio_output"],
        "gpio_functions": ["gpio"],
    },
}

STM32_DISCOVERY_FEATURE_IDS = [
    "gpio",
    "wifi",
    "ble",
    "ethernet",
    "usb_host",
    "usb_client",
    "micro_sd_storage",
    "hdmi_display",
    "dsi_display",
    "touch_panel",
    "audio_output",
]


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
    features_by_id = {}

    for feature_data in FEATURES_DATA:
        feature = get_or_create_feature(feature_data)
        features_by_id[feature.id] = feature

    raspberry_pi_4 = get_or_create_board(RASPBERRY_PI_4_DATA)

    for feature_id in RASPBERRY_PI_4_FEATURE_IDS:
        feature = features_by_id[feature_id]
        if feature not in raspberry_pi_4.features:
            raspberry_pi_4.features.append(feature)

    beaglebone = get_or_create_board(BEAGLEBONE_DATA)

    for feature_id in BEAGLEBONE_FEATURE_IDS:
        feature = features_by_id[feature_id]
        if feature not in beaglebone.features:
            beaglebone.features.append(feature)

    stm32_discovery = get_or_create_board(STM32_DISCOVERY_DATA)

    for feature_id in STM32_DISCOVERY_FEATURE_IDS:
        feature = features_by_id[feature_id]
        if feature not in stm32_discovery.features:
            stm32_discovery.features.append(feature)

    db.session.commit()
