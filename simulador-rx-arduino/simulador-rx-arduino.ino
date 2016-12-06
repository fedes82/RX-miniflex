/*
  Analog input, analog output, serial output

 Reads an analog input pin, maps the result to a range from 0 to 255
 and uses the result to set the pulsewidth modulation (PWM) of an output pin.
 Also prints the results to the serial monitor.

 The circuit:
 * potentiometer connected to analog pin 0.
   Center pin of the potentiometer goes to the analog pin.
   side pins of the potentiometer go to +5V and ground
 * LED connected from digital pin 9 to ground

 created 29 Dec. 2008
 modified 9 Apr 2012
 by Tom Igoe

 This example code is in the public domain.

 */

// These constants won't change.  They're used to give names
// to the pins used:
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)
char lectura =0;
const int buttonPin = 2;
int estoymidiendo =0;
void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(4800);
  pinMode(buttonPin, INPUT);
}

void loop() {
  // read the analog in value:
  if (Serial.available() >0)
  { //Serial.print("LLEGO EL DATO \n") ;
    lectura = Serial.read();
   // Serial.print(lectura);
   // Serial.print("\n");
      if (lectura == 'I')
      { 
        while(digitalRead(buttonPin) == HIGH);
        
        estoymidiendo = 1;
        sensorValue = analogRead(analogInPin);
        //Serial.print(sensorValue);
        printDouble(sensorValue,2);
        Serial.print("\n");
        while(estoymidiendo)
        {
            if (Serial.available() >0)
            {  
              //Serial.print("LLEGO EL SEGUNTO DATO") ;
              lectura = Serial.read();
            //  Serial.print(lectura);
            //  Serial.print("\n");
               if (lectura == '1')
               {
                //Serial.print("MIDO") ;
                  sensorValue = analogRead(analogInPin);
                  //Serial.print(sensorValue);
                  printDouble(sensorValue,2);
                  Serial.print("\n");
               }
               if (lectura == 'T')
                {
                  //Serial.print("SALGO") ;
                  estoymidiendo = 0;
                }
                if (lectura == 'P')
                {Serial.println("comunicacion ON \n");}
        }
            /*
            // map it to the range of the analog out:
            outputValue = map(sensorValue, 0, 1023, 0, 255);
            // change the analog out value:
            
          
            // print the results to the serial monitor:
            Serial.print("sensor = ");
            
            Serial.print("\t output = ");
            Serial.println(outputValue);
          */
            // wait 2 milliseconds before the next loop
            // for the analog-to-digital converter to settle
            // after the last reading:
            delay(2);
        }
      }
  }
}



void printDouble( double val, byte precision){
 // prints val with number of decimal places determine by precision
 // precision is a number from 0 to 6 indicating the desired decimial places
 // example: printDouble( 3.1415, 2); // prints 3.14 (two decimal places)

 Serial.print (int(val));  //prints the int part
 if( precision > 0) {
   Serial.print("."); // print the decimal point
   unsigned long frac;
   unsigned long mult = 1;
   byte padding = precision -1;
   while(precision--)
      mult *=10;
     
   if(val >= 0)
     frac = (val - int(val)) * mult;
   else
     frac = (int(val)- val ) * mult;
   unsigned long frac1 = frac;
   while( frac1 /= 10 )
     padding--;
   while(  padding--)
     Serial.print("0");
   Serial.print(frac,DEC) ;
 }
}
