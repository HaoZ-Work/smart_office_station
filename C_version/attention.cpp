#include <Wire.h>
#include <BH1750.h>
#include "html.hpp"

#define LIGHT_THRESH 10.00
#define MILLIS_NOT_IN_CASE_UNTIL_RESET 4*60*60*1000 /* 4 hours */
static BH1750 lightMeter;
static bool phone_in_case = false;
static unsigned long phone_in_case_total = 0;
static unsigned long phone_in_case_since = millis();
static unsigned long phone_not_in_case_since = millis();
static unsigned int disruptions = 0;
static unsigned int connected = false;

int is_connected() {
	return connected;
}

int is_phone_in_case() {
	if (phone_in_case) return true;
	return false;
}

void attention_setup() {
	connected = (lightMeter.readLightLevel() != -1.f);
  lightMeter.begin();
}

void attention_update() {
	if (!connected) return;
	
    float lux = lightMeter.readLightLevel();
	bool phone_in_case_new = lux < LIGHT_THRESH;
	if        (phone_in_case && phone_in_case_new) {
		// do nothing
	} else if (!phone_in_case && phone_in_case_new) {
		phone_in_case_since = millis();
		phone_in_case = true;
	} else if (phone_in_case && !phone_in_case_new) {
		unsigned long cur_time = millis();		
		phone_in_case_total += cur_time - phone_in_case_since;
		phone_not_in_case_since = cur_time;
		disruptions += 1;
		phone_in_case = false;
	} else /* !phone_in_case && !phone_in_case_new */ {
		unsigned long cur_time = millis();
	    if (cur_time - phone_not_in_case_since > MILLIS_NOT_IN_CASE_UNTIL_RESET) {
			disruptions = 0;
		}
	}
}

int get_disruptions() { return disruptions; }

unsigned long get_concentration_time_millis() {
	if (phone_in_case) return phone_in_case_total + phone_in_case_since - millis();
	else return phone_in_case_total;
}

String attention_get_html() {
	if (!connected) return "";
	return get_window("<svg xmlns=\\http://www.w3.org/2000/svg\\ width=\\50\\ height=\\50\\ fill=\\currentColor\\ class=\\bi bi-cup-straw\\ viewBox=\\0 0 16 16\\>" /* todo */, String(get_disruptions()));
}
