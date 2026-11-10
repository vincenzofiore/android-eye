# Android Eye — project plan

The working document for the installation: the idea, the design, the
technical details, the decision trail, and the steps to mark as done.

This is not the code documentation. The code is
`android_eye_test/android_eye_test.ino`; the bench notes are in `README.md`;
the drawings are in `docs/`; the shopping list is `docs/bom.md`.

Status: **prototype, design approved, not yet built.** Last updated 2026-11-10.

---

## 1. The idea

A wall-mounted face on a staircase. The eye is mechanical: an eyelid opens and
a pupil lights up when someone passes. It is the third piece of a triptych,
after a portrait of Rosa Luxemburg and an African mask.

The piece is a **half face, seen from the front**: a plain panel of plywood,
the left half of a face, with the right side missing. It is a fragment, not a
figure — it declares that it has been taken out of a whole, not that it is a
whole.

The triptych is the same face three times. The piece is the only one that is a
**machine**. The mask is the piece that comes just before it: it has **closed,
sculpted eyes**, not realistic. The piece is therefore the only one of the
three that starts closed, and the only one that opens. That is the break in the
series: the mask is closed and stays closed; the piece is closed and opens.

### The triptych as a sequence

The three pieces are **50 cm apart**, on the same wall, in the order of the
climb. The eyes are at **173 cm**, **150 cm** and **127 cm** above the tread of
each piece. The eyes are not at the same height: the triptych is a descent of
the eyes, and the piece is the lowest of the three.

### The light

The light comes from the **top** of the staircase: from the skylight in day,
from the artificial light at the top of the stairs in the evening. It is frontal
on the portrait and the mask, and **lateral** on the piece, from the opposite
side of the climb. The piece is the only one seen in contre-jour, and the light
is what makes its profile read as a silhouette.

---

## 2. The design

### 2.1 The piece

| | |
|---|---|
| Overall | half face, front view, 334 mm tall, 115 mm wide, 36 mm deep |
| Panels | two 18 mm plywood, glued face to face |
| Contour | 3 mm bevel on the front edge of the back panel, a 3 × 3 mm shadow line along the whole contour |
| Neck | **none**; the piece ends at the jaw |
| Ear | on the right, vertical panel, 18 mm plywood, orthogonal to the face plane, a single simplified silhouette |
| Eye | Ø46 socket, 12 mm deep, 238 mm from the chin, 40 % of the face width |
| Nose | half, a wedge, 28 mm out of the face at the tip |
| Mouth | a recess, 90 × 14 mm, 4 mm deep, not a piece |
| Brow | slanted strip, 60 mm long, 12 mm thick, 7 mm slope |
| Chin | block, 27 × 26 × 18 mm |
| PIR | forehead, Ø32, in the dome |
| HC-SR04 | in the ear, two Ø16 holes for the transducers |
| Cable | 6 mm groove in the back panel |

The relief pieces are not a model: they are the senses. The nose is the sense of
the nose, the ear is the sense of the HC-SR04, the mouth is the recess of the
mouth. The eye is the only sense that is a mechanism.

### 2.2 The eye

| | |
|---|---|
| Ball | Ø35 mm, plastic, rotated so the pupil faces the viewer |
| Pivot | through the ball's centre, horizontal, parallel to the wall |
| Eyelid | 90° of arc, 6° to 96°, 27.5 mm of travel on the 17.5 mm radius |
| Stop | a pin at 96°, so the servo never has to be tuned |
| Servo | SG90, behind the front panel, horn in a slot |
| Friction | a short silicone tube on the pivot |
| LED | inside the ball, 5 mm, warm white or amber, with a connector in the wire |

The eyelid is a shell, not a flat piece: it follows the 17.5 mm radius. It is
the same closed as the mask: the same closed, the same shadow, the same quiet.
The piece opens the mask's eye.

---

## 3. Technical details

### 3.1 The board

| | |
|---|---|
| Board | Arduino Nano v3, CH340 |
| Pins | D7 TRIG, D8 ECHO, D9 SERVO, D6 LED, D2 PIR, D4 LATCH |
| Power | 4×AA NiMH, 2000 mAh, 4.8 V, on the 5 V pin |
| Servo | from the switched rail, not from the Nano's 5 V |
| Latch | P-MOSFET Q1, NPN Q2, R1 100 k, R2/R3 10 k, 470 µF |
| Serial | 115200 baud, `v` for verbose, `o` / `c` / `d` |

The sketch is the same on the Uno and on the Nano: same pins, same code, same
numbers.

### 3.2 The constants

| Constant | Value | Meaning |
|---|---|---|
| `ANG_CLOSED` | 6° | eyelid on the socket |
| `ANG_SLIT` | 21° | the crack |
| `ANG_OPEN` | 96° | the open |
| `ANG_GLANCE` | 101° | the last glance |
| `D_ANTICIPATE` | 210 cm | the far edge |
| `D_NEAR` | 100 cm | the near edge |
| `D_AWAY` | 150 cm | the hysteresis |
| `T_OPEN` | 620 ms | the opening |
| `T_CLOSE` | 2600 ms | the closing |
| `T_MIN_OPEN` | 4000 ms | the minimum |
| `T_SLIT` | 950 ms | the hesitation |
| `LED_SLIT` | 25 | the light in the crack |
| `LED_MAX` | 200 | the pupil |
| `T_SHUTDOWN` | 1500 ms | the quiet before the latch |
| `CON_LATCH` | 0 | 1 only with the latch and no USB |
| `CON_PIR` | 0 | 1 only with the PIR |

The 1:4 ratio between opening and closing is the design of the movement, not a
parameter to be equalised.

### 3.3 The states

```
SLEEPING  eyelid closed, nobody around
   | PIR triggers
SUSPECT   eyelid cracks open, a thin line of light appears
   | ultrasonic reads < D_NEAR
OPENING   real opening, fast
CONTACT   eye open, pupil dilating
   | nobody moving and nobody in range
FAREWELL  last glance, then slow close
   | movement detected -> back to SUSPECT
SLEEPING
```

### 3.4 The diagrams

| File | What it is |
|---|---|
| `docs/wiring.svg` | the wiring, module by module |
| `docs/states.svg` | the state machine |
| `docs/mechanics.svg` | the ball, the 90° arc, the 27.5 mm |
| `docs/structure.svg` | the half face, front view |
| `docs/template.svg` | the 1:1 panel, A2 |
| `docs/template-a4-p1.svg` / `-p2.svg` | the same panel, two A4 sheets |
| `docs/parts.svg` | the small parts, 1:1 |
| `docs/eye-module.svg` | the eye, 2:1 |
| `docs/latch.svg` | the soft latch |

All of them come from `docs/generate.py`. Run `python3 docs/generate.py` to
regenerate them; do not edit the SVGs by hand.

---

## 4. Decision trail

The decisions that were taken, and the alternatives that were rejected. This is
the part that explains the piece, not the code.

| # | Decision | Alternative rejected | Why |
|---|---|---|---|
| 1 | Half face, front view | full face; profile | a fragment is a fragment; the piece declares that it was taken out of a whole |
| 2 | Two panels, 18 mm, 3 mm bevel | one panel; two panels with a 10 mm inset | the bevel is the shadow line, made by the machine, identical around the perimeter |
| 3 | No neck, the piece ends at the jaw | a neck, the piece ends at the collar | the neck is what was cut away; the cut is the cut |
| 4 | Ear on the right, vertical | ear on the left; ear as a stack of discs | the viewer sees the ear on the right; the ear must be orthogonal to the face so the HC-SR04 points along the stair; the discs were too decorative |
| 5 | 334 mm tall | 250 mm, same as the mask; 360 mm, bigger | 334 keeps the eye in proportion; 250 gives a doll eye; 360 makes the piece the largest |
| 6 | 35 mm ball, in the socket | 24 mm; 46 mm | the ball is the one we have; 35 mm gives 40 % of the face width at 334 |
| 7 | Eye starts closed, citing the mask | eye starts open | the mask has closed eyes; the piece is the only one that opens, so the break is the opening |
| 8 | Batteries, no mains | USB, mains, no latch | no socket on the stairs; the piece must be autonomous |
| 9 | PIR in the forehead, HC-SR04 in the ear | PIR in the ear, HC-SR04 in the nose | the PIR has a wide field and needs no aim; the HC-SR04 needs the direction of the ear, which points along the stair |
| 10 | Nano instead of Uno | Uno; Pro Mini | Uno too big for the cavity; Pro Mini needs FTDI; Nano has the same pins, the same sketch, half the current |
| 11 | 3 mm bevel, not a 1–2 mm inset | 1–2 mm inset | 1–2 mm is lost in wood movement; 3 mm is a deliberate shadow line |
| 12 | Perfboard for the prototype | custom PCB; screw-terminal shield | for one piece, perfboard is enough; the custom PCB only for the final installation |
| 13 | One access, the cheek as the lid | two accesses, the battery and the board | one access is simpler to service and one less seam to hide |

---

## 5. The plan

The steps, in the order they are to be done. Mark each with `[x]` when done.

### 5.1 The design

- [x] The idea, the triptych, the mask
- [x] The half face, front view
- [x] The two panels and the 3 mm bevel
- [x] The eye in proportion, 334 mm
- [x] The ear, the vertical, the HC-SR04
- [x] The diagrams, the 9 SVGs
- [x] The BOM, the soldering
- [x] The 1:1 templates, the A4
- [ ] This project plan

### 5.2 The bench

- [ ] Print the A4 template, check the 100 mm bar
- [ ] Print the A2 template, check the 100 mm bar
- [ ] LED inside the 35 mm ball, in the dark, check the diffusion
- [ ] LED at 25/255 and 200/255, check the crack
- [ ] Servo 6° to 96°, check the 27.5 mm of travel
- [ ] Cardboard eyelid, check the closed against the ball

### 5.3 The wood

- [ ] Cut the two 18 mm panels, 400 × 300
- [ ] Bevel 3 mm at 45°, on the back panel
- [ ] Glue the two panels, face to face
- [ ] Cut the outline from the 1:1 template, once
- [ ] Ø46 eye socket
- [ ] Ø32 PIR
- [ ] Ø16 ear holes
- [ ] 6 mm cable groove
- [ ] Nose, half, wedge
- [ ] Mouth recess, 90 × 14 mm
- [ ] Brow, 60 mm, 7 mm slope
- [ ] Chin, 27 × 26 × 18 mm
- [ ] Eye ring, 12 mm
- [ ] Eyelid shell, 17.5 mm radius
- [ ] Matte black inside the socket

### 5.4 The electronics

- [ ] Solder the latch on perfboard, Q1, Q2, R1, R2, R3
- [ ] Test the latch with no Nano, multimeter on the output
- [ ] Nano on headers, upload the sketch
- [ ] Servo from the switched rail, 470 µF
- [ ] LED with a connector, inside the ball
- [ ] PIR on D2, forehead
- [ ] HC-SR04 on D7 and D8, ear
- [ ] `CON_LATCH` set to 1
- [ ] `CON_PIR` set to 0
- [ ] Battery pack, 4.8 V, check the 5 V rail
- [ ] Check no short between +5 V and GND

### 5.5 The wall

- [ ] Four screws 5 × 50, the panel weighs 1.2 kg
- [ ] Mount the panel on the wall
- [ ] Cable in the 6 mm groove
- [ ] Battery pack in the cheek, behind the lid
- [ ] Nano in the cavity, behind the panels
- [ ] Light from the skylight, lateral
- [ ] Light from the top of the stairs, artificial
- [ ] Triptych, 50 cm to the portrait
- [ ] Triptych, 50 cm to the mask
- [ ] Eyes at 173, 150 and 127 cm

### 5.6 The test

- [ ] Bench: SLEEPING, SUSPECT, OPENING, CONTACT, FAREWELL, SLEEPING
- [ ] Hand at 1 m, the distance reads 100, not 130 or 70
- [ ] 4 s minimum, T_MIN_OPEN, the eye never closes on a passer-by
- [ ] 0.6 s open, 2.6 s close, the 1:4 ratio
- [ ] Latch, D4, T_SHUTDOWN, the board switches off
- [ ] PIR, 60 s warm-up, the first readings are honest
- [ ] Battery, 4.6 V minimum, the servo does not reset the board
- [ ] Servo, no stutter, no buzz
- [ ] Wall: the piece stays, the cable stays, the light stays
- [ ] Open: the eye, the mask, the light, the triptych
