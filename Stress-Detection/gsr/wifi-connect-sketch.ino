#include <WiFiS3.h>
#include <ArduinoHttpClient.h>

// Update with your hotspot credentials
const char* ssid = "abril";
const char* password = "abril123";

// Laptop IP from ipconfig
const char* serverAddress = "172.20.10.2";
const int serverPort = 5000;

// yes this ^ is personal info but whatever

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, serverPort);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  int status = WiFi.begin(ssid, password);
  while (status != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
    status = WiFi.status();
  }

  Serial.println("\nConnected to Wi-Fi.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Prepare a JSON payload
  String json = "{\"status\":\"hello from Arduino\"}";

  // Send HTTP POST
  client.beginRequest();
  client.post("/update");
  client.sendHeader("Content-Type", "application/json");
  client.sendHeader("Content-Length", json.length());
  client.beginBody();
  client.print(json);
  client.endRequest();

  // Read response
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("HTTP Status: ");
  Serial.println(statusCode);
  Serial.print("Server Response: ");
  Serial.println(response);
}

void loop() {
  // Nothing here for now
}
