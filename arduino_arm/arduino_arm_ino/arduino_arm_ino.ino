// input serial as x,y,z.. {two trailing .}

String readString;
#include <Servo.h> 
Servo servoy;  // create servo object to control a servo 
Servo servox;
Servo servoz;
Servo servog;
int x1=0;
int y1=0;
int z1=0;
int g1=0;
int x=0,y=0,z=0,g=0;
int cx=45,cy=50,cz=110;
int dx=3,dy=2;
int zo=0;
int grabflag=0;
void setup() {
  Serial.begin(9600);
  servox.write(45);//40  25 45 65 | --200 -  +200
  servoy.write(50); //30lower value moves up  5-30-50|-170- +170 set initial servo position if desired
  
  servoz.write(110);//110   - 110 -  lower moves fwd 80grab
  servox.attach(9);

  servoy.attach(10); 
  servoz.attach(11);
    servog.attach(4);
    servog.writeMicroseconds(700);
    //delay(2000);
    //servog.writeMicroseconds(1000);
  //Serial.println("servo-test-22-dual-input"); // so I can keep track of what is loaded
}

void loop() {
  char c;
  //Serial.println("grabbed from loop");
  while (Serial.available()) {
     //Serial.println("grabbed from serial avai;");
     c = Serial.read();  //gets one byte from serial buffer
     //makes the string readString
    delay(2);  //slow looping to allow buffer to fill with next character
   // Serial.println(c);
    
    
  if(x1 == 0){
  if(c==','){
    x = readString.toInt();
    x1=1;
    
  readString="";  }
  else{
    readString+=c;}
  }
  else if(y1 == 0){
  if(c==','){
    y = readString.toInt();
    y1=1;
  readString="";  }
  else
    readString+=c;
  }
  else if(z1==0){
  if(c==','){
    z = readString.toInt();
    z1=1;
  readString="";  }
  else
    readString+=c;
  }
  else if(g1==0){
  if(c=='.'){
    g = readString.toInt();
    g1=1;
  readString="";  }
  else
    readString+=c;
  }
  else if(c=='.'){
      readString="";
      x1=0;
      y1=0;
      z1=0;
      g1=0;
      //Serial.print("writing Anglex: ");
      //Serial.println(x);  
      //Serial.print("writing Angley: ");
      //Serial.println(y);
      //Serial.print("writing Anglez: ");
      //Serial.println(z);
      //Serial.print("writing Angleg: ");
      //Serial.println(g);
      if(z==80){//grab 
      grabflag=1;}
      
      if(z==110){
        

        
      if(x<0){
        if(cx>10)
          cx=cx-dx;
      }
      else 
      if(cx<65)
        cx=cx+dx;
      if(y>0){
        if(cy>5)
          cy=cy-dy;
      }
      else 
      if(cy<50)
        cy=cy+dy;
      

      
      }
   
      
      servox.write(cx);
      servoy.write(cy);
      /*Serial.print("writing Anglex: ");
      Serial.println(cx);  
      Serial.print("writing Angley: ");
      Serial.println(cy);
      Serial.print("writing Anglez: ");
      Serial.println(z);
      //Serial.print("writing Angleg: ");
      //Serial.println(g);*/
      
      if(grabflag==1){
      //do the grab here
      //Serial.println("grabflag set");
      //delay(2000);
      //Serial.print("init"+cx);
        for(int v=110;v>80;v--){
          servoz.write(v);
          if(v%2==0)
            cy--;
            servoy.write(cy);
          delay(50);
        }
        for(int v=700;v<1000;v++){
          servog.writeMicroseconds(v);
          delay(3);
        }
        
        delay(2000);
        for(int v=80;v<110;v++){
          servoz.write(v);
          if(v%2==0)
            cy++;
            servoy.write(cy);
          delay(50);
        }
        for(int v=cx;v<120;v++){
          servox.write(v);
          delay(50);
        }
        for(int v=1000;v>700;v--){
          servog.writeMicroseconds(v);
          delay(4);
        }
        for(int v=120;v>45;v--){
          servox.write(v);
          delay(50);
        }

        //Serial.println("\nSTOPGRAB");
      
      Serial.println("grab done,continue");
      grabflag=0;
      }
      
     
      x=0;
      y=0;
      g=0;
      
  
  }
  else{
    //Serial.print("eerrrrr ");
    z=110;
  }
    
    
    
  }
  

       
     
      
    }


 


