#include <WiFiS3.h>
#include <ArduinoHttpClient.h>

// THESE 3 NEED TO BE CHANGED PER LAPTOP AND PER PHONE HOTSPOT

const char* ssid = "iPhone (25)";               // your hotspot name
const char* password = "ghskblwzda9s";   // your hotspot password

// run `ipconfig` in cmd, its the IPv4 address under the Wireless LAN adapter Wi-Fi
const char* serverAddress = "LAPTOP_IP"; // your laptop's IP
// Abril: "172.20.10.2"
// Alizee HP: "172.20.10.4"


const int serverPort = 5000;

const int GSR = A0;
int sensorValue = 0;
int gsr_average = 0;
WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, serverPort);
void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  int status = WiFi.begin(ssid, password);
  while (status != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    status = WiFi.status();
  }


  Serial.println("\nConnected to Wi-Fi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}


void loop() {
  // Read and average GSR sensor
  long sum = 0;
  for (int i = 0; i < 10; i++) {
    sensorValue = analogRead(GSR);
    sum += sensorValue;
    delay(5);
  }
  gsr_average = sum / 10;


  // Show in Serial Monitor
  Serial.print("GSR Avg: ");
  Serial.println(gsr_average);


  // Prepare JSON string
  String json = "{\"gsr\":" + String(gsr_average) + "}";


  // Send HTTP POST to Flask server
  client.beginRequest();
  client.post("/update");
  client.sendHeader("Content-Type", "application/json");
  client.sendHeader("Content-Length", json.length());
  client.beginBody();
  client.print(json);
  client.endRequest();


  int statusCode = client.responseStatusCode();
  String response = client.responseBody();
  Serial.print("Status: ");
  Serial.println(statusCode);


  delay(1000); // Send once per second
}
