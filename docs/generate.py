#!/usr/bin/env python3
"""Generate the wiring and state diagrams for android-eye.

Run from anywhere:  python3 docs/generate.py
The two SVG files land next to this script; commit them with the change.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
WIRE = {
    "5v": "#d62828", "gnd": "#1b1b1b", "trig": "#2a9d8f", "echo": "#3a7ca5",
    "servo": "#e07a1f", "pir": "#7b2cbf", "led": "#c9a227", "latch": "#6c757d",
}
HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        'viewBox="0 0 {w} {h}" font-family="' + FONT + '">\n')


def wire(pts, color, width=3.2, dash=None):
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="{width + 4.5}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{da}/>\n')


def dot(x, y, color, r=4.4):
    return (f'<circle cx="{x}" cy="{y}" r="{r+2.2}" fill="#ffffff"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>\n')


def text(x, y, s, size=13, fill="#1b1b1b", anchor="start", weight="normal",
         spacing=0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{ls}>{s}</text>\n')


def pin(x, y, w=26, h=20):
    return (f'<rect x="{x}" y="{y - h/2}" width="{w}" height="{h}" rx="3" '
            f'fill="#c9b458" stroke="#8a7430" stroke-width="1.2"/>\n')


# ======================================================================
# 1. wiring
# ======================================================================
W, H = 1440, 1215
s = [HEAD.format(w=W, h=H)]
s.append(f'<rect width="{W}" height="{H}" fill="#fbfaf7"/>\n')
s.append(text(60, 58, "ANDROID EYE &#183; ARDUINO UNO WIRING", 27, "#161616",
              weight="bold", spacing="0.3"))
s.append(text(60, 84, "behaviour test bench &#183; all signal levels 5 V &#183; "
              "sketch: android_eye_test.ino", 14, "#5f6b73"))
s.append('<path d="M 60 100 L 1380 100" stroke="#d9d4c8" stroke-width="2"/>\n')

BX0, BX1, BY0, BY1 = 70, 470, 190, 830
s.append(f'<rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" rx="10" '
         f'fill="#1f7a8c" stroke="#0b3d47" stroke-width="2.5"/>\n')
s.append(f'<path d="M {BX0} {BY0+34} L {BX0} {BY0+10} Q {BX0} {BY0} {BX0+10} {BY0} '
         f'L {BX1-10} {BY0} Q {BX1} {BY0} {BX1} {BY0+10} L {BX1} {BY0+34} Z" '
         f'fill="#0b3d47"/>\n')
s.append(text((BX0 + BX1) / 2, BY0 + 24, "ARDUINO UNO R3", 16, "#ffffff",
              anchor="middle", weight="bold", spacing="1"))
s.append(text((BX0 + BX1) / 2, BY0 + 62, "USB powered &#183; 5 V logic", 12.5,
              "#bfe3ea", anchor="middle"))

PADR = BX1 - 4
PADS = []
PY = {"5V": 265, "GND": 305, "D2": 375, "D6": 435, "D7": 495, "D8": 555,
      "D9": 615, "D4": 675, "GND2": 735, "5V2": 785}
LABELS = [("5V", 265), ("GND", 305), ("D2", 375), ("D6~", 435), ("D7", 495),
          ("D8", 555), ("D9", 615), ("D4", 675), ("GND", 735), ("5V", 785)]
for label, y in LABELS:
    PADS.append(pin(BX1 - 30, y))
    s.append(text(BX1 - 40, y + 5.5, label, 13.5, "#ffffff", anchor="end",
                  weight="bold"))

MOD_X0, MOD_X1 = 920, 1350


def module(y0, y1, title, subtitle, pins, dashed=False, fill="#ffffff"):
    g = [f'<rect x="{MOD_X0}" y="{y0}" width="{MOD_X1-MOD_X0}" height="{y1-y0}" '
         f'rx="8" fill="{fill}" stroke="#3d3d3d" stroke-width="2"'
         + (' stroke-dasharray="7 5"' if dashed else '') + '/>\n']
    g.append(text(MOD_X0 + 22, y0 + 30, title, 15.5, "#161616", weight="bold",
                  spacing="0.5"))
    if subtitle:
        g.append(text(MOD_X0 + 22, y0 + 50, subtitle, 12, "#6b6b6b"))
    for name, y in pins:
        PADS.append(pin(MOD_X0 - 26, y))
        g.append(text(MOD_X0 + 12, y + 4.5, name, 11.5, "#5f6b73"))
    return "".join(g)


# HC-SR04 -------------------------------------------------------------
s.append(module(130, 370, "HC-SR04", "ultrasonic &#183; aims 25&#176; down the stairs",
                [("VCC", 200), ("TRIG", 240), ("ECHO", 280), ("GND", 320)]))
for cx in (1110, 1245):
    s.append(f'<circle cx="{cx}" cy="252" r="30" fill="#e8e4d9" stroke="#3d3d3d" stroke-width="1.6"/>\n')
    s.append(f'<circle cx="{cx}" cy="252" r="17" fill="#d3cec0" stroke="#3d3d3d" stroke-width="1.2"/>\n')
s.append(text(1110, 330, "T", 11, "#6b6b6b", anchor="middle"))
s.append(text(1245, 330, "R", 11, "#6b6b6b", anchor="middle"))

# SG90 ----------------------------------------------------------------
s.append(module(400, 640, "SG90 SERVO", "eyelid drive",
                [("GND &#183; brown", 470), ("VCC &#183; red", 505),
                 ("SIG &#183; orange", 540)]))
s.append('<rect x="1060" y="505" width="180" height="115" rx="8" fill="#5c6b73" stroke="#2f3a40" stroke-width="1.6"/>\n')
s.append('<rect x="1104" y="470" width="56" height="38" rx="5" fill="#37474f"/>\n')
s.append('<circle cx="1132" cy="489" r="12" fill="#cfd8dc" stroke="#2f3a40" stroke-width="1.4"/>\n')
s.append('<rect x="1127" y="452" width="10" height="26" rx="4" fill="#e0a800"/>\n')
s.append(text(1150, 570, "SG90", 13, "#e8eef1", anchor="middle", weight="bold"))
s.append(text(1150, 590, "eyelid arm", 11, "#c3d0d6", anchor="middle"))

# PIR -----------------------------------------------------------------
s.append(module(670, 870, "HC-SR501 PIR", "",
                [("VCC", 730), ("OUT", 770), ("GND", 810)], dashed=True,
                fill="#faf7ff"))
s.append('<circle cx="1190" cy="775" r="52" fill="#f2eefc" stroke="#3d3d3d" stroke-width="1.6"/>\n')
s.append('<circle cx="1190" cy="775" r="38" fill="#ffffff" stroke="#3d3d3d" stroke-width="1.2"/>\n')
s.append(text(1190, 780, "PIR", 11, "#8a86a3", anchor="middle"))
s.append(text(MOD_X0 + 22, 850, "must stay powered while the board is off",
              11.5, "#7b2cbf"))

# signals -------------------------------------------------------------
s.append(wire([(PADR, 495), (770, 495), (770, 240), (MOD_X0 - 8, 240)], WIRE["trig"]))
s.append(wire([(PADR, 555), (830, 555), (830, 280), (MOD_X0 - 8, 280)], WIRE["echo"]))
s.append(wire([(PADR, 615), (860, 615), (860, 540), (MOD_X0 - 8, 540)], WIRE["servo"]))
s.append(wire([(PADR, 375), (880, 375), (880, 770), (MOD_X0 - 8, 770)], WIRE["pir"]))
s.append(wire([(PADR, 675), (560, 675)], WIRE["latch"], dash="8 6"))
s.append(text(474, 663, "D4 &#8594; soft latch gate", 11.5, "#5f6b73"))
s.append(wire([(PADR, 435), (600, 435)], WIRE["led"]))
s.append(text(474, 423, "D6 &#8594; LED panel", 11.5, "#7a6a20"))

# buses ---------------------------------------------------------------
BUS5, BUSG = 640, 700
s.append(wire([(PADR, 305), (BUSG, 305)], WIRE["gnd"]))
s.append(wire([(PADR, 735), (BUSG, 735)], WIRE["gnd"]))
s.append(wire([(BUSG, 305), (BUSG, 810)], WIRE["gnd"]))
s.append(wire([(BUSG, 320), (MOD_X0 - 8, 320)], WIRE["gnd"]))
s.append(wire([(BUSG, 470), (MOD_X0 - 8, 470)], WIRE["gnd"]))
s.append(wire([(BUSG, 810), (MOD_X0 - 8, 810)], WIRE["gnd"]))
for y in (305, 735, 320, 470, 810):
    s.append(dot(BUSG, y, WIRE["gnd"]))

s.append(wire([(PADR, 265), (BUS5, 265)], WIRE["5v"]))
s.append(wire([(PADR, 785), (BUS5, 785)], WIRE["5v"]))
s.append(wire([(BUS5, 200), (BUS5, 785)], WIRE["5v"]))
s.append(wire([(BUS5, 200), (MOD_X0 - 8, 200)], WIRE["5v"]))
s.append(wire([(BUS5, 505), (MOD_X0 - 8, 505)], WIRE["5v"]))
s.append(wire([(BUS5, 730), (MOD_X0 - 8, 730)], WIRE["5v"]))
for y in (265, 785, 200, 505, 730):
    s.append(dot(BUS5, y, WIRE["5v"]))

s.append(text(876, 192, "5V", 10.5, WIRE["5v"], anchor="middle", weight="bold"))
s.append(text(876, 312, "GND", 10.5, "#1b1b1b", anchor="middle", weight="bold"))

# LED panel -----------------------------------------------------------
LX0, LY0, LX1, LY1 = 70, 880, 640, 1050
s.append(f'<rect x="{LX0}" y="{LY0}" width="{LX1-LX0}" height="{LY1-LY0}" rx="8" '
         f'fill="#fffbef" stroke="#c9a227" stroke-width="2"/>\n')
s.append(text(LX0 + 20, LY0 + 28, "LED (PUPIL) &#8212; D6", 15, "#5c4a08",
              weight="bold", spacing="0.5"))
s.append(text(LX0 + 20, LY0 + 47, "220 &#937; in series, anode towards D6", 12, "#7a6a20"))

ly = 990
s.append(wire([(LX0 + 20, ly), (LX0 + 120, ly)], WIRE["led"]))
s.append(text(LX0 + 24, ly - 9, "from D6", 10.5, "#7a6a20"))
rx = LX0 + 120
pts = [(rx, ly)]
for i in range(6):
    pts.append((rx + 12 + i * 12, ly + (-13 if i % 2 == 0 else 13)))
pts += [(rx + 84, ly), (rx + 100, ly)]
s.append(wire(pts, "#5c4a08", width=2.6))
s.append(text(rx + 50, ly + 36, "220 &#937;", 11.5, "#5c4a08", anchor="middle"))
lx = rx + 100
s.append(wire([(lx, ly), (lx + 26, ly)], WIRE["led"]))
s.append(f'<path d="M {lx+26} {ly-15} L {lx+26} {ly+15} L {lx+56} {ly} Z" '
         f'fill="{WIRE["led"]}" stroke="#7a6a20" stroke-width="1.6"/>\n')
s.append(f'<path d="M {lx+58} {ly-15} L {lx+58} {ly+15}" stroke="#7a6a20" stroke-width="3"/>\n')
for dy in (0, 16):
    s.append(f'<path d="M {lx+70} {ly-24+dy} l 16 -11" stroke="#7a6a20" stroke-width="1.6"/>\n'
             f'<path d="M {lx+80} {ly-35+dy} l -2 8 l 7 -2" stroke="#7a6a20" '
             f'stroke-width="1.6" fill="none"/>\n')
s.append(wire([(lx + 58, ly), (LX1 - 22, ly)], WIRE["gnd"]))
s.append(text(LX1 - 26, ly - 9, "to GND", 10.5, "#1b1b1b", anchor="end"))

# legend --------------------------------------------------------------
GX, GY = 700, 892
s.append(text(GX, GY + 20, "LEGEND", 12, "#5f6b73", weight="bold", spacing="1.2"))
items = [("5 V", "5v"), ("GND", "gnd"), ("TRIG &#183; D7", "trig"),
         ("ECHO &#183; D8", "echo"), ("servo signal &#183; D9", "servo"),
         ("PIR out &#183; D2", "pir"), ("LED &#183; D6", "led"),
         ("soft-latch gate &#183; D4", "latch")]
for i, (label, key) in enumerate(items):
    x = GX + (i // 4) * 330
    y = GY + 52 + (i % 4) * 34
    dash = ' stroke-dasharray="7 5"' if key == "latch" else ""
    s.append(f'<path d="M {x} {y} L {x+36} {y}" stroke="{WIRE[key]}" '
             f'stroke-width="3.4"{dash}/>\n')
    s.append(text(x + 46, y + 4.5, label, 12.5, "#3d3d3d"))

# notes ---------------------------------------------------------------
NX0, NX1, NY0 = 70, 1350, 1075
s.append(f'<rect x="{NX0}" y="{NY0}" width="{NX1-NX0}" height="105" rx="8" '
         f'fill="#ffffff" stroke="#d9d4c8" stroke-width="1.6"/>\n')
s.append(text(NX0 + 20, NY0 + 26, "NOTES", 12, "#5f6b73", weight="bold", spacing="1.2"))
notes = [
    "D9 and D10 lose PWM while the Servo library is linked: expected, not a fault.",
    "On the bench the SG90 runs from the board 5 V; on site give it its own 5 V supply and tie the grounds together.",
    "ECHO outputs 5 V: keep the board at 5 V logic, no level shifter needed. The HC-SR04 wants at least 10 &#181;s on TRIG.",
    "D4 stays unused until the soft-latch circuit is installed: leave CON_LATCH at 0.",
]
for i, n in enumerate(notes):
    s.append(text(NX0 + 20, NY0 + 48 + i * 17, "&#8226; " + n, 12, "#4a4a4a"))
s.extend(PADS)
s.append("</svg>\n")
open(f"{OUT}/wiring.svg", "w").write("".join(s))
print("wrote wiring.svg")


# ======================================================================
# 2. state machine
# ======================================================================
W2, H2 = 1640, 600
s = [HEAD.format(w=W2, h=H2)]
s.append(f'<rect width="{W2}" height="{H2}" fill="#fbfaf7"/>\n')
s.append(text(60, 58, "ANDROID EYE &#183; BEHAVIOUR", 27, "#161616",
              weight="bold", spacing="0.3"))
s.append(text(60, 84, "five states, one eyelid &#183; what the sensors decide and "
              "where the eyelid sits", 14, "#5f6b73"))
s.append('<path d="M 60 100 L 1580 100" stroke="#d9d4c8" stroke-width="2"/>\n')

STATES = [
    ("SLEEPING", "6&#176;", "off", "#e9ecef", "#495057",
     "eyelid closed, nobody around"),
    ("SUSPECT", "21&#176;", "25", "#fff3cd", "#8a6d1a",
     "something moved &#183; a crack of light"),
    ("OPENING", "96&#176;", "200", "#d8f3dc", "#2d6a4f", "real opening, fast"),
    ("CONTACT", "96&#176;", "200", "#c7e9d0", "#2d6a4f", "eye open, pupil dilating"),
    ("FAREWELL", "101&#176; &#8594; 6&#176;", "off", "#dbe7f3", "#2b4c6f",
     "last glance, then slow close"),
]
BW, BH, BY, GAP = 200, 132, 240, 120
xs = [70 + i * (BW + GAP) for i in range(5)]
for (name, ang, led, fill, stroke, caption), x in zip(STATES, xs):
    s.append(f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="10" fill="{fill}" '
             f'stroke="{stroke}" stroke-width="2.5"/>\n')
    s.append(text(x + BW / 2, BY + 42, name, 18, "#161616", anchor="middle",
                  weight="bold", spacing="1"))
    s.append(text(x + BW / 2, BY + 70, caption, 11, "#5f6b73", anchor="middle"))
    s.append(text(x + BW / 2, BY + 98, f"eyelid {ang}", 14, "#3d3d3d",
                  anchor="middle", weight="bold"))
    s.append(text(x + BW / 2, BY + 118, f"LED {led}", 12, "#7a6a20", anchor="middle"))

ARROW = "#6b6b6b"
s.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" '
         'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ARROW}"/></marker>'
         f'<marker id="ap" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
         f'markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{WIRE["pir"]}"/></marker></defs>\n')

TRANS = [
    (["PIR high for", "120 ms"], 0, 1),
    (["distance &lt; 100 cm", "for 130 ms"], 1, 2),
    (["servo arrived"], 2, 3),
    (["open 4 s at least,", "then 900 ms quiet"], 3, 4),
]
for lines, a, b in TRANS:
    x1 = xs[a] + BW
    x2 = xs[b]
    s.append(f'<path d="M {x1} {BY+BH/2} L {x2-2} {BY+BH/2}" stroke="{ARROW}" '
             f'stroke-width="2.4" fill="none" marker-end="url(#ah)"/>\n')
    cx = (x1 + x2) / 2
    for i, line in enumerate(lines):
        s.append(text(cx, BY + BH / 2 - 27 + i * 14, line, 10.5, "#5f6b73",
                      anchor="middle"))

# farewell -> sleeping
fx = xs[4] + BW / 2
sx = xs[0] + BW / 2
s.append(f'<path d="M {fx} {BY+BH} L {fx} {BY+BH+90} L {sx} {BY+BH+90} '
         f'L {sx} {BY+BH+6}" stroke="{ARROW}" stroke-width="2.4" fill="none" '
         f'marker-end="url(#ah)"/>\n')
s.append(text((fx + sx) / 2, BY + BH + 82, "servo arrived: the eyelid is closed "
              "again", 11.5, "#5f6b73", anchor="middle"))

# farewell -> suspect
s.append(f'<path d="M {xs[4]+BW/2} {BY} L {xs[4]+BW/2} {BY-72} '
         f'L {xs[1]+BW/2} {BY-72} L {xs[1]+BW/2} {BY-6}" stroke="{WIRE["pir"]}" '
         f'stroke-width="2.4" fill="none" marker-end="url(#ap)"/>\n')
s.append(text((xs[4] + xs[1]) / 2 + BW / 2, BY - 80,
              "second thoughts: movement inside 120 ms", 11.5, WIRE["pir"],
              anchor="middle"))

s.append(text(60, 512, "The PIR decides whether to suspect, the ultrasonic sensor "
              "decides whether to open.", 13, "#4a4a4a"))
s.append(text(60, 534, "Opening takes 620 ms, closing 2600 ms: that ratio is what "
              "makes the eyelid read as alive, not the absolute speed.", 13, "#4a4a4a"))
s.append(text(60, 562, "Escape hatches: SUSPECT closes again after 900 ms of nobody "
              "in range, FAREWELL reopens on movement.", 13, "#5f6b73"))
s.append("</svg>\n")
open(f"{OUT}/states.svg", "w").write("".join(s))
print("wrote states.svg")
