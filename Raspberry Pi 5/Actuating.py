import asyncio
try:
    from bleak import BleakClient
except ImportError:
    print("Error: bleak module not found. Please install it using 'sudo apt install python3-dev python3-pip' and 'pip install bleak'.")
    exit(1)
import RPi.GPIO as GPIO
try:
    from rpi_ws281x import Color
except ImportError:
    print("Error: rpi_ws281x module not found. Please install it using 'pip install rpi_ws281x'.")
    exit(1)

try:
    from gpiozero import PWMLED, PWMOutputDevice
except ImportError:
    print("Error: gpiozero module not found. Please install it using 'sudo apt install python3-gpiozero'.")

import time

# GPIO setup for LED and Buzzer using GPIO Zero
led = PWMLED(18)  # LED connected to GPIO pin 18
buzzer = PWMOutputDevice(23)  # Buzzer connected to GPIO pin 23

# BLE characteristic UUID
DISTANCE_CHARACTERISTIC_UUID = "2A19"

async def run_ble_client():
    address = "XX:XX:XX:XX:XX:XX"  # Replace with Arduino Nano 33 IoT MAC address
    async with BleakClient(address) as client:
        while True:
            # Read distance data from BLE characteristic
            distance_data = await client.read_gatt_char(DISTANCE_CHARACTERISTIC_UUID)
            distance = int.from_bytes(distance_data, byteorder='little')
            print(f"Distance: {distance} cm")

            # Adjust LED and buzzer based on proximity
            if distance <= 50:  # Dangerously close
                led.value = 1.0  # Full brightness
                buzzer.value = 1.0  # Loudest sound
            elif distance <= 100:  # Close
                led.value = 0.5  # Medium brightness
                buzzer.value = 0.5  # Medium sound
            else:
                led.value = 0.0  # Turn off LED
                buzzer.value = 0.0  # No sound

            await asyncio.sleep(1)  # Adjust the loop delay as needed

# Run the BLE client to receive data from Arduino Nano 33 IoT
loop = asyncio.get_event_loop()
loop.run_until_complete(run_ble_client())
