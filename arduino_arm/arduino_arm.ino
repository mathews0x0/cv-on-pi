// zoomkat 10-22-11 serial servo test
// type servo position 0 to 180 in serial monitor
// or for writeMicroseconds, use a value like 1500
// for IDE 0022 and later
// Powering a servo from the arduino usually *DOES NOT WORK*.

String readString;
#include <Servo.h> 
Servo servoy;  // create servo object to control a servo 
Servo servox;
Servo servoz;

void setup() {
  Serial.begin(9600);
  servox.writeMicroseconds(1000);//45  35 45 55
  servoy.writeMicroseconds(1000); //45  25-45-85 set initial servo position if desired
  
  servoz.writeMicroseconds(850);//30   25 - 30 - 55 
  servox.attach(9);
  servoy.attach(10); 
  servoz.attach(11);
  Serial.println("servo-test-22-dual-input"); // so I can keep track of what is loaded
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();  //gets one byte from serial buffer
    readString += c; //makes the string readString
    delay(2);  //slow looping to allow buffer to fill with next character
  }

  if (readString.length() >0) {
    Serial.println(readString);  //so you can see the captured string 
    int z = readString.toInt()%100;
    int x = readString.toInt()/10000;
    int y = readString.toInt()%10000;  //convert readString into a number
     y = y/100;

    // auto select appropriate value, copied from someone elses code.
    if(x >= 500 || y >= 500)
    {
      Serial.print("writing Microseconds 1: ");
      Serial.println(x);
      Serial.print("writing Microseconds 2: ");
      Serial.println(y);
     
    }
    else
    { Serial.print("writing Anglex: ");
      Serial.println(x);  
      Serial.print("writing Angley: ");
      Serial.println(y);
      Serial.print("writing Anglez: ");
      Serial.println(z);
      servox.write(x);
      servoy.write(y);
      servoz.write(z);
      
    }

    readString=""; //empty for next input
  } 
}

