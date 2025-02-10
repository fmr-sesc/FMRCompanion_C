#include <Wire.h>
#include <vector> // Für die Verwendung von Vektoren benötigen Sie die <vector>-Bibliothek

#define HCL_ADDR 0x78
#define PCA95_ADDR 0x71
std::vector<int> availableSensors;

// Float of calculated pressure
float result;
// Integer of read sensor output
unsigned int value;

void setup() {
  Wire.begin(); // Enable I2C communication as master
  Serial.begin (19200);
  
  // Vektor für die Speicherung der verfügbaren Sensoren initialisieren
  for (int i = 0; i <= 7; i++) {
    // Teste, ob Sensor ansprechbar ist
    if (sensSelect(i)) {
      if (std::abs(GetPressure(HCL_ADDR)) < 5) {
        Serial.print("The sensor ");
        Serial.print(i);
        Serial.print(" is found");
        Serial.println();

      // Füge den Index von i zu den verfügbaren Sensoren hinzu
        availableSensors.push_back(i);
      } else {
        Serial.print("The sensor ");
        Serial.print(i);
        Serial.print(" is not found");
        Serial.println();
      }
    } else {
      Serial.print("The sensor ");
      Serial.print(i);
      Serial.print(" is not found");
      Serial.println();
    }
    // Warte 10 Millisekunden
    delay(100);
  }

  // Ausgabe der verfügbaren Sensoren
  Serial.println("Available sensors:");
  for (int sensorIndex : availableSensors) {
    Serial.println(sensorIndex);
  }
}

bool sensSelect(uint8_t i) {
  if (i > 7) return false;
  Wire.beginTransmission(PCA95_ADDR);
  Wire.write(1 << i);
  int error = Wire.endTransmission();
  if (error != 0) {
    return false;
  } else {
    return true;
  }
}

float GetPressure(int addr) {
  Wire.beginTransmission(addr);
  
  //Read first bite from address
  Wire.requestFrom(addr, 1); 

  //Read from adress
  value = Wire.read();

  value <<= 8;

  //Calculate pressure 
  result = ((float(value) - 1638) / 5253) - 2.47;
  return result;
}

void loop() {
  for (int sensorIndex : availableSensors) {
    sensSelect(sensorIndex);
    Serial.print("Druck Sensor ");
    Serial.print(sensorIndex);
    Serial.print(": ");
    Serial.print(GetPressure(HCL_ADDR));
    Serial.print(" mbar");
    Serial.println();
    delay(500);
  }
}
