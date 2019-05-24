#include <SoftwareSerial.h>
#include <EduIntro.h>
#define buz 6
#define smoke 3
//const String ssid="\"PresentationSSID\"";
const String ssid="\"ASUS\"";
const String password="\"xuyitaodashabi\"";
PIR pir(D7);
DHT11 dht11(D2);  // creating the object sensor on pin 'D7'
int C;   // temperature C readings are integers
float F; // temperature F readings are returned in float format
int H;   // humidity readings are integers
int val;
int O;
int S;
String postjson;
String postRequest;
String message;
SoftwareSerial mySerial(10, 11); // RX, TX
void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
  ; // wait for serial port to connect. Needed for Leonardo only
  }
  Serial.println("test mySerial");
  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  pinMode(buz,OUTPUT);
  pinMode(smoke,INPUT);
  //Serial.println(postRequest.length());
  //mySerial.println("AT+CIFSR");
  setwifi();
  mySerial.println("AT+CIPMUX=1");
  delay(100);
  mySerial.println("AT+CIPSERVER=1,8080");
  //mySerial.println("AT+CIPSERVER=0");
}

void loop() // run over and over
{
  dht11.update();
  while(!getmessage("CONNECT"));
  C = dht11.readCelsius();       // Reading the temperature in Celsius degrees and store in the C variable
  F = dht11.readFahrenheit();   // Reading the temperature in Fahrenheit degrees and store in the F variable
  H = dht11.readHumidity();     // Reading the humidity index
  if (pir.active() == HIGH) {
    O=1;
  }
  else {
    O=0;
  }
  val=analogRead(smoke);
  if(val<310) S=0;
  else S=1;
  postjson="{\"temperature\":"+String(C)+".0,"+
            "\"humidity\":"+String(H)+","+
            "\"occupancy\":"+String(O)+","+
            "\"smoke\":"+String(S)+"}";
  postRequest =(String)("HTTP/1.1 200 OK\r\n") +
    "Content-Type: application/json;charset=utf-8\r\n" +
    //"Server:Arduino-esp8266\r\n"+
    //"Date: Mon, 14 May 2019 12:28:53 GMT\r\n"+
    //"Accept-Ranges: bytes\r\n"+
    //"Content-Length:"+String(postjson.length())+"\r\n"+
    "Connection:close\r\n\r\n" +
    postjson;
  
  mySerial.println("AT+CIPSEND=0,"+String(postRequest.length()));
  delay(100);
  mySerial.print(postRequest);
  delay(100);
  mySerial.println("AT+CIPCLOSE=5");
  while(!getmessage("CLOSED"));
}
boolean getmessage(String val){
  while(mySerial.available()){
    String line = mySerial.readStringUntil('\r');
    line.trim();
    Serial.println(line);
    if(line.endsWith(val)){
      return 1;
    }
  }
  return 0;
}
void setwifi(){
  mySerial.println("AT+CWMODE=3");
  while(!getmessage("OK"));
  mySerial.println("AT+CWJAP="+ssid+","+password);
  while(!getmessage("OK"));
  mySerial.println("AT+CIFSR");
  while(!getmessage("OK"));
}
