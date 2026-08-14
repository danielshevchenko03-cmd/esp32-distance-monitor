#include <WiFi.h> // wifi
#include <HTTPClient.h> // http
#include "Adafruit_VL6180X.h" // sensor lib
#include "secrets.h"

// sensor logic
int distanceLimit = 500;
bool objectPresent = false;

Adafruit_VL6180X vl = Adafruit_VL6180X();

void setup() {
  // test sensor connection
  Serial.begin(115200);
  delay(1000);

  if (!vl.begin()) 
  {
    Serial.println("Failed to find sensor!");
    while(1);
  }
  else { Serial.println("Sensor found!"); }

  // WiFi connection
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

    Serial.println("Connected!");
    Serial.println("Board IP address: ");
    Serial.println(WiFi.localIP());

}

void loop() {
  // read sensor data
  uint8_t range = vl.readRange();
  uint8_t status = vl.readRangeStatus();

  if (status == VL6180X_ERROR_NONE && range < distanceLimit && objectPresent == false) 
  {
    // print range
    Serial.print("Object detected at: ");
    Serial.print(range);
    Serial.println(" mm");

    // create http client
    HTTPClient http = HTTPClient();
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    
    // collect json and send
    String jsonString = "{\"distance\":" + String(range) + "," + "\"device_id\":" + "\"esp32_1\"}";
    int httpResponseCode = http.POST(jsonString);
    
    // print response code to console
    if (httpResponseCode > 0)
    {
      Serial.print("Response Code: ");
      Serial.println(httpResponseCode);
    } 
    
    else 
    {
      Serial.print("Error Code: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();

    objectPresent = true;
  }

  else if ((status != VL6180X_ERROR_NONE || range >= distanceLimit) && objectPresent == true)
  {
    Serial.println("No objects nearby");
    objectPresent = false;
  }
}
