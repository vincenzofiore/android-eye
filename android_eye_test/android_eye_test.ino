/* =====================================================================
   android_eye_test.ino — behaviour test bench
   ---------------------------------------------------------------------
   Arduino Uno + PIR + HC-SR04 + SG90 + LED (pupil)

   TWO SENSES, TWO ROLES
     PIR      -> wide (~100 deg), slow, sees motion in BOTH directions.
                 Its only job is to SUSPECT. It is also what wakes the
                 system from the soft-latch, so it must stay powered
                 outside the main switch.
     HC-SR04  -> narrow (25 deg downwards along the stair flight),
                 precise. Its job is to CONFIRM and to OPEN.

   STATES
     SLEEPING : eyelid closed, nobody around
     SUSPECT  : something moved -> the eyelid cracks open a sliver
     OPENING  : real opening, fast
     CONTACT  : eye open, pupil dilating
     FAREWELL : last glance + slow close

   Every number that matters lives in the block below: those are the
   ones to tune. Nothing else needs to be touched.
   ===================================================================== */

#include <Servo.h>

// ------------------------------------------------------------------ PINS
const uint8_t PIN_TRIG  = 7;
const uint8_t PIN_ECHO  = 8;
const uint8_t PIN_SERVO = 9;   // Servo library uses Timer1: no PWM on 9 and 10
const uint8_t PIN_LED   = 6;   // PWM, free
const uint8_t PIN_PIR   = 2;

// ------------------------------------------------------------ MECHANICS
const int ANG_CLOSED = 6;      // eyelid resting on the socket
const int ANG_SLIT   = 21;     // "I heard something"
const int ANG_OPEN   = 96;
const int ANG_GLANCE = 101;    // last glance before closing

// ------------------------------------------------- THRESHOLDS (cm)
// Head about 1.10 m above the tread: eye contact happens three steps
// below, roughly 1 m ahead. Change the height, retune these two.
const int     D_ANTICIPATE = 210;   // beyond this the ultrasonic sees nobody
const int     D_NEAR       = 100;   // below this, open all the way
const int     D_AWAY       = 150;   // hysteresis for "they are leaving"
const uint8_t SAMPLE_COUNT = 5;     // median over 5 readings

// ------------------------------------------------------ TIMINGS (ms)
const uint32_t T_SUSPECT_CONFIRM = 120;    // the PIR must not flicker
const uint32_t T_NEAR_CONFIRM    = 130;
const uint32_t T_ABANDON         = 900;
const uint32_t T_SLIT            = 950;
const uint32_t T_OPEN            = 620;
const uint32_t T_GLANCE          = 300;
const uint32_t T_CLOSE           = 2600;
const uint32_t T_MIN_OPEN        = 4000;   // never close on someone walking past
const uint32_t T_SERVO_RELEASE   = 400;    // set to 60000 to never detach

// ------------------------------------------------------------------ LED
const uint8_t  LED_MAX     = 200;
const uint8_t  LED_SLIT    = 25;    // the thin line of light in the crack
const uint32_t T_PUPIL     = 1500;

// ---------------------------------------------------------- POWER
// Set to 1 only with the soft-latch installed and no USB attached,
// otherwise the board will power itself off after every interaction.
#define CON_LATCH 0
// 0 = bench test without a PIR: suspicion is triggered by the ultrasonic.
#define CON_PIR   0

const uint8_t  PIN_LATCH    = 4;     // HIGH = keep the power on
const uint32_t T_SHUTDOWN   = 1500;  // quiet time required before cutting power

// ---------------------------------------------------------------- STATES
enum State { SLEEPING, SUSPECT, OPENING, CONTACT, FAREWELL };
State state = SLEEPING;

Servo servo;
bool  servoAttached = false;
int   angle = ANG_CLOSED;

struct { float from, to; uint32_t t0, dur; bool active; uint32_t tEnd; } tw = {0, 0, 0, 1, false, 0};

// distance
int      samples[SAMPLE_COUNT];
uint8_t  sampleIdx = 0;
int      distance  = 400;
uint32_t lastReadTime = 0;

// LED
float ledNow = 0, ledTarget = 0;
uint32_t tLed = 0;

// condition timers
uint32_t tSuspect = 0, tNear = 0, tGone = 0, tOpenStart = 0;

bool verbose = false;

// ====================================================================
void setup() {
#if CON_LATCH
  pinMode(PIN_LATCH, OUTPUT);
  digitalWrite(PIN_LATCH, HIGH);      // before anything else: latch yourself alive
#endif

  Serial.begin(115200);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_LED, OUTPUT);
#if CON_PIR
  pinMode(PIN_PIR, INPUT);            // the PIR module already has a push-pull output
#endif
  analogWrite(PIN_LED, 0);

  for (uint8_t i = 0; i < SAMPLE_COUNT; i++) samples[i] = 400;

  attachServo();
  servo.write(ANG_CLOSED);
  delay(300);
  detachServo();

  tSuspect = tNear = tGone = millis();
  tLed = millis();
  Serial.println(F("android_eye v2. 'v' verbose, 'o' open, 'c' close, 'd' read distance."));
#if CON_PIR
  Serial.println(F("PIR: wait ~60 s after the very first power-up before trusting it."));
#endif
}

// ====================================================================
void loop() {
  serialCommands();

  bool moving = (state == OPENING || state == FAREWELL);
  if (!moving) readDistance();        // pulseIn blocks: never during servo motion

  bool arrived = updateServo();
  updateLed();
  stateMachine(arrived);
#if CON_LATCH
  handleLatch();
#endif
}

// -------------------------------------------------- the two senses, split
bool pirPresent() {
#if CON_PIR
  return digitalRead(PIN_PIR) == HIGH;
#else
  return distance < D_ANTICIPATE;     // fallback: ultrasonic only
#endif
}

// ---------------------------------------------------------- state machine
void stateMachine(bool arrived) {
  bool near = (distance < D_NEAR);
  bool gone = (distance > D_AWAY);

  switch (state) {

    case SLEEPING:
      if (!pirPresent()) { tSuspect = millis(); break; }
      if (millis() - tSuspect >= T_SUSPECT_CONFIRM) changeState(SUSPECT);
      break;

    case SUSPECT:
      if (near) {
        if (millis() - tNear >= T_NEAR_CONFIRM) { changeState(OPENING); break; }
      } else {
        tNear = millis();
      }
      // nobody moving any more AND the ultrasonic sees nobody -> close again
      if (!pirPresent() && gone) {
        if (millis() - tGone >= T_ABANDON) changeState(FAREWELL);
      } else {
        tGone = millis();
      }
      break;

    case OPENING:
      if (arrived) changeState(CONTACT);
      break;

    case CONTACT: {
      bool minOpen = (millis() - tOpenStart) >= T_MIN_OPEN;
      bool nobody  = !pirPresent() && gone;
      if (minOpen && nobody) {
        if (millis() - tGone >= T_ABANDON) changeState(FAREWELL);
      } else {
        tGone = millis();
      }
      break;
    }

    case FAREWELL:
      // second thoughts: if someone shows up mid-close, open again
      if (!pirPresent()) {
        tSuspect = millis();
      } else if (millis() - tSuspect >= T_SUSPECT_CONFIRM) {
        changeState(SUSPECT);
        break;
      }
      if (arrived) changeState(SLEEPING);
      break;
  }
}

void changeState(State next) {
  if (verbose) {
    Serial.print(F("["));
    Serial.print(millis());
    Serial.print(F("] "));
    Serial.print(stateName(state));
    Serial.print(F(" -> "));
    Serial.print(stateName(next));
    Serial.print(F("  d="));
    Serial.print(distance);
    Serial.print(F("  pir="));
    Serial.println(pirPresent() ? 1 : 0);
  } else {
    Serial.print(F("-> ")); Serial.println(stateName(next));
  }

  state = next;
  tSuspect = tNear = tGone = millis();

  switch (next) {
    case SLEEPING: moveTo(ANG_CLOSED, 400);        ledTarget = 0;         break;
    case SUSPECT:  moveTo(ANG_SLIT,   T_SLIT);     ledTarget = LED_SLIT;  break;
    case OPENING:  moveTo(ANG_OPEN,   T_OPEN);     ledTarget = LED_MAX;
                   tOpenStart = millis();                                 break;
    case CONTACT:  moveTo(ANG_OPEN,   200);        ledTarget = LED_MAX;   break;
    case FAREWELL: moveTo(ANG_GLANCE, T_GLANCE);   ledTarget = 0;         break;
  }
}

// ------------------------------------------------------------------ servo
void attachServo() {
  if (!servoAttached) { servo.attach(PIN_SERVO); servo.write(angle); servoAttached = true; }
}
void detachServo() {
  if (servoAttached) { servo.detach(); servoAttached = false; }
}

void moveTo(int target, uint32_t dur) {
  attachServo();
  tw.from   = angle;
  tw.to     = target;
  tw.t0     = millis();
  tw.dur    = dur ? dur : 1;
  tw.active = true;
}

float ease(float x) {                 // cubic ease-in-out
  if (x <= 0) return 0;
  if (x >= 1) return 1;
  if (x < 0.5f) return 4 * x * x * x;
  float y = 1 - x;
  return 1 - 4 * y * y * y;
}

bool updateServo() {                  // true when the movement is finished
  if (!tw.active) {
    if (servoAttached && millis() - tw.tEnd > T_SERVO_RELEASE) detachServo();
    return true;
  }

  float x = (float)(millis() - tw.t0) / (float)tw.dur;

  if (x >= 1.0f) {
    angle = (int)tw.to;
    servo.write(angle);
    tw.active = false;
    tw.tEnd   = millis();

    if (state == FAREWELL && angle == ANG_GLANCE) {   // second phase: slow close
      moveTo(ANG_CLOSED, T_CLOSE);
      return false;
    }
    return true;
  }

  angle = (int)(tw.from + (tw.to - tw.from) * ease(x) + 0.5f);
  servo.write(angle);
  return false;
}

// -------------------------------------------------------------------- LED
void updateLed() {
  uint32_t now = millis();
  float dt = (float)(now - tLed);
  tLed = now;

  float step = ((float)LED_MAX / (float)T_PUPIL) * dt;

  if (ledNow < ledTarget)      { ledNow += step; if (ledNow > ledTarget) ledNow = ledTarget; }
  else if (ledNow > ledTarget) { ledNow -= step; if (ledNow < ledTarget) ledNow = ledTarget; }

  analogWrite(PIN_LED, (int)ledNow);
}

// --------------------------------------------------------------- distance
void readDistance() {
  if (millis() - lastReadTime < 30) return;
  lastReadTime = millis();

  digitalWrite(PIN_TRIG, LOW);  delayMicroseconds(3);
  digitalWrite(PIN_TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  unsigned long us = pulseIn(PIN_ECHO, HIGH, 30000UL);

  int cm = us ? (int)(us / 58UL) : 400;
  if (cm <= 0)  cm = 400;
  if (cm > 400) cm = 400;

  samples[sampleIdx] = cm;
  sampleIdx = (sampleIdx + 1) % SAMPLE_COUNT;
  distance = medianValue();

  if (verbose && (millis() % 500 < 32)) {
    Serial.print(F("   d=")); Serial.print(distance);
    Serial.print(F(" cm  pir=")); Serial.println(pirPresent() ? 1 : 0);
  }
}

int medianValue() {
  int v[SAMPLE_COUNT];
  for (uint8_t i = 0; i < SAMPLE_COUNT; i++) v[i] = samples[i];
  for (uint8_t i = 1; i < SAMPLE_COUNT; i++) {          // insertion sort
    int k = v[i], j = i - 1;
    while (j >= 0 && v[j] > k) { v[j + 1] = v[j]; j--; }
    v[j + 1] = k;
  }
  return v[SAMPLE_COUNT / 2];
}

// ------------------------------------------------------------ soft-latch
void handleLatch() {
  static uint32_t tAllStill = 0;

  bool still = (state == SLEEPING) && !tw.active && !pirPresent() && (distance >= D_ANTICIPATE);

  if (!still) {
    tAllStill = millis();
    digitalWrite(PIN_LATCH, HIGH);
    return;
  }

  if (millis() - tAllStill > T_SHUTDOWN) {
    Serial.println(F("-- power off"));
    Serial.flush();
    digitalWrite(PIN_LATCH, LOW);     // the latch opens: everything dies
  }
}

// ---------------------------------------------------------------- serial
void serialCommands() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == 'v') verbose = !verbose;
    else if (c == 'o') changeState(OPENING);
    else if (c == 'c') changeState(FAREWELL);
    else if (c == 'd') { Serial.print(F("distance: ")); Serial.print(distance); Serial.println(F(" cm")); }
  }
}

const __FlashStringHelper* stateName(State s) {
  switch (s) {
    case SLEEPING: return F("SLEEPING");
    case SUSPECT:  return F("SUSPECT");
    case OPENING:  return F("OPENING");
    case CONTACT:  return F("CONTACT");
    case FAREWELL: return F("FAREWELL");
  }
  return F("?");
}
