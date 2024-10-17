#include <ArduinoBLE.h>
#include <Ultrasonic.h>

// Pin definitions
const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
Ultrasonic ultrasonic(TRIG_PIN, ECHO_PIN);

// BLE Service and Characteristic
BLEService parkingService("180A");
BLEUnsignedIntCharacteristic distanceCharacteristic("2A19", BLERead | BLENotify);

void setup() {
  Serial.begin(9600);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // Set BLE device name and service
  BLE.setLocalName("ParkingSensor");
  BLE.setAdvertisedService(parkingService);
  parkingService.addCharacteristic(distanceCharacteristic);
  BLE.addService(parkingService);
  BLE.advertise();

  Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() {
  // Wait for a central device to connect
  BLEDevice central = BLE.central();
  if (central) {
    Serial.println("Connected to central device");

    while (central.connected()) {
      // Get the distance in cm
      unsigned int distance = ultrasonic.read();
      
      if (distance > 0) {
        Serial.print("Distance: ");
        Serial.println(distance);

        // Update BLE characteristic with new distance
        distanceCharacteristic.writeValue(distance);
      }
      delay(100);
    }
    Serial.println("Disconnected from central device");
  }
}
