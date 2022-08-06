#define DEBUG
/* Funktionen, die von DEBUGDU() umhüllt werden, werden nur ausgeführt, wenn DEFINE DEBUG
   im Code steht. Somit kann man die Serial-Befehle vollständig auskommentieren, um in
   der finalen Version des Microcontrollers höhere Performance und mehr Speicheplatz zu haben */
#ifdef DEBUG
  #include <SPI.h>
#endif
#ifdef DEBUG
#define DEBUGDO(stmt) stmt
#else
  #define DEBUGDO(stmt) ;
#endif

/* libraries */
#include <Wire.h>
#include <WebServer.h>    // vorinstallierte Bibliothek (esp32 Treiber muss in Boardverwaltung installiert sein)
#include <DHTesp.h>       // DHT sensor libary for ESPx by  begee_tokyo
#include <DNSServer.h>    // vorinstallierte Bibliothek
#include <EEPROM.h>       // vorinstallierte  Bibliothek
#include <NTPClient.h>    // NTPClient by Fabrice Weinberg
#include "attention.hpp"
#include "html.hpp"
#include "pomodoro.hpp"
#include "weather.hpp"

WiFiUDP ntpUDP;    // User Datagram Protocol verbindungslosen Versand von Datagrammen; Quelle https://www.ionos.de/digitalguide/server/knowhow/udp-user-datagram-protocol/
NTPClient timeClient(ntpUDP, "pool.ntp.org");   // Network Time Protocol (NTP) ist ein Standard zur Synchronisierung von Uhren in Computersystemen notwendig für kommunikativen Austausch zwischen zwei oder mehr Systemen          Quelle: https://www.ionos.de/digitalguide/server/knowhow/network-time-protocol-ntp/


// Definieren von Variablen
const IPAddress apIP(192, 168, 1, 1);
const char* apSSID = "OfficeStation";
boolean settingMode;
String ssidList;

unsigned long lastmillis3;
unsigned long lastmillis2;
unsigned long lastmillis1;

DNSServer dnsServer;
WebServer webServer(80);

void setup() {  
  Wire.begin();
  DEBUGDO(Serial.begin(115200));
  EEPROM.begin(512);

  weather_setup();
  attention_setup();
  pomodoro_setup();
  
  if (restoreConfig()) {
    if (checkConnection()) {
      settingMode = false;
      startWebServer();
      return;
     }
  }
  settingMode = true;
  setupMode();
}

void loop() {
  if (settingMode) {
    dnsServer.processNextRequest();
  }

  /* update state machines */
  pomodoro_update();
  attention_update();
  webServer.handleClient();
}




boolean restoreConfig() {
  Serial.println("Reading EEPROM...");
  String ssid = "";
  String pass = "";
  if (EEPROM.read(0) != 0) {
    for (int i = 0; i < 32; ++i) {
      ssid += char(EEPROM.read(i));
    }
    Serial.print("SSID: ");
    Serial.println(ssid);
    for (int i = 32; i < 96; ++i) {
      pass += char(EEPROM.read(i));
    }
    Serial.print("Password: ");
    Serial.println(pass);
    WiFi.hostname("OfficeStation");
    WiFi.begin(ssid.c_str(), pass.c_str());
    WiFi.hostname("OfficeStation");
    return true;
  }
  else {
    Serial.println("Config not found.");
    return false;
  }
    timeClient.begin();
    timeClient.setTimeOffset(1);
}

boolean checkConnection() {
  int count = 0;
  Serial.print("Waiting for Wi-Fi connection");
  while ( count < 100 ) {
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println();
      Serial.println("Connected!");
      return (true);
    }
    delay(500);
    Serial.print(".");
    count++;
  }
  Serial.println("Timed out.");
  return false;
}

void handleNormalWebsite() {
  String website =
      get_website_head() +
	  weather_get_html() + 
      pomodoro_get_html() +
      attention_get_html() +
      get_website_tail();
  webServer.send(200, "text/html", website);
}

void startWebServer() {
  if (settingMode) {
    Serial.print("Starting Web Server at ");
    Serial.println(WiFi.softAPIP());
    webServer.on
    ("/settings", []() {
      String s = "<h1>Wi-Fi Einstellungen</h1><p>Bitte wählen Sie den Namen Ihres Netzwerkes aus und geben Sie anschließend Ihr WLAN-Passwort ein.</p>";
      s += "<form class=\"pure-form\" method=\"get\" action=\"setap\"><label>SSID: </label><select name=\"ssid\">";
      s += ssidList;
      s += "</select><br>Password: <input class=\"form-control ml-5\" name=\"pass\" length=64 type=\"password\">  <button type=\"submit\" class=\"pure-button pure-button-primary\">Submit</button></form>";
      webServer.send(200, "text/html", makePage("Wi-Fi Settings", s));
    });
    webServer.on("/setap", []() {
      for (int i = 0; i < 96; ++i) {
        EEPROM.write(i, 0);
      }
      String ssid = urlDecode(webServer.arg("ssid"));
      Serial.print("SSID: ");
      Serial.println(ssid);
      String pass = urlDecode(webServer.arg("pass"));
      Serial.print("Password: ");
      Serial.println(pass);
      Serial.println("Writing SSID to EEPROM...");
      for (int i = 0; i < ssid.length(); ++i) {
        EEPROM.write(i, ssid[i]);
      }
      Serial.println("Writing Password to EEPROM...");
      for (int i = 0; i < pass.length(); ++i) {
        EEPROM.write(32 + i, pass[i]);
      }
      EEPROM.commit();
      Serial.println("Write EEPROM done!");
      String s = "<h1>Setup complete.</h1><p>device will be connected to \"";
      s += ssid;
      s += "\" after the restart.";
      webServer.send(200, "text/html", makePage("Wi-Fi Settings", s));
      ESP.restart();
    });
    webServer.onNotFound([]() {
      String s = "<h1>AP mode</h1><p><a href=\"/settings\">Wi-Fi Settings</a></p>";
      webServer.send(200, "text/html", makePage("AP mode", s));
    });
  } else {
    Serial.print("Starting Web Server at ");
    Serial.println(WiFi.localIP());


    webServer.on("/", handleNormalWebsite);  // send root page
    
    webServer.on("/reset", []() {
      for (int i = 0; i < 96; ++i) {
        EEPROM.write(i, 0);
      }
      EEPROM.commit();
      String s = "<h1>Wi-Fi settings were reset.</h1><p>Please reset device.</p>";
      webServer.send(200, "text/html", makePage("Reset Wi-Fi Settings", s));
    });
  }
  webServer.begin();
}

void setupMode() {
  WiFi.mode(WIFI_STA);
  WiFi.hostname("SmartOffice");
  WiFi.disconnect();
  delay(100);
  int n = WiFi.scanNetworks();
  delay(100);
  Serial.println("");
  for (int i = 0; i < n; ++i) {
    ssidList += "<option value=\"";
    ssidList += WiFi.SSID(i);
    ssidList += "\">";
    ssidList += WiFi.SSID(i);
    ssidList += "</option>";
  }
  delay(100);
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  WiFi.softAP(apSSID);
  dnsServer.start(53, "*", apIP);
  startWebServer();
  Serial.print("Starting Access Point at \"");
  Serial.print(apSSID);
  Serial.println("\"");
}


String makePage(String title, String contents) {
  String s = "<!DOCTYPE html><html><head>";
  s += "<meta name=\"viewport\" charset=\"utf-8\" content=\"width=device-width,user-scalable=0\">";
  s += "<title>";
  s += title;
  s += "</title>";
  s += "<style>";
  //s += cssList;
  s += "</style>";
  s += "</head>";
  s += "<body>";
  s += contents;
  s += "</body></html>";
  return s;
}

String urlDecode(String input) {
  String s = input;
  s.replace("%20", " ");
  s.replace("+", " ");
  s.replace("%21", "!");
  s.replace("%22", "\"");
  s.replace("%23", "#");
  s.replace("%24", "$");
  s.replace("%25", "%");
  s.replace("%26", "&");
  s.replace("%27", "\'");
  s.replace("%28", "(");
  s.replace("%29", ")");
  s.replace("%30", "*");
  s.replace("%31", "+");
  s.replace("%2C", ",");
  s.replace("%2E", ".");
  s.replace("%2F", "/");
  s.replace("%2C", ",");
  s.replace("%3A", ":");
  s.replace("%3A", ";");
  s.replace("%3C", "<");
  s.replace("%3D", "=");
  s.replace("%3E", ">");
  s.replace("%3F", "?");
  s.replace("%40", "@");
  s.replace("%5B", "[");
  s.replace("%5C", "\\");
  s.replace("%5D", "]");
  s.replace("%5E", "^");
  s.replace("%5F", "-");
  s.replace("%60", "`");
  return s;
}
