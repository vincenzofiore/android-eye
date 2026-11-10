# Bill of materials and final assembly

Two stages are described here: what to buy for the prototype, and how to turn
the prototype into something that hangs on a wall with no breadboard.

Prices are indicative, in euro, for single pieces bought in Europe.

## 0. How to buy this list

The quantities below are the **minimum** for a piece that works. The "spare"
column is what you buy when you are learning and cannot afford a dead part
stopping the project for a week: the servo gears strip, the Nano is a
counterfeit, the MOSFET is a wrong label, the PIR is a dud.

Buying the spare column costs about 30 € more and saves a whole week. It is
the right call for a first build.

| Rule | Why |
|------|-----|
| Buy resistors, capacitors and LEDs in 10-packs | they cost 0.5 € each, and 10 cost 2 € |
| Buy one spare Nano, one spare servo, one spare PIR | these are the parts that fail or arrive dead |
| Buy one spare HC-SR04 | the cheapest to lose, and it is soldered in the ear |
| Buy one spare plywood panel | the saw is the first tool that goes wrong |
| Do not buy a battery charger if you already have one | NiMH is 4.8 V, 4.8 V is not 5 V, but it is close enough |

## 1. Electronics

| Qty | Part | Notes | ~€ |
|-----|------|-------|----|
| 2 | Arduino Nano v3 (CH340) | one works, one is spare. Same sketch, same pins as the Uno | 10–16 |
| 2 | SG90 micro servo | the gears strip; the spare is the difference between a 5-minute fix and a 2-week order | 6–10 |
| 2 | HC-SR501 PIR | one in the forehead, one spare | 4–8 |
| 2 | HC-SR04 ultrasonic | one in the ear, one spare | 4–8 |
| 10 | LED, 5 mm, warm white and amber | 5 warm, 5 amber. The pupil is 1 LED; the rest are for testing | 2 |
| 10 | Resistor 220 Ω, 1/4 W | 10-pack, one is in series with the LED | 1 |
| 10 | Resistor 100 kΩ, 1/4 W | 10-pack, gate pull-up | 1 |
| 20 | Resistor 10 kΩ, 1/4 W | 10-pack, base resistors | 1 |

## 2. Soft latch

| Qty | Part | Notes |
|-----|------|-------|
| 2 | Q1 — P-channel MOSFET | IRF9540 or FQP47P06 in TO-220; IRLML6402 if you want it tiny |
| 2 | Q2 — NPN | 2N2222 or BC547, anything small |
| 2 | 470 µF, 16 V electrolytic | across the servo supply, kills brownouts |
| 10 | 100 nF ceramic | 10-pack, across the pack, optional |
| 2 | momentary pushbutton | manual start, useful on the bench |

## 3. Power

| Qty | Part | Notes | ~€ |
|-----|------|-------|----|
| 2 | Battery holder, 4×AA, with switch | one spare, the plastic clips break | 3 |
| 4 | AA NiMH, 2000 mAh | do not use alkaline: they sag under the servo | 10 |
| 8 | AA NiMH, 2000 mAh, spare | a second set, so the piece is never dark | 20 |
| 1 | NiMH charger | if you do not have one | 15 |
| 10 | 2-pin JST connector | 10-pack, so the pack can be unplugged | 2 |
| 10 | 3-pin JST connector | 10-pack, servo | 2 |
| 10 | 4-pin JST-SM connector | 10-pack, PIR and HC-SR04 | 2 |

## 4. Wood and hardware

| Qty | Part | Notes |
|-----|------|-------|
| 3 | 18 mm plywood, 400 × 300 | the two panels, plus one spare for mistakes |
| 2 | 18 mm plywood, 300 × 200 | ear, nose, brow, chin |
| 2 | 12 mm plywood, 120 × 120 | the eye ring, one spare |
| 2 | 1.5 mm plywood, 120 × 120 | the eyelid shell, or use a 35 mm plastic ball |
| 1 | 35 mm plastic ball | the eyeball |
| 1 | table-tennis ball (40 mm) | the eyelid, sanded down to 35 mm |
| 4 | wall screws 5 × 50 + plugs | the panel weighs about 1.2 kg |
| 25 | screws 3 × 16 | relief pieces, from the front |
| 1 | PVA glue (D3) | panels to each other |
| 1 | matte black paint | inside the eye socket, without it the eye reads as a hole |
| 1 | cable, 6 mm | 2 m of two-core cable, for the pack and the servo |

## 5. Tools worth having

| Tool | Why |
|------|-----|
| 45° chamfer bit, 3 mm | the bevel between the panels |
| Hole saws Ø46, Ø40, Ø32, Ø16 | the eye socket, the ring, the PIR, the ear |
| Router or plough plane, 6 mm | the cable groove |
| Jigsaw | the face outline |
| Soldering iron, solder, heat-shrink, side cutters | the latch |
| Multimeter | the only way to find the short before the board burns |
| Perfboard 5 × 7 cm | the latch, on the bench |
| Female headers, 2.54 mm | the Nano, so it can be swapped |

---

# From the bench to the wall

The breadboard is for finding the values. Once the face works, the circuit has
to become a small rigid object, because nothing on a wall can be held together
by friction.

## The three ways, in order of cost

1. **Perfboard** (millefori), 5 × 7 cm. Cut it to size, solder the latch on it,
   put the Nano on two female headers so it can be swapped. This is enough for
   a prototype and costs a couple of euros.
2. **Custom PCB**, five pieces for about 5 € from any small-batch service. Once
   the layout works, this is what makes the piece serviceable in ten years:
   the same board, the same holes, a silkscreen that says what goes where. Do
   it for the final installation, not before.
3. **Screw-terminal shield** for the Nano: no soldering at all, but bulky and
   it vibrates loose with the servo. Not recommended.

For one piece, perfboard is the right answer. Everything below assumes it.

## What to solder, and what to keep pluggable

- **Soldered permanently:** the latch (Q1, Q2, R1, R2, R3), the 470 µF, the
  220 Ω in series with the LED.
- **On female headers:** the Nano, so a dead board is a one-minute swap.
- **On connectors:** battery (JST), servo (its own 3-pin plug), PIR and
  HC-SR04 (JST-SM 4-pin, or a 4-way screw terminal). Every wire that leaves
  the board ends in a connector, so the piece can be opened without a soldering
  iron on a ladder.

The rule is: **solder what must never move, connect what might need to be
replaced.** With a screwdriver you must be able to change the battery, the
servo and the board, without a soldering iron, on a staircase.

## Order of work

1. Solder the four wires to each module, 20 cm long, then crimp or solder the
   connector at the other end. Heat-shrink every joint: nothing bare inside a
   wooden box.
2. Solder the latch on the perfboard, then test it alone: with no Nano, a
   multimeter on the output rail should show the pack voltage when the button
   is pressed and drop to zero a moment later.
3. Add the Nano on headers, upload the sketch, and repeat the bench test with
   `CON_LATCH 1`.
4. Only then mount everything in the head, and route the wires in the 6 mm
   groove in the back panel.

## The two details that cause trouble later

- **The servo's current does not go through the Nano.** Its two power wires go
  to the switched rail on the perfboard, with the 470 µF next to them. If the
  servo is fed from the board's 5 V pin, the eye stutters and the board resets
  in the middle of an opening.
- **The LED inside the ball** must have a connector in the wire, a few
  centimetres behind the ball. The pupil is the one part that will need to come
  out again, and re-soldering inside a 35 mm ball is not a thing you want to do
  with the piece on the wall.

## Testing before closing

With the multimeter, in this order: no short between the +5 V rail and ground;
the latch switches on with the button and stays on while `D4` is high; the
sketch wakes on the PIR with the button untouched; the eye still runs for a
whole cycle with the pack, not the USB cable, and the voltage on the 5 V rail
never drops below 4.6 V while the servo moves.
