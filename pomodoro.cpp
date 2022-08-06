#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

/* Variables for the display */
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
static Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
static bool connected = false;

/* Variables for the timer */
static unsigned long start_time;
static bool started = false;
enum phase {CONCENTRATION, BREAK};
static bool phase = CONCENTRATION;
#define MINUTES_CONCENTRATION 1
#define MINUTES_BREAK 1

/* Functions for the display */
static void draw_time(uint8_t minutes, uint8_t seconds) {
    display.clearDisplay();

    display.setTextSize(2);             // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE);        // Draw white text
    display.setCursor(0,0);             // Start at top-left corner
    display.print(minutes);
    display.print("m ");
    display.print(seconds);
    display.println("s");
    display.print(F("remaining"));
    display.display();
}

/* Functions for the timer */
int get_remaining_time() {
    unsigned long current_time = millis();
    unsigned long elapsed_seconds = (current_time - start_time) / 1000;
    int seconds_left;
    if (phase == CONCENTRATION) {
        seconds_left = MINUTES_CONCENTRATION*60 - elapsed_seconds;
    } else {
        seconds_left = MINUTES_BREAK*60 - elapsed_seconds;
    }
    return seconds_left;
}

void draw_remaining_time() {
    int remaining_time = get_remaining_time();
    int remaining_time_minutes = remaining_time / 60;
    int remaining_time_seconds = remaining_time % 60;
    draw_time(remaining_time_minutes, remaining_time_seconds);
}

void draw_press_button() {
    display.clearDisplay();

    display.setTextSize(1);             // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE);        // Draw white text
    display.setCursor(0,0);             // Start at top-left corner
    display.print("Press Button to start phase ");
    if (phase == CONCENTRATION) display.print("concentration");
    else                        display.print("break");
    display.display();
}

void start_timer() {
    start_time = millis();
    started = true;
    Serial.print("Set start time to "); Serial.println(millis());
}

void stop_timer() {
    started = false;
}

bool get_input() { // TODO return the input of the pomodoro button
    return true;
}

void pomodoro_state_machine() {
    if      (phase==CONCENTRATION && started==true )  {if (get_remaining_time() <= 0) {phase = BREAK;         stop_timer();} else draw_remaining_time();}
    else if (phase==BREAK         && started==true )  {if (get_remaining_time() <= 0) {phase = CONCENTRATION; stop_timer();} else draw_remaining_time();}
    else if (phase==BREAK         && started==false)  {if (get_input()) {start_timer();} else draw_press_button();}
    else if (phase==CONCENTRATION && started==false)  {if (get_input()) {start_timer();} else draw_press_button();}
}

void pomodoro_setup() {
// SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
#ifdef SERIAL      
    Serial.println(F("SSD1306 allocation failed"));
#endif    
    connected = false;
    return;
  }
  connected = true;
}

void pomodoro_update() {
    if (connected)
        pomodoro_state_machine();
}

String pomodoro_get_html() {return "";}
