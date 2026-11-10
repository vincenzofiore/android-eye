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
s.append(text(LX0 + 20, LY0 + 47, "220 &#937; in series, anode towards D6 &#183; "
              "fits inside the 35 mm plastic ball", 12, "#7a6a20"))

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


# ======================================================================
# 3. mechanics
# ======================================================================
import math

W3, H3 = 1400, 900
s = [HEAD.format(w=W3, h=H3)]
s.append(f'<rect width="{W3}" height="{H3}" fill="#fbfaf7"/>\n')
s.append(text(60, 58, "ANDROID EYE &#183; MECHANICS", 27, "#161616",
              weight="bold", spacing="0.3"))
s.append(text(60, 84, "35 mm plastic ball &#183; where the eyelid has to go &#183; "
              "side view, schematic", 14, "#5f6b73"))
s.append('<path d="M 60 100 L 1340 100" stroke="#d9d4c8" stroke-width="2"/>\n')

CX, CY, R = 470, 470, 210          # 210 px = 17.5 mm -> 12 px per mm
MM = 12.0


def pt(theta, radius=R):
    return (CX + radius * math.cos(math.radians(theta)),
            CY - radius * math.sin(math.radians(theta)))


def fmt(p):
    return f"{p[0]:.1f} {p[1]:.1f}"


FRONT, TOP = 180.0, 95.0           # aperture runs from the front to the top

# ball
s.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#efeade" stroke="#3d3d3d" '
         f'stroke-width="2.6"/>\n')
s.append(f'<circle cx="{CX}" cy="{CY}" r="{R-16}" fill="none" stroke="#cfc8b6" '
         f'stroke-width="1.4" stroke-dasharray="5 5"/>\n')

# aperture wedge
a0, a1 = FRONT, TOP
s.append(f'<path d="M {fmt(pt(a0, R))} A {R} {R} 0 0 1 {fmt(pt(a1, R))} L {CX} {CY} Z" '
         f'fill="#dbe7f3" stroke="#8fb2cf" stroke-width="1.6" stroke-dasharray="6 5"/>\n')

# pupil, centred in the aperture
PUP_TH, PUP_R = (FRONT + TOP) / 2, 0.70 * R
pp = pt(PUP_TH, PUP_R)
s.append(f'<circle cx="{pp[0]:.1f}" cy="{pp[1]:.1f}" r="46" '
         f'fill="#c9a227" stroke="#8a6d1a" stroke-width="1.6"/>\n')
s.append(text(pp[0], pp[1] + 5, "pupil", 11, "#5c4a08", anchor="middle"))

# closed eyelid: annular band over the aperture
RO = R + 34
s.append(f'<path d="M {fmt(pt(a0, RO))} A {RO} {RO} 0 0 1 {fmt(pt(a1, RO))} '
         f'L {fmt(pt(a1, R+4))} A {R+4} {R+4} 0 0 0 {fmt(pt(a0, R+4))} Z" '
         f'fill="#37474f" stroke="#1f2a30" stroke-width="1.8"/>\n')
_lx, _ly = pt(152, R + 19)
s.append(f'<text x="{_lx:.1f}" y="{_ly:.1f}" font-size="11" fill="#e8eef1" '
         f'text-anchor="middle" font-weight="bold" '
         f'transform="rotate({152-270} {_lx:.1f} {_ly:.1f})">eyelid, closed</text>\n')

# leading-edge positions
LID_ANGLES = [(180, 306, "end", -8, "6&#176; closed", "#1f2a30"),
              (165, 352, "end", -8, "21&#176; slit", "#8a6d1a"),
              (95, 300, "start", 10, "96&#176; open", "#2d6a4f"),
              (85, 352, "start", 10, "101&#176; glance", "#2b4c6f")]
for theta, lr, anchor, off, label, col in LID_ANGLES:
    inner, outer = pt(theta, R - 12), pt(theta, RO + 42)
    s.append(f'<path d="M {fmt(inner)} L {fmt(outer)}" stroke="{col}" stroke-width="1.8" '
             f'stroke-dasharray="7 5" opacity="0.85"/>\n')
    lab = pt(theta, lr)
    s.append(text(lab[0] + off, lab[1], label, 11.5, col, anchor=anchor,
                  weight="bold"))

# travel arc
ARC = RO + 96
p_start, p_end = pt(FRONT, ARC), pt(TOP, ARC)
s.append(f'<path d="M {fmt(p_start)} A {ARC} {ARC} 0 0 1 {fmt(p_end)}" fill="none" '
         f'stroke="#6b6b6b" stroke-width="2" marker-end="url(#am)"/>\n')
s.append('<defs><marker id="am" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
         'markerHeight="7" orient="auto-start-reverse">'
         '<path d="M 0 0 L 10 5 L 0 10 z" fill="#6b6b6b"/></marker></defs>\n')
mp = pt(120, 378)
s.append(text(mp[0], mp[1], "27.5 mm of travel", 12.5, "#3d3d3d", anchor="middle",
              weight="bold"))

# centre and pivot axis
s.append(f'<path d="M {CX} {CY-330} L {CX} {CY+300}" stroke="#6b6b6b" stroke-width="1.4" '
         f'stroke-dasharray="14 4 4 4"/>\n')
s.append(f'<circle cx="{CX}" cy="{CY}" r="6" fill="#ffffff" stroke="#3d3d3d" stroke-width="2"/>\n')
s.append(text(CX + 12, CY + 320, "pivot axis through the ball centre", 12, "#5f6b73"))

# radius
rp = pt(215, R)
s.append(f'<path d="M {CX} {CY} L {fmt(rp)}" stroke="#3d3d3d" stroke-width="1.6"/>\n')
mid = pt(215, R * 0.55)
s.append(text(mid[0] - 6, mid[1], "r 17.5 mm", 12.5, "#3d3d3d", anchor="end",
              weight="bold"))

# diameter
s.append(f'<path d="M {CX-R} {CY} L {CX+R} {CY}" stroke="#3d3d3d" stroke-width="1.4" '
         f'marker-start="url(#am)" marker-end="url(#am)"/>\n')
s.append(text(CX + R + 18, CY + 5, "&#8960; 35 mm", 13, "#3d3d3d", weight="bold"))

# ---------------------------------------------------------------- table
TX, TY = 880, 150
s.append(text(TX, TY, "WHAT EACH ANGLE MEANS", 13, "#5f6b73", weight="bold",
              spacing="1.2"))
TX = 850
cols = [(TX, "servo"), (TX + 84, "lid edge"), (TX + 180, "aperture"),
        (TX + 276, "gap"), (TX + 370, "state")]
for x, c in cols:
    s.append(text(x, TY + 30, c, 11.5, "#8a8a8a", weight="bold"))
s.append(f'<path d="M {TX} {TY+40} L {TX+470} {TY+40}" stroke="#d9d4c8" '
         f'stroke-width="1.6"/>\n')

ROWS = [
    ("6&#176;", "180&#176;", "0&#176;", "0 mm", "closed, on the socket"),
    ("21&#176;", "165&#176;", "15&#176;", "4.6 mm", "the line of light"),
    ("96&#176;", "95&#176;", "90&#176;", "27.5 mm", "pupil fully out"),
    ("101&#176;", "85&#176;", "95&#176;", "29 mm", "last glance"),
]
for i, row in enumerate(ROWS):
    y = TY + 68 + i * 34
    for x, cell in zip([c[0] for c in cols], row):
        s.append(text(x, y, cell, 12.5 if x != TX + 370 else 11.5,
                      "#161616" if x == TX else "#3d3d3d",
                      weight="bold" if x == TX else "normal"))
    s.append(f'<path d="M {TX} {y+10} L {TX+470} {y+10}" stroke="#eee8da" '
             f'stroke-width="1"/>\n')

# ---------------------------------------------------------------- notes
NX, NY = 850, 420
s.append(text(NX, NY, "WHY IT IS BUILT LIKE THIS", 13, "#5f6b73", weight="bold",
              spacing="1.2"))
NOTES = [
    ("The lid turns about an axis through the ball centre, so it needs no track: "
     "it simply slides on the sphere and its curvature is fixed for free."),
    ("The shell must be curved to r 17.5 mm. Flat cardboard touches the ball only "
     "in the middle and leaves two crescents of light."),
    ("A 20 mm pupil needs about 70&#176; of aperture to be fully uncovered: the "
     "90&#176; of travel leaves margin, so the limit is timing, not geometry."),
    ("The silicone clutch on the axle holds the lid wherever the servo leaves it, "
     "so detaching the servo does not drop the eyelid, and the servo carries the "
     "lid only while it is moving."),
]
y = NY + 30
for n in NOTES:
    s.append(text(NX, y, "&#8226;", 13, "#5f6b73"))
    # naive wrap at 62 characters
    words, line, lines = n.split(" "), "", []
    for w in words:
        probe = (line + " " + w).strip()
        if len(probe) > 62:
            lines.append(line)
            line = w
        else:
            line = probe
    lines.append(line)
    for i, ln in enumerate(lines):
        s.append(text(NX + 16, y + i * 18, ln, 12.5, "#4a4a4a"))
    y += 18 * len(lines) + 14

# scale hint
s.append(text(70, 860, "Scale: 12 px per mm. The eyelid thickness is exaggerated "
              "to stay readable.", 11.5, "#8a8a8a"))

s.append("</svg>\n")
open(f"{OUT}/mechanics.svg", "w").write("".join(s))
print("wrote mechanics.svg")


# ======================================================================
# 4. structure: half face seen from the front. All figures in mm.
# ======================================================================
W4, H4 = 1240, 900
s = [HEAD.format(w=W4, h=H4)]
s.append(f'<rect width="{W4}" height="{H4}" fill="#fbfaf7"/>\n')
s.append(text(50, 56, "ANDROID EYE &#183; HALF FACE, FRONT VIEW", 26, "#161616",
              weight="bold", spacing="0.3"))
s.append(text(50, 82, "360 mm head, no neck, eye in proportion &#183; two identical "
              "18 mm panels, 3 mm bevel &#183; figures in millimetres, not to scale",
              13.5, "#5f6b73"))
s.append('<path d="M 50 98 L 1190 98" stroke="#d9d4c8" stroke-width="2"/>\n')

K = 1.44                       # 250 mm reference -> 360 mm head
S4 = 1.28                      # px per real millimetre
AX, AY = 132, 752              # bottom-left of the piece


def F(px, py):
    return (AX + px * K * S4, AY - py * K * S4)


OUTLINE = [
    ("M", 0, 18),
    ("C", 3, 24, 8, 31, 15, 38),
    ("C", 27, 50, 42, 64, 54, 76),
    ("L", 60, 86),
    ("C", 63, 100, 65, 116, 66, 130),
    ("C", 67, 144, 66, 156, 64, 168),
    ("C", 62, 182, 57, 194, 50, 206),
    ("C", 42, 222, 28, 238, 14, 247),
    ("C", 8, 250, 3, 251, 0, 250),
    ("L", 0, 18),
]
parts = []
for seg in OUTLINE:
    cmd, c = seg[0], seg[1:]
    pts = " ".join(f"{F(c[i], c[i+1])[0]:.1f} {F(c[i], c[i+1])[1]:.1f}"
                   for i in range(0, len(c), 2))
    parts.append(f"{cmd} {pts}")
outline_d = parts[0] + " " + " ".join(parts[1:]) + " Z"
s.append(f'<path d="{outline_d}" fill="#e8dcc4" stroke="#5a4a30" stroke-width="2.4"/>\n')


def piece(x0, y0, x1, y1, fill="#cbb894"):
    return (f'<rect x="{F(x0,y1)[0]:.1f}" y="{F(x0,y1)[1]:.1f}" width="{(x1-x0)*K*S4:.1f}" '
            f'height="{(y1-y0)*K*S4:.1f}" rx="2" fill="{fill}" stroke="#6b5a3e" '
            f'stroke-width="1.5"/>\n')


s.append(piece(0, 130, 13, 175))                  # half nose
s.append(piece(0, 98, 14, 112, fill="#a89372"))    # pseudo mouth: a recess
s.append(piece(0, 22, 19, 40))                     # chin
s.append(f'<path d="M {F(0,182)[0]:.1f} {F(0,182)[1]:.1f} L {F(42,190)[0]:.1f} '
         f'{F(42,190)[1]:.1f} L {F(42,178)[0]:.1f} {F(42,178)[1]:.1f} L '
         f'{F(0,170)[0]:.1f} {F(0,170)[1]:.1f} Z" fill="#cbb894" stroke="#6b5a3e" '
         f'stroke-width="1.5"/>\n')

# eye module
EX, EY = 24, 165
ex, ey = F(EX, EY)
s.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{23*S4:.1f}" fill="#f8f5ec" '
         f'stroke="#3d3d3d" stroke-width="2"/>\n')
s.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{17.5*S4:.1f}" fill="#e3dccb" '
         f'stroke="#3d3d3d" stroke-width="1.8"/>\n')
s.append(f'<path d="M {ex-17.5*S4:.1f} {ey+2:.1f} A {17.5*S4:.1f} {17.5*S4:.1f} 0 0 1 '
         f'{ex+17.5*S4:.1f} {ey+2:.1f} Z" fill="#a89372" stroke="#5a4a30" '
         f'stroke-width="2"/>\n')
s.append(f'<path d="M {ex-16*S4:.1f} {ey+1:.1f} Q {ex:.1f} {ey+7*S4:.1f} '
         f'{ex+16*S4:.1f} {ey+1:.1f}" fill="none" stroke="#5a4a30" stroke-width="1.8"/>\n')
s.append(f'<path d="M {ex-17.5*S4:.1f} {ey-4:.1f} L {ex-17.5*S4:.1f} {ey-26*S4:.1f} '
         f'A {17.5*S4:.1f} {17.5*S4:.1f} 0 0 1 {ex+17.5*S4:.1f} {ey-26*S4:.1f} '
         f'L {ex+17.5*S4:.1f} {ey-4:.1f}" fill="none" stroke="#2d6a4f" '
         f'stroke-width="1.8" stroke-dasharray="7 5"/>\n')

# PIR
px_, py_ = F(38, 202)
s.append(f'<circle cx="{px_:.1f}" cy="{py_:.1f}" r="{16*S4:.1f}" fill="#f2eefc" '
         f'stroke="#7b2cbf" stroke-width="2"/>\n')
s.append(f'<circle cx="{px_:.1f}" cy="{py_:.1f}" r="{11*S4:.1f}" fill="#ffffff" '
         f'stroke="#7b2cbf" stroke-width="1.5"/>\n')

# ear, seen edge-on
s.append(f'<rect x="{F(64,170)[0]:.1f}" y="{F(64,170)[1]:.1f}" width="{13*K*S4:.1f}" '
         f'height="{50*K*S4:.1f}" rx="{4*K*S4:.1f}" fill="#cbb894" stroke="#6b5a3e" '
         f'stroke-width="2"/>\n')

# screws
for sx_, sy_ in [(9, 228), (46, 150), (30, 46), (52, 96)]:
    qx, qy = F(sx_, sy_)
    s.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="7" fill="#ffffff" '
             f'stroke="#3d3d3d" stroke-width="1.8"/>\n')
    s.append(f'<path d="M {qx-4.4:.1f} {qy:.1f} L {qx+4.4:.1f} {qy:.1f} '
             f'M {qx:.1f} {qy-4.4:.1f} L {qx:.1f} {qy+4.4:.1f}" stroke="#3d3d3d" '
             f'stroke-width="1.5"/>\n')

# callouts
CALL = [
    (1, 24, 165, 8, 198, "#3d3d3d"),
    (2, 38, 202, 70, 224, "#7b2cbf"),
    (3, 6, 152, 30, 142, "#6b5a3e"),
    (4, 8, 105, 30, 96, "#6b5a3e"),
    (5, 66, 150, 88, 190, "#6b5a3e"),
]
for num, ax_, ay_, lx_, ly_, col in CALL:
    ax, ay = F(ax_, ay_)
    lx, ly = F(lx_, ly_)
    s.append(f'<path d="M {ax:.1f} {ay:.1f} L {lx:.1f} {ly:.1f}" stroke="{col}" '
             f'stroke-width="1.3" opacity="0.7"/>\n')
    s.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="11" fill="{col}"/>\n')
    s.append(text(lx, ly + 5, str(num), 12.5, "#ffffff", anchor="middle", weight="bold"))

# dimensions
DIM = "#2b6cb0"
s.append('<defs><marker id="dA" viewBox="0 0 10 10" refX="9" refY="5" '
         'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{DIM}"/></marker></defs>\n')


def vd(py1, py2, x, label):
    a, b = F(0, py1)[1], F(0, py2)[1]
    mid = (a + b) / 2
    return (f'<path d="M {x} {a:.1f} L {x} {b:.1f}" stroke="{DIM}" stroke-width="1.4" '
            f'marker-start="url(#dA)" marker-end="url(#dA)"/>\n'
            f'<path d="M {x-6} {a:.1f} L {x+6} {a:.1f} M {x-6} {b:.1f} L {x+6} {b:.1f}" '
            f'stroke="{DIM}" stroke-width="1.2"/>\n'
            f'<text x="{x-9}" y="{mid:.1f}" font-size="13" fill="{DIM}" '
            f'text-anchor="middle" transform="rotate(-90 {x-9} {mid:.1f})">{label}</text>\n')


def hd(px1, px2, y, label):
    a, b = F(px1, 0)[0], F(px2, 0)[0]
    return (f'<path d="M {a:.1f} {y} L {b:.1f} {y}" stroke="{DIM}" stroke-width="1.4" '
            f'marker-start="url(#dA)" marker-end="url(#dA)"/>\n'
            f'<path d="M {a:.1f} {y-6} L {a:.1f} {y+6} M {b:.1f} {y-6} L {b:.1f} {y+6}" '
            f'stroke="{DIM}" stroke-width="1.2"/>\n'
            f'<text x="{(a+b)/2:.1f}" y="{y-10}" font-size="13" fill="{DIM}" '
            f'text-anchor="middle">{label}</text>\n')


s.append(vd(250, 18, 44, "334"))
s.append(vd(165, 18, 26, "238 to the eye"))
s.append(hd(0, 80, 858, "115"))
s.append(hd(64, 84, 858, "20"))

# section at eye level
BX, BY, BS = 470, 170, 1.75
s.append(text(BX, BY - 26, "SECTION AT EYE LEVEL", 13, "#5f6b73", weight="bold",
              spacing="1.2"))


def S(x, y):
    return (BX + x * K * BS, BY + y * BS)


s.append(f'<path d="M {BX-20} {BY} L {BX+80*K*BS+20} {BY}" stroke="#5a4a30" '
         f'stroke-width="7" stroke-linecap="square"/>\n')
s.append(text(BX - 16, BY - 10, "wall", 11, "#8a7a5e"))
s.append(f'<rect x="{S(0,0)[0]:.1f}" y="{BY:.1f}" width="{80*K*BS:.1f}" '
         f'height="{18*BS:.1f}" fill="#dccfae" stroke="#5a4a30" stroke-width="1.8"/>\n')
s.append(f'<rect x="{S(0,18)[0]:.1f}" y="{BY+18*BS:.1f}" width="{80*K*BS:.1f}" '
         f'height="{18*BS:.1f}" fill="#e8dcc4" stroke="#5a4a30" stroke-width="1.8"/>\n')
for x0_, x1_, x2_ in [(0, 3, 0), (77, 80, 80)]:
    s.append(f'<path d="M {S(x0_,15)[0]:.1f} {S(x0_,15)[1]:.1f} '
             f'L {S(x1_,18)[0]:.1f} {S(x1_,18)[1]:.1f} L {S(x2_,18)[0]:.1f} '
             f'{S(x2_,18)[1]:.1f} Z" fill="#3d3d3d" opacity="0.75"/>\n')
s.append(f'<rect x="{S(14,36)[0]:.1f}" y="{BY+36*BS:.1f}" width="{30*K*BS:.1f}" '
         f'height="{20*BS:.1f}" rx="3" fill="#f8f5ec" stroke="#3d3d3d" stroke-width="1.8"/>\n')
s.append(f'<rect x="{S(14,56)[0]:.1f}" y="{BY+56*BS:.1f}" width="{30*K*BS:.1f}" '
         f'height="{6*BS:.1f}" fill="#a89372" stroke="#5a4a30" stroke-width="1.4"/>\n')
s.append(f'<path d="M {S(0,36)[0]:.1f} {S(0,36)[1]:.1f} L {S(-28,36)[0]:.1f} '
         f'{S(-28,36)[1]:.1f} L {S(-28,62)[0]:.1f} {S(-28,62)[1]:.1f} L '
         f'{S(0,62)[0]:.1f} {S(0,62)[1]:.1f} Z" fill="#cbb894" stroke="#6b5a3e" '
         f'stroke-width="1.6"/>\n')
s.append(text(*S(-14, 70), "half nose", 10.5, "#6b5a3e", anchor="middle"))
s.append(f'<rect x="{S(74,36)[0]:.1f}" y="{BY+36*BS:.1f}" width="{18*BS:.1f}" '
         f'height="{24*BS:.1f}" fill="#cbb894" stroke="#6b5a3e" stroke-width="1.5"/>\n')
s.append(text(*S(96, 70), "ear, perpendicular to the face", 10.5, "#6b5a3e",
              anchor="middle"))
s.append(text(*S(-4, 92), "3 mm bevel at the joint: the shadow line", 10.5, "#3d3d3d",
              anchor="middle"))

dy = BY + 62 * BS + 26
s.append(f'<path d="M {S(0,0)[0]:.1f} {dy} L {S(0,62)[0]:.1f} {dy}" stroke="{DIM}" '
         f'stroke-width="1.4" marker-start="url(#dA)" marker-end="url(#dA)"/>\n')
s.append(text(BX + 20, dy + 18, "62 from the wall to the eyelid &#183; the depth does "
              "not scale", 11.5, DIM, weight="bold"))

# ear, seen from the flight
EX6, EY6, ESC = 918, 350, 2.1
s.append(text(EX6, EY6 - 150, "EAR, SEEN FROM THE FLIGHT", 13, "#5f6b73",
              weight="bold", spacing="1.2"))
s.append(text(EX6, EY6 - 132, "one silhouette, 18 mm plywood", 11, "#8a8a8a"))


def E(px, py):
    return (EX6 + px * ESC, EY6 - py * ESC)


EARP = [
    ("M", 0, 14),
    ("C", 0, 26, 6, 40, 12, 46),
    ("C", 17, 51, 24, 52, 28, 46),
    ("C", 26, 42, 22, 38, 20, 33),
    ("C", 18, 27, 20, 21, 24, 16),
    ("C", 26, 12, 25, 8, 21, 6),
    ("C", 16, 3, 8, 4, 4, 8),
    ("C", 2, 10, 1, 12, 0, 14),
]
parts = []
for seg in EARP:
    cmd, c = seg[0], seg[1:]
    pts = " ".join(f"{E(c[i], c[i+1])[0]:.1f} {E(c[i], c[i+1])[1]:.1f}"
                   for i in range(0, len(c), 2))
    parts.append(f"{cmd} {pts}")
s.append(f'<path d="{parts[0]} {" ".join(parts[1:])}" fill="#cbb894" '
         f'stroke="#6b5a3e" stroke-width="2.2"/>\n')
for cx_, cy_ in [(12, 22), (12, 34)]:
    ccx, ccy = E(cx_, cy_)
    s.append(f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="{7*ESC:.1f}" fill="#cfc9ba" '
             f'stroke="#3d3d3d" stroke-width="1.5"/>\n')
s.append(text(E(14, 58), "HC-SR04 behind it", 10.5, "#3d3d3d"))
s.append(text(E(11, 1), "two transducers in the concha", 10.5, "#8a7a5e",
              anchor="middle"))
s.append(text(E(11, -7), "looking down the flight", 10.5, "#8a7a5e", anchor="middle"))

# legend
NX, NY = 470, 430
s.append(text(NX, NY, "WHAT IS WHERE", 13, "#5f6b73", weight="bold", spacing="1.2"))
LEG = [
    (1, "#3d3d3d", "Eye: ball &#216;35 in a &#216;46 ring. The lid is a carved "
     "wooden shell, closed like the mask's eyelids; open it stands up as a visor."),
    (2, "#7b2cbf", "PIR &#216;32 in the forehead, dome proud of the surface."),
    (3, "#6b5a3e", "Half nose: a wedge screwed on the cut edge. In front view it "
     "is a narrow ridge; the section shows how far it comes out."),
    (4, "#6b5a3e", "Pseudo mouth: a shallow recess cut in the front panel, not "
     "two lips. The shadow of the slot does the work, and a shadow costs nothing."),
    (5, "#6b5a3e", "Ear: one silhouette cut in 18 mm plywood and screwed on the "
     "edge. The concha is a shallow recess and the HC-SR04 sits in it, looking "
     "sideways down the flight. Position, not concealment."),
]
y = NY + 30
for num, col, n in LEG:
    s.append(f'<circle cx="{NX+9}" cy="{y-4}" r="10" fill="{col}"/>')
    s.append(text(NX + 9, y + 0.5, str(num), 11.5, "#ffffff", anchor="middle",
                  weight="bold"))
    words, line, lines = n.split(" "), "", []
    for w in words:
        probe = (line + " " + w).strip()
        if len(probe) > 58:
            lines.append(line)
            line = w
        else:
            line = probe
    lines.append(line)
    for i, ln in enumerate(lines):
        s.append(text(NX + 30, y + i * 17, ln, 12, "#4a4a4a"))
    y += 17 * len(lines) + 13

s.append(text(50, 884, "Eye centre 1500 mm above the tread of its step. From the "
              "wall the piece comes out 62 mm at the eye and 110 mm at the nose: the "
              "head is flattened, only the ball is spherical.", 12, "#8a8a8a"))

s.append("</svg>\n")
open(f"{OUT}/structure.svg", "w").write("".join(s))
print("wrote structure.svg")


# ======================================================================
# 5. cutting template, 1:1 in millimetres (A2)
# ======================================================================
W6, H6 = 594, 420
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W6}mm" height="{H6}mm" '
     f'viewBox="0 0 {W6} {H6}" font-family="' + FONT + '">\n']
s.append(f'<rect width="{W6}" height="{H6}" fill="#ffffff"/>\n')
s.append(text(16, 14, "ANDROID EYE &#183; PANEL TEMPLATE, 1:1", 8, "#161616",
              weight="bold", spacing="0.4"))
s.append(text(16, 20.5, "half face, 334 mm tall &#183; print at 100 % on A2 and "
              "check the 100 mm bar before cutting", 4.4, "#5f6b73"))
s.append('<path d="M 16 23 L 578 23" stroke="#c9c3b6" stroke-width="0.4"/>\n')

TK = 1.44
TX_, TY_ = 40, 395


def G(px, py):
    return (TX_ + px * TK, TY_ - py * TK)


segs = []
for seg in OUTLINE:
    cmd, c = seg[0], seg[1:]
    pts = " ".join(f"{G(c[i], c[i+1])[0]:.2f} {G(c[i], c[i+1])[1]:.2f}"
                   for i in range(0, len(c), 2))
    segs.append(f"{cmd} {pts}")
tmpl_d = segs[0] + " " + " ".join(segs[1:]) + " Z"
s.append(f'<path d="{tmpl_d}" fill="#fbf8f0" stroke="#161616" stroke-width="0.9"/>\n')

# holes
def hole(px, py, d, label, lx, ly):
    cx, cy = G(px, py)
    s.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{d/2*TK:.2f}" fill="#ffffff" '
             f'stroke="#161616" stroke-width="0.7"/>\n')
    s.append(f'<path d="M {cx-1:.2f} {cy:.2f} L {cx+1:.2f} {cy:.2f} '
             f'M {cx:.2f} {cy-1:.2f} L {cx:.2f} {cy+1:.2f}" stroke="#161616" '
             f'stroke-width="0.4"/>\n')
    gx, gy = G(lx, ly)
    s.append(f'<path d="M {cx:.2f} {cy:.2f} L {gx:.2f} {gy:.2f}" stroke="#8a8a8a" '
             f'stroke-width="0.3" stroke-dasharray="2 1.5"/>\n')
    s.append(text(gx, gy - 1.5, label, 4.2, "#161616"))


hole(24, 165, 46, "&#216;46 eye socket", 34, 170)
hole(42, 205, 32, "&#216;32 PIR", 64, 212)

# ear position, outside the outline
ex_, ey_ = G(64, 150)
s.append(f'<circle cx="{ex_:.2f}" cy="{ey_:.2f}" r="{8*TK:.2f}" fill="none" '
         f'stroke="#8a8a8a" stroke-width="0.4" stroke-dasharray="3 2"/>\n')
gsx, gsy = G(64, 196)
s.append(f'<path d="M {ex_:.2f} {ey_:.2f} L {gsx:.2f} {gsy:.2f}" stroke="#8a8a8a" '
         f'stroke-width="0.3" stroke-dasharray="2 1.5"/>\n')
s.append(text(gsx - 2, gsy - 1.5, "ear, disc stack screwed on the edge", 4.2, "#161616"))

# relief pieces, as outlines
REL = [(0, 130, 13, 175, "half nose"), (0, 96, 17, 114, "lips"),
       (0, 20, 19, 40, "chin"), (0, 170, 42, 190, "brow")]
for x0, y0, x1, y1, lab in REL:
    a = G(x0, y1)
    s.append(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{(x1-x0)*TK:.2f}" '
             f'height="{(y1-y0)*TK:.2f}" fill="none" stroke="#2b6cb0" '
             f'stroke-width="0.35" stroke-dasharray="2.5 1.5"/>\n')

# screws
for sx_, sy_ in [(9, 228), (46, 150), (30, 46), (52, 96)]:
    qx, qy = G(sx_, sy_)
    s.append(f'<circle cx="{qx:.2f}" cy="{qy:.2f}" r="{3*TK:.2f}" fill="#fbf8f0" '
             f'stroke="#161616" stroke-width="0.5"/>\n')
    s.append(f'<path d="M {qx-2:.2f} {qy:.2f} L {qx+2:.2f} {qy:.2f} '
             f'M {qx:.2f} {qy-2:.2f} L {qx:.2f} {qy+2:.2f}" stroke="#161616" '
             f'stroke-width="0.35"/>\n')

# dimensions
s.append(f'<path d="M {G(0,0)[0]-7:.2f} {G(0,0)[1]:.2f} L {G(0,0)[0]-7:.2f} '
         f'{G(0,250)[1]:.2f}" stroke="#2b6cb0" stroke-width="0.35"/>\n')
s.append(text(G(0, 0)[0] - 9, G(0, 125)[1], "360", 4.6, "#2b6cb0", anchor="middle",
              weight="bold"))
s.append(f'<path d="M {G(0,0)[0]:.2f} {G(0,0)[1]+8:.2f} L {G(80,0)[0]:.2f} '
         f'{G(0,0)[1]+8:.2f}" stroke="#2b6cb0" stroke-width="0.35"/>\n')
s.append(text(G(40, 0)[0], G(0, 0)[1] + 6, "115", 4.6, "#2b6cb0", anchor="middle",
              weight="bold"))

# scale bar
s.append(f'<path d="M 400 404 L 500 404" stroke="#161616" stroke-width="0.6"/>\n')
for i in range(11):
    s.append(f'<path d="M {400+i*10} 404 L {400+i*10} {401 if i % 5 else 399}" '
             f'stroke="#161616" stroke-width="0.4"/>\n')
s.append(text(400, 410, "100 mm: if the print does not measure this, it is scaled "
              "and cannot be used", 3.8, "#8a8a8a"))

# notes
NOTES6 = [
    "Cut two of these in 18 mm plywood, glue them face to face and cut once. "
    "Before gluing, bevel 3 mm at 45&#176; along the front edge of the back panel: "
    "it leaves a shadow line under the front panel, all round.",
    "Both panels: this same outline. Glue them first, cut once, so the two "
    "silhouettes cannot drift apart.",
    "Blue dashed: the relief pieces, drawn at their positions. They are screwed on "
    "the front face, from the front, screws visible.",
    "The &#216;46 socket must be drilled before the front panel is mounted: the "
    "ring covers the joint.",
]
y6 = 250
for n in NOTES6:
    words, line, lines = n.split(" "), "", []
    for w in words:
        probe = (line + " " + w).strip()
        if len(probe) > 46:
            lines.append(line)
            line = w
        else:
            line = probe
    lines.append(line)
    for i, ln in enumerate(lines):
        s.append(text(320, y6 + i * 5.2, ln, 4.2, "#4a4a4a"))
    y6 += 5.2 * len(lines) + 4

s.append("</svg>\n")
open(f"{OUT}/template.svg", "w").write("".join(s))
print("wrote template.svg")


# ======================================================================
# 7. eye module, 2:1
# ======================================================================
W7, H7 = 1240, 860
s = [HEAD.format(w=W7, h=H7)]
s.append(f'<rect width="{W7}" height="{H7}" fill="#fbfaf7"/>\n')
s.append(text(50, 56, "ANDROID EYE &#183; THE EYE MODULE", 26, "#161616",
              weight="bold", spacing="0.3"))
s.append(text(50, 82, "ball &#216;35 in a &#216;46 ring &#183; carved wooden lid, "
              "hinged in the wall plane &#183; drawn at 2:1, figures in millimetres",
              13.5, "#5f6b73"))
s.append('<path d="M 50 98 L 1190 98" stroke="#d9d4c8" stroke-width="2"/>\n')

SC7 = 3.4
EX, EY = 290, 470


def Q(px, py):
    return (EX + px * SC7, EY - py * SC7)


s.append(text(EX - 100, EY - 225, "FRONT VIEW", 13, "#5f6b73", weight="bold",
              spacing="1.2"))
# ring
s.append(f'<circle cx="{EX}" cy="{EY}" r="{23*SC7:.1f}" fill="#e6d8bc" '
         f'stroke="#5a4a30" stroke-width="2.6"/>\n')
s.append(f'<circle cx="{EX}" cy="{EY}" r="{20*SC7:.1f}" fill="#3d3d3d" opacity="0.25"/>\n')
# ball, seen through the ring
s.append(f'<circle cx="{EX}" cy="{EY}" r="{17.5*SC7:.1f}" fill="#efeade" '
         f'stroke="#3d3d3d" stroke-width="1.8"/>\n')
# closed lid: carved shell with an eyelid crease
s.append(f'<path d="M {EX-17.5*SC7:.1f} {EY+1:.1f} A {17.5*SC7:.1f} {17.5*SC7:.1f} 0 0 1 '
         f'{EX+17.5*SC7:.1f} {EY+1:.1f} Z" fill="#a89372" stroke="#5a4a30" '
         f'stroke-width="2.2"/>\n')
s.append(f'<path d="M {EX-15*SC7:.1f} {EY:.1f} Q {EX} {EY+6*SC7:.1f} '
         f'{EX+15*SC7:.1f} {EY:.1f}" fill="none" stroke="#5a4a30" stroke-width="1.8"/>\n')
s.append(f'<path d="M {EX-13*SC7:.1f} {EY+7*SC7:.1f} Q {EX} {EY+10*SC7:.1f} '
         f'{EX+13*SC7:.1f} {EY+7*SC7:.1f}" fill="none" stroke="#8a7a5e" '
         f'stroke-width="1.2"/>\n')
# lid open, dashed, standing above
s.append(f'<path d="M {EX-17.5*SC7:.1f} {EY-3:.1f} L {EX-20*SC7:.1f} {EY-24*SC7:.1f} '
         f'A {20*SC7:.1f} {20*SC7:.1f} 0 0 1 {EX+20*SC7:.1f} {EY-24*SC7:.1f} '
         f'L {EX+17.5*SC7:.1f} {EY-3:.1f}" fill="none" stroke="#2d6a4f" '
         f'stroke-width="2" stroke-dasharray="8 5"/>\n')
# axle
s.append(f'<circle cx="{EX}" cy="{EY}" r="5" fill="#ffffff" stroke="#3d3d3d" stroke-width="2"/>\n')
s.append(f'<path d="M {EX-23*SC7-40:.1f} {EY} L {EX-23*SC7:.1f} {EY} '
         f'M {EX+23*SC7:.1f} {EY} L {EX+23*SC7+40:.1f} {EY}" stroke="#3d3d3d" '
         f'stroke-width="3"/>\n')
s.append(text(EX + 23 * SC7 + 46, EY + 4, "axle, in the wall plane", 11, "#3d3d3d"))

# servo above
s.append(f'<rect x="{EX-14:.1f}" y="{EY-23*SC7-96:.1f}" width="{70:.1f}" height="{58:.1f}" '
         f'rx="4" fill="#5c6b73" stroke="#2f3a40" stroke-width="2"/>\n')
s.append(text(EX + 21, EY - 23 * SC7 - 60, "SG90", 11.5, "#e8eef1", anchor="middle",
              weight="bold"))
s.append(f'<path d="M {EX-14:.1f} {EY-23*SC7-66:.1f} L {EX-56:.1f} {EY-150:.1f}" '
         f'stroke="#e0a800" stroke-width="5" stroke-linecap="round"/>\n')
s.append(f'<circle cx="{EX-56:.1f}" cy="{EY-150:.1f}" r="6" fill="#e0a800" '
         f'stroke="#a07a00" stroke-width="1.5"/>\n')
s.append(text(EX - 68, EY - 146, "horn and pushrod to the lid", 11, "#8a6d1a",
              anchor="end"))

# stop pin
s.append(f'<circle cx="{EX+34:.1f}" cy="{EY-86:.1f}" r="5" fill="#3d3d3d"/>\n')
s.append(text(EX + 44, EY - 82, "stop at 96&#176;", 11, "#3d3d3d"))

# ---------------- section
BX7, BY7 = 700, 210
s.append(text(BX7, BY7 - 62, "SECTION, FROM THE SIDE", 13, "#5f6b73", weight="bold",
              spacing="1.2"))
SC8 = 2.6


def R(px, py):
    return (BX7 + px * SC8, BY7 + py * SC8)


# wall and the two panels
s.append(f'<path d="M {BX7-24} {BY7} L {BX7-24} {BY7+62*SC8}" stroke="#5a4a30" '
         f'stroke-width="7" stroke-linecap="square"/>\n')
s.append(text(BX7 - 30, BY7 - 6, "wall", 11, "#8a7a5e", anchor="end"))
s.append(f'<rect x="{R(0,0)[0]:.1f}" y="{BY7:.1f}" width="{18*SC8:.1f}" '
         f'height="{62*SC8:.1f}" fill="#dccfae" stroke="#5a4a30" stroke-width="1.8"/>\n')
s.append(f'<rect x="{R(18,0)[0]:.1f}" y="{BY7:.1f}" width="{18*SC8:.1f}" '
         f'height="{62*SC8:.1f}" fill="#e8dcc4" stroke="#5a4a30" stroke-width="1.8"/>\n')
# ring recess in the front panel
s.append(f'<rect x="{R(26,0)[0]:.1f}" y="{BY7+8*SC8:.1f}" width="{10*SC8:.1f}" '
         f'height="{46*SC8:.1f}" fill="#e6d8bc" stroke="#5a4a30" stroke-width="1.6"/>\n')
# ball
s.append(f'<circle cx="{R(31,31)[0]:.1f}" cy="{R(31,31)[1]:.1f}" r="{17.5*SC8:.1f}" '
         f'fill="#efeade" stroke="#3d3d3d" stroke-width="2"/>\n')
# lid standing above
s.append(f'<path d="M {R(36,14)[0]:.1f} {R(36,14)[1]:.1f} L {R(36,-6)[0]:.1f} '
         f'{R(36,-6)[1]:.1f}" stroke="#a89372" stroke-width="{6*SC8:.1f}" '
         f'stroke-linecap="round"/>\n')
# servo behind the panels
s.append(f'<rect x="{R(4,52)[0]:.1f}" y="{BY7+2*SC8:.1f}" width="{14*SC8:.1f}" '
         f'height="{20*SC8:.1f}" fill="#5c6b73" stroke="#2f3a40" stroke-width="1.6"/>\n')


# dimensions
s.append(text(BX7, BY7 + 62 * SC8 + 26, "36 mm of panels, 62 mm to the eyelid",
              11.5, "#2b6cb0", weight="bold"))

# ---------------- legend
NX7, NY7 = 700, 450
s.append(text(NX7, NY7, "HOW IT GOES TOGETHER", 13, "#5f6b73", weight="bold",
              spacing="1.2"))
LEG7 = [
    "The ring is screwed into a &#216;46 recess in the front panel, 12 mm deep, "
    "so the ball sits half in and half out.",
    "The axle passes through the ball centre, horizontal and parallel to the "
    "wall: the lid sweeps up in front of the face, exactly like an eyelid.",
    "The closed lid is a carved shell, not a disc: the crease and the lower line "
    "quote the mask's closed eyelids, which is what ties the triptych together.",
    "At 96&#176; the lid rests on a small pin and stops. Repeatable, no servo "
    "strain, no calibration.",
    "The SG90 sits behind the front panel with its horn through a slot; the "
    "pushrod is visible in the gap. Nothing hidden.",
    "The LED goes in the ball from behind, two wires through a 3 mm hole, which "
    "is also the way to re-glue the pupil if it comes loose.",
]
y = NY7 + 30
for n in LEG7:
    s.append(text(NX7, y, "&#8226;", 13, "#5f6b73"))
    words, line, lines = n.split(" "), "", []
    for w in words:
        probe = (line + " " + w).strip()
        if len(probe) > 58:
            lines.append(line)
            line = w
        else:
            line = probe
    lines.append(line)
    for i, ln in enumerate(lines):
        s.append(text(NX7 + 16, y + i * 17, ln, 12, "#4a4a4a"))
    y += 17 * len(lines) + 12

s.append("</svg>\n")
open(f"{OUT}/eye-module.svg", "w").write("".join(s))
print("wrote eye-module.svg")


# ======================================================================
# 8. soft latch: how the battery pack wakes and sleeps the board
# ======================================================================
W8, H8 = 1240, 1080
s = [HEAD.format(w=W8, h=H8)]
s.append(f'<rect width="{W8}" height="{H8}" fill="#fbfaf7"/>\n')
s.append(text(50, 56, "ANDROID EYE &#183; SOFT LATCH", 26, "#161616",
              weight="bold", spacing="0.3"))
s.append(text(50, 82, "the PIR is always awake and wakes the board; D4 keeps it "
              "alive until the face is quiet again", 13.5, "#5f6b73"))
s.append('<path d="M 50 98 L 1180 98" stroke="#d9d4c8" stroke-width="2"/>\n')

RED, BLK, BLU = "#d62828", "#1b1b1b", "#2b6cb0"


def box(x0, y0, x1, y1, title, sub="", fill="#ffffff", stroke="#3d3d3d",
        dashed=False, titlesize=12.5):
    g = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="6" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="2"'
         + (' stroke-dasharray="7 5"' if dashed else '') + '/>\n']
    g.append(text((x0 + x1) / 2, y0 + 20, title, titlesize, "#161616",
                  anchor="middle", weight="bold"))
    if sub:
        g.append(text((x0 + x1) / 2, y0 + 36, sub, 11, "#6b6b6b", anchor="middle"))
    return "".join(g)


def dot8(x, y, color):
    return (f'<circle cx="{x}" cy="{y}" r="6.5" fill="#ffffff"/>'
            f'<circle cx="{x}" cy="{y}" r="4.4" fill="{color}"/>\n')


# rails
s.append(wire([(95, 148), (1150, 148)], RED))
s.append(text(100, 138, "PACK +", 11.5, RED, weight="bold"))
s.append(wire([(95, 800), (1150, 800)], BLK))
s.append(text(100, 818, "GND", 11.5, BLK, weight="bold"))
s.append(wire([(95, 148), (95, 800)], BLK, width=2.6))   # pack return

# battery pack
s.append(f'<rect x="70" y="300" width="50" height="330" rx="6" fill="#fff8e8" '
         f'stroke="#8a6d1a" stroke-width="2"/>\n')
s.append(f'<text x="95" y="480" font-size="11.5" fill="#8a6d1a" text-anchor="middle" '
         f'transform="rotate(-90 95 480)">4&#215;AA NiMH, 4.8 V</text>\n')

# Q1 and Q2
s.append(box(330, 196, 430, 254, "Q1", "P-MOSFET", fill="#eef4ff", stroke=BLU))
s.append(box(330, 452, 430, 510, "Q2", "NPN", fill="#eef4ff", stroke=BLU))
s.append(text(440, 214, "IRF9540", 10.5, "#6b6b6b"))
s.append(text(440, 470, "2N2222", 10.5, "#6b6b6b"))

# switched rail
s.append(wire([(430, 225), (1150, 225)], RED))
s.append(text(1050, 216, "+5 V switched", 11.5, RED, weight="bold"))
s.append(wire([(380, 254), (380, 452)], BLU))
s.append(wire([(360, 254), (360, 196)], BLU, width=2.4))
s.append(f'<rect x="352" y="150" width="16" height="46" fill="#ffffff" stroke="#2b6cb0" '
         f'stroke-width="1.8"/>\n')
s.append(text(352, 142, "R1 100k", 10.5, BLU, anchor="middle"))
s.append(dot8(360, 148, RED))

# pull-down to Q2's collector, and the base network
s.append(text(388, 300, "gate", 10.5, BLU))
s.append(wire([(430, 481), (505, 481)], BLU))
s.append(f'<rect x="505" y="474" width="46" height="14" fill="#ffffff" stroke="#2b6cb0" '
         f'stroke-width="1.8"/>\n')
s.append(text(528, 466, "R2 10k", 10.5, BLU, anchor="middle"))
s.append(wire([(551, 481), (640, 481)], BLU))
s.append(text(600, 472, "D4", 11, BLU, weight="bold"))

# PIR, always on, waking through R3
s.append(box(120, 560, 300, 700, "HC-SR501", "always powered", fill="#f7f1ff",
             stroke="#7b2cbf"))
s.append(wire([(95, 610), (120, 610)], RED))
s.append(wire([(95, 660), (120, 660)], BLK))
s.append(wire([(300, 630), (400, 630)], "#7b2cbf"))
s.append(f'<rect x="400" y="623" width="46" height="14" fill="#ffffff" stroke="#7b2cbf" '
         f'stroke-width="1.8"/>\n')
s.append(text(423, 615, "R3 10k", 10.5, "#7b2cbf", anchor="middle"))
s.append(wire([(446, 630), (480, 630), (480, 481)], "#7b2cbf"))
s.append(dot8(480, 481, BLU))
s.append(text(310, 646, "OUT", 11, "#7b2cbf"))
# the same signal also feeds D2: that is how the sketch reads the PIR
s.append(wire([(480, 630), (600, 630), (600, 380), (640, 380)], "#7b2cbf"))
s.append(dot8(480, 630, "#7b2cbf"))
s.append(text(556, 372, "D2", 11, "#7b2cbf", weight="bold"))

# board
s.append(box(640, 330, 880, 700, "ARDUINO NANO", "same sketch, same pins",
             fill="#f4f8f4", stroke="#2d6a4f"))
s.append(wire([(760, 225), (760, 330)], RED))
s.append(text(766, 300, "5V", 11, RED, weight="bold"))
s.append(wire([(820, 700), (820, 800)], BLK))
s.append(text(826, 740, "GND", 11, BLK, weight="bold"))
PIN_Y = {"D2": 380, "D4": 410, "D6": 450, "D7": 490, "D8": 520, "D9": 560}
for name, y in PIN_Y.items():
    s.append(text(650, y + 4, name, 11, "#3d3d3d", weight="bold"))

# servo, led, sonar on the switched rail
s.append(wire([(1150, 225), (1180, 225)], RED))
s.append(wire([(1180, 225), (1180, 655)], RED))

s.append(box(950, 300, 1140, 390, "SG90", sub="moves with the lid"))
s.append(wire([(1180, 345), (1140, 345)], RED))
s.append(wire([(950, 345), (905, 345)], BLK))
s.append(wire([(905, 345), (905, 800)], BLK))
s.append(wire([(880, 560), (925, 560), (925, 375), (950, 375)], "#e07a1f"))
s.append(text(930, 565, "D9", 11, "#e07a1f", weight="bold"))

s.append(box(950, 430, 1140, 510, "LED pupil", sub="through 220 &#937;"))
s.append(wire([(1180, 470), (1140, 470)], RED))
s.append(wire([(950, 490), (905, 490)], BLK))
s.append(wire([(905, 490), (905, 800)], BLK))
s.append(wire([(880, 450), (928, 450), (928, 445), (950, 445)], "#c9a227"))
s.append(text(933, 440, "D6", 11, "#8a6d1a", weight="bold"))

s.append(box(950, 560, 1140, 660, "HC-SR04", sub="aims down the flight"))
s.append(wire([(1180, 610), (1140, 610)], RED))
s.append(wire([(950, 640), (905, 640)], BLK))
s.append(wire([(880, 490), (930, 490), (930, 585), (950, 585)], WIRE["trig"]))
s.append(text(934, 583, "D7", 11, WIRE["trig"], weight="bold"))
s.append(wire([(880, 520), (938, 520), (938, 620), (950, 620)], WIRE["echo"]))
s.append(text(942, 618, "D8", 11, WIRE["echo"], weight="bold"))

# notes
NOTES8 = [
    "Off state: only the PIR draws, about 60 &#181;A. That is what makes a battery pack last years.",
    "Boot: PIR OUT goes high, R3 pulls Q2's base, Q2 pulls the gate low, Q1 conducts, the board starts.",
    "Run: the sketch sets D4 high in setup(), which holds Q2 on through R2. The PIR can now go quiet.",
    "Sleep: when the state machine reaches SLEEPING and T_SHUTDOWN passes, D4 goes low and everything dies but the PIR.",
    "R1 keeps the gate at the pack voltage when nothing pulls it down: without it the FET may half-conduct.",
    "The pack feeds the 5 V pin directly, so keep it at 4.8-5.2 V. With 6&#215;AA (9 V) feed VIN instead.",
]
for col in range(2):
    y = 880
    for n in NOTES8[col * 3:(col + 1) * 3]:
        words, line, lines = n.split(" "), "", []
        for w in words:
            probe = (line + " " + w).strip()
            if len(probe) > 52:
                lines.append(line)
                line = w
            else:
                line = probe
        lines.append(line)
        x0 = 70 + col * 600
        s.append(text(x0, y, "&#8226;", 12, "#5f6b73"))
        for i, ln in enumerate(lines):
            s.append(text(x0 + 16, y + i * 15, ln, 11.5, "#4a4a4a"))
        y += 15 * len(lines) + 12

s.append(text(60, 1050, "Values are starting points: R1 100 k, R2 and R3 10 k, "
              "Q2 any small NPN, Q1 any P-channel FET that turns on at 4 V of "
              "gate-source.", 11, "#8a8a8a"))

s.append("</svg>\n")
open(f"{OUT}/latch.svg", "w").write("".join(s))
print("wrote latch.svg")


# ======================================================================
# 6. the same template tiled on two A4 sheets
# ======================================================================
A4W, A4H = 210, 297
PAGES = [(175.0, 360.0), (26.0, 185.0)]     # real mm covered, top sheet first
OVERLAP_LO, OVERLAP_HI = 175.0, 185.0

HOLES = [(24, 165, 46, "&#216;46 eye socket"), (42, 205, 32, "&#216;32 PIR")]
REL = [(0, 130, 13, 175), (0, 98, 14, 112), (0, 22, 19, 40), (0, 170, 42, 190)]
SCREWS = [(9, 228), (46, 150), (30, 46), (52, 96)]
EAR_AT = (64, 150)

for page, (y_lo, y_hi) in enumerate(PAGES, start=1):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{A4W}mm" height="{A4H}mm" '
         f'viewBox="0 0 {A4W} {A4H}" font-family="' + FONT + '">\n']
    s.append(f'<rect width="{A4W}" height="{A4H}" fill="#ffffff"/>\n')

    def A(px, py):
        """reference mm -> page mm, 1:1"""
        return (48 + px * K, 22 + (y_hi - py * K))

    def areal(rx, ry):
        return (48 + rx, 22 + (y_hi - ry))

    # everything is clipped to this sheet's band
    band_h = y_hi - y_lo
    s.append(f'<defs><clipPath id="band{page}"><rect x="38" y="20" width="142" '
             f'height="{band_h:.1f}"/></clipPath></defs>\n')
    s.append(f'<g clip-path="url(#band{page})">\n')

    # piece outline
    parts = []
    for seg in OUTLINE:
        cmd, c = seg[0], seg[1:]
        pts = " ".join(f"{A(c[i], c[i+1])[0]:.2f} {A(c[i], c[i+1])[1]:.2f}"
                       for i in range(0, len(c), 2))
        parts.append(f"{cmd} {pts}")
    s.append(f'<path d="{parts[0]} {" ".join(parts[1:])}" fill="#fbf8f0" '
             f'stroke="#161616" stroke-width="0.9"/>\n')

    # holes
    for hx, hy, hd_, label in HOLES:
        cx, cy = A(hx, hy)
        s.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{hd_/2*K:.2f}" fill="#ffffff" '
                 f'stroke="#161616" stroke-width="0.7"/>\n')
        s.append(f'<path d="M {cx-1.2:.2f} {cy:.2f} L {cx+1.2:.2f} {cy:.2f} '
                 f'M {cx:.2f} {cy-1.2:.2f} L {cx:.2f} {cy+1.2:.2f}" stroke="#161616" '
                 f'stroke-width="0.4"/>\n')
        s.append(text(cx + hd_ / 2 * K + 2, cy + 1.2, label, 3.6, "#161616"))

    # relief pieces
    for x0, y0, x1, y1 in REL:
        a = A(x0, y1)
        s.append(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{(x1-x0)*K:.2f}" '
                 f'height="{(y1-y0)*K:.2f}" fill="none" stroke="#2b6cb0" '
                 f'stroke-width="0.3" stroke-dasharray="2 1.4"/>\n')

    # screws
    for sx_, sy_ in SCREWS:
        qx, qy = A(sx_, sy_)
        s.append(f'<circle cx="{qx:.2f}" cy="{qy:.2f}" r="{3*K:.2f}" fill="#fbf8f0" '
                 f'stroke="#161616" stroke-width="0.45"/>\n')
        s.append(f'<path d="M {qx-1.6:.2f} {qy:.2f} L {qx+1.6:.2f} {qy:.2f} '
                 f'M {qx:.2f} {qy-1.6:.2f} L {qx:.2f} {qy+1.6:.2f}" stroke="#161616" '
                 f'stroke-width="0.35"/>\n')

    s.append("</g>\n")

    # the overlap band and its alignment line
    by = areal(0, 180)[1]
    s.append(f'<path d="M 40 {by:.2f} L 175 {by:.2f}" stroke="#c0392b" stroke-width="0.35" '
             f'stroke-dasharray="3 2"/>\n')
    tip = ("the overlap starts here: match it with page 2" if page == 1 else
           "match this line with page 1: 10 mm of overlap")
    s.append(text(48, by - 2 if page == 1 else by + 5, tip, 4, "#c0392b"))

    # registration crosses at the corners of the content area
    for cx_, cy_ in [(43, 10), (168, 10), (43, 287), (168, 287)]:
        s.append(f'<path d="M {cx_-3} {cy_} L {cx_+3} {cy_} M {cx_} {cy_-3} L {cx_} {cy_+3}" '
                 f'stroke="#161616" stroke-width="0.3"/>\n')

    # title
    s.append(text(14, 12, f"ANDROID EYE &#183; PANEL TEMPLATE &#183; SHEET {page} OF 2",
                  5.2, "#161616", weight="bold", spacing="0.2"))
    s.append(text(14, 17.5, "1:1 in millimetres &#183; print at 100 %, no fit to page "
                  "&#183; check the 100 mm bar", 3.8, "#5f6b73"))

    # mini assembly diagram
    TX_, TY_, TS = 156, 52, 0.30
    s.append(text(TX_, TY_ - 4, "ASSEMBLY", 3.6, "#8f8f8f", weight="bold"))
    s.append(f'<rect x="{TX_}" y="{TY_}" width="{115*TS:.1f}" height="{334*TS:.1f}" '
             f'fill="#f4f1ea" stroke="#c9c3b6" stroke-width="0.25"/>\n')
    mini = []
    for seg in OUTLINE:
        cmd, c = seg[0], seg[1:]
        pts = " ".join(f"{TX_ + c[i]*K*TS:.1f} {TY_ + (360 - c[i+1]*K)*TS:.1f}"
                       for i in range(0, len(c), 2))
        mini.append(f"{cmd} {pts}")
    s.append(f'<path d="{mini[0]} {" ".join(mini[1:])}" fill="#e6d8bc" '
             f'stroke="#8a7a5e" stroke-width="0.3"/>\n')
    for lo, hi in PAGES:
        yy = TY_ + (360 - hi) * TS
        s.append(f'<path d="M {TX_} {yy:.1f} L {TX_ + 115*TS:.1f} {yy:.1f}" '
                 f'stroke="#c0392b" stroke-width="0.3" stroke-dasharray="1.2 1"/>\n')
    s.append(f'<rect x="{TX_ + (115*TS)/2 - 1}" y="{TY_}" width="2" height="{334*TS:.1f}" '
             f'fill="none" stroke="#c0392b" stroke-width="0.25" opacity="0"/>\n')

    # scale bar on the first sheet only
    if page == 1:
        s.append(f'<path d="M 14 283 L 114 283" stroke="#161616" stroke-width="0.5"/>\n')
        for i in range(11):
            s.append(f'<path d="M {14+i*10} 283 L {14+i*10} {280.5 if i % 5 else 278.5}" '
                     f'stroke="#161616" stroke-width="0.35"/>\n')
        s.append(text(14, 288, "100 mm: if it does not measure this, the print is "
                      "scaled", 3.6, "#8a8a8a"))

    s.append("</svg>\n")
    open(f"{OUT}/template-a4-p{page}.svg", "w").write("".join(s))
    print(f"wrote template-a4-p{page}.svg")


# ======================================================================
# 7. the small parts, 1:1 on A4
# ======================================================================
W9, H9 = 210, 297
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W9}mm" height="{H9}mm" '
     f'viewBox="0 0 {W9} {H9}" font-family="' + FONT + '">\n']
s.append(f'<rect width="{W9}" height="{H9}" fill="#ffffff"/>\n')
s.append(text(14, 12, "ANDROID EYE &#183; SMALL PARTS, 1:1", 6, "#161616",
              weight="bold", spacing="0.2"))
s.append(text(14, 17.5, "print at 100 %, no fit to page &#183; every outline below "
              "is the real size", 3.8, "#5f6b73"))
s.append('<path d="M 14 20 L 196 20" stroke="#c9c3b6" stroke-width="0.4"/>\n')


def P9(px, py):
    return (px, py)          # pieces are drawn at their real size, 1 unit = 1 mm


def outline(pts, ox, oy, flip=False):
    """draw a piece given its segments, origin top-left, y down already"""
    out = []
    for seg in pts:
        cmd, c = seg[0], seg[1:]
        coords = " ".join(f"{ox + c[i]:.2f} {oy + c[i+1]:.2f}"
                          for i in range(0, len(c), 2))
        out.append(f"{cmd} {coords}")
    return f'<path d="{out[0]} {" ".join(out[1:])}" fill="#e8dcc4" stroke="#5a4a30" stroke-width="0.5"/>\n'


# ---- ear, 30 x 60
EAR = [
    ("M", 4, 0), ("C", 1, 8, 2, 20, 6, 32),
    ("C", 10, 44, 14, 52, 20, 56), ("C", 26, 59, 30, 56, 29, 50),
    ("C", 27, 44, 22, 40, 20, 34), ("C", 18, 27, 21, 20, 26, 15),
    ("C", 29, 11, 29, 5, 24, 2), ("C", 17, -2, 8, -2, 4, 0),
]
s.append(text(16, 30, "EAR", 4.6, "#161616", weight="bold"))
s.append(text(16, 34.5, "18 mm plywood, one piece", 3.4, "#6b6b6b"))
s.append(outline(EAR, 20, 40))
for ty in (59, 77):
    s.append(f'<circle cx="33" cy="{ty}" r="8" fill="#ffffff" stroke="#3d3d3d" '
             f'stroke-width="0.4"/>\n')
s.append(text(20, 106, "30 &#215; 60 &#183; the two &#216;16 holes are the "
              "transducers", 3.4, "#4a4a4a"))
s.append(f'<path d="M 20 110 L 50 110" stroke="#2b6cb0" stroke-width="0.3"/>\n')
s.append(text(35, 113.5, "30", 3.6, "#2b6cb0", anchor="middle"))

# ---- nose, side view and plan
NOSE_S = [("M", 0, 0), ("L", 28, 5), ("L", 28, 19), ("L", 0, 26)]
s.append(text(66, 30, "HALF NOSE", 4.6, "#161616", weight="bold"))
s.append(text(66, 34.5, "18 mm plywood, screwed on the cut edge", 3.4, "#6b6b6b"))
s.append(outline(NOSE_S, 66, 40))
s.append(text(66, 74, "side view: 28 mm out of the face, 26 mm at the base",
              3.4, "#4a4a4a"))
s.append(outline([("M", 0, 0), ("L", 28, 0), ("L", 28, 12), ("L", 0, 12)], 66, 82))
s.append(text(66, 100, "plan: 12 mm wide", 3.4, "#4a4a4a"))

# ---- brow and chin
s.append(text(112, 30, "BROW", 4.6, "#161616", weight="bold"))
s.append(outline([("M", 0, 0), ("L", 60, 7), ("L", 60, 19), ("L", 0, 12)], 112, 40))
s.append(text(112, 68, "60 long, 12 thick, 7 mm of slope", 3.4, "#4a4a4a"))
s.append(text(112, 84, "CHIN", 4.6, "#161616", weight="bold"))
s.append(outline([("M", 0, 0), ("L", 27, 0), ("L", 27, 26), ("L", 0, 26)], 112, 92))
s.append(text(112, 124, "27 &#215; 26 &#215; 18 block", 3.4, "#4a4a4a"))

# ---- what has no template
s.append(text(14, 140, "WHAT HAS NO TEMPLATE, AND WHY", 4.6, "#161616",
              weight="bold", spacing="0.2"))
NOTES9 = [
    "The pseudo mouth is a recess, not a piece: set the router to 4 mm and take out a slot "
    "90 mm long, 14 mm tall, 4 mm deep. The shadow does the rest.",
    "The eyelid cannot be templated flat: it is a shell that follows the 17.5 mm radius. "
    "Either cut it from a 35 mm plastic ball (a table-tennis ball is 40 and can be sanded down), "
    "or press 1.5 mm plywood over a 35 mm ball and let it dry in shape.",
    "The panel outline is on the other sheets: template.svg for a plotter, "
    "template-a4-p1.svg and -p2.svg for a normal printer.",
    "The eye ring is turned or cut from 12 mm plywood, &#216;46 outside, &#216;40 inside: "
    "no template needed, a hole saw does both.",
]
y = 146
for n in NOTES9:
    words, line, lines = n.split(" "), "", []
    for w in words:
        probe = (line + " " + w).strip()
        if len(probe) > 92:
            lines.append(line)
            line = w
        else:
            line = probe
    lines.append(line)
    s.append(text(14, y, "&#8226;", 3.8, "#5f6b73"))
    for i, ln in enumerate(lines):
        s.append(text(18, y + i * 4.4, ln, 3.6, "#4a4a4a"))
    y += 4.4 * len(lines) + 2.6

# ---- scale bar
s.append(f'<path d="M 14 283 L 114 283" stroke="#161616" stroke-width="0.5"/>\n')
for i in range(11):
    s.append(f'<path d="M {14+i*10} 283 L {14+i*10} {280.5 if i % 5 else 278.5}" '
             f'stroke="#161616" stroke-width="0.35"/>\n')
s.append(text(14, 288, "100 mm: if it does not measure this, the print is scaled",
              3.6, "#8a8a8a"))

s.append("</svg>\n")
open(f"{OUT}/parts.svg", "w").write("".join(s))
print("wrote parts.svg")
