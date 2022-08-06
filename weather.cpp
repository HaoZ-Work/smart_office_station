#include <Wire.h>
#include "weather.hpp"
#include "html.hpp"
#include "Adafruit_HTU21DF.h"

Adafruit_HTU21DF htu;
static int htu_connected;

void weather_setup() {
  htu = Adafruit_HTU21DF();
  htu_connected = htu.begin();
  Serial.print("htu_connected yielded: "); Serial.println(htu_connected);
}

float get_temperature() {
  return htu.readTemperature();
}

float get_humidity() {
  return htu.readHumidity();
}

String weather_get_html() {
  if (!htu_connected) {
    Serial.println("deine mama is not connected");
    return "";
  };
  Serial.println("deine mama is connected");
  return
    get_window("<svg xmlns=\\http://www.w3.org/2000/svg\\ width=\\50\\ height=\\50\\ fill=\\currentColor\\ class=\\bi bi-cup-straw\\ viewBox=\\0 0 16 16\\>" /* todo */,
	       String(get_humidity())) +
    get_window("<svg xmlns=\\http://www.w3.org/2000/svg\\ width=\\50\\ height=\\50\\ fill=\\currentColor\\ class=\\bi bi-cup-straw\\ viewBox=\\0 0 16 16\\>" /* todo */,
	       String(get_temperature()));
}
