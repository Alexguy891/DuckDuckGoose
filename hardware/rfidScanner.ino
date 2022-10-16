#include <SPI.h>
#include <RFID.h>
#define SS_PIN 10
#define RST_PIN 9
RFID rfid(SS_PIN, RST_PIN);

String rfidCard;

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.init();
  pinMode(7, OUTPUT); //red
  pinMode(6, OUTPUT); //yellow
}

void loop() {
  if (rfid.isCard()) {
    if (rfid.readCardSerial()) {
      rfidCard = String(rfid.serNum[0]) + " " + String(rfid.serNum[1]) + " " + String(rfid.serNum[2]) + " " + String(rfid.serNum[3]);
      Serial.println(rfidCard);
      delay(500);
      String test = Serial.readString();
      test.trim(); 
      if (test == "pass") {
        digitalWrite(6, HIGH);
        delay(2000); 
        digitalWrite(6,LOW);
      }
      else {
      digitalWrite(7, HIGH);
      delay(2000);
      digitalWrite(7, LOW);
    }
    }
    rfid.halt();
  }
}
