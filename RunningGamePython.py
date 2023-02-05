import math

from p5 import *

MAX_STEPRATE = 5
# TRACK_LEN = 200
FRAME_RATE = 60

last_key = "A"
step_rate = 1.0
frames_since_last = 0
current_position = 0
distance_covered = 0
steps = 0
f = None


def setup():
    global f

    size(800, 600)
    f = create_font("Ubuntu-Regular.ttf", 36)


def draw():
    # State updating code
    update_state()

    # Drawing code
    draw_position(current_position)
    draw_text()


def update_state():
    global frames_since_last, distance_covered, steps, step_rate
    frames_since_last += 1

    if steps:
        distance_covered += (step_rate * 8) / FRAME_RATE

    t = target_frame_count()
    tolerance = t / 5
    if frames_since_last - t > tolerance:
        step_rate = max(1, step_rate - 0.05)


def key_released(event):
    global step_rate, frames_since_last

    key = event.key.name

    # Check if wrong key was hit
    if key == last_key:
        # If we hit the same key twice, we stumble and our speed reduces
        step_rate = max(2, step_rate - 1)
        reset_keypress(key)
        return

    # We now know that the user hit the correct key
    # Next we will check how well the user has timed the step

    t = target_frame_count()
    tolerance = t / 5  # Tolerance reduces with speed

    error = frames_since_last - t
    abs_error = abs(error)

    if abs_error <= tolerance:
        step_rate = min(MAX_STEPRATE, step_rate + 0.5)
    else:
        if error < 0:
            i = (5 - step_rate) / 10
            penalty = -(abs_error - tolerance) * 0.05
            step_rate = max(1, step_rate + i + penalty)
        else:
            i = (5 - step_rate) / 10
            penalty = min(i, (abs_error - tolerance) * 0.05)
            step_rate = min(MAX_STEPRATE, step_rate + i - penalty)

    reset_keypress(key)


# Resets all timing variables
def reset_keypress(key: str):
    global frames_since_last, last_key, steps

    # Reset last key pressed
    if key in ("D", "A"):
        last_key = key

    # Reset timing counter
    frames_since_last = 0

    # Update number of steps
    steps += 1


def draw_text():
    text_font(f, 36)
    fill(0)
    no_stroke()

    next_key = "A" if last_key == "D" else "D"

    text("Speed: {:.2f}".format(step_rate), (10, 20))
    text("Next key: " + next_key, (10, 80))
    text("Distance covered: {:.2f}".format(distance_covered), (10, 110))

    fill(255)
    stroke(0)


def draw_position(position: int):
    global step_rate

    background(255)
    stroke(0)
    stroke_weight(2)

    top = 255
    ellipse((400, top + 20), 40, 40)

    hip_pos = Vector(400, top + 115)
    line((400, top + 40), hip_pos)

    t = target_frame_count()
    time_to_left = t - frames_since_last
    time_to_right = time_to_left + t
    if last_key == "A":
        temp = time_to_left
        time_to_left = time_to_right
        time_to_right = temp

    left_horiz = -math.sin((-math.pi * time_to_left) / t) * 40
    right_horiz = -math.sin((-math.pi * time_to_right) / t) * 40
    right_vert = left_vert = abs(math.cos((-math.pi * time_to_left) / t)) * 40
    left_knee = Vector(left_horiz, left_vert) + hip_pos
    right_knee = Vector(right_horiz, right_vert) + hip_pos
    if left_horiz > 0:
        left_foot = left_knee + Vector(0, 30)

        right_shin_horiz = -abs(math.sin((math.pi * frames_since_last) / t) * 30)
        right_shin_vert = abs(math.cos((math.pi * frames_since_last) / t) * 30)
        right_foot = right_knee + Vector(right_shin_horiz, right_shin_vert)
    else:
        right_foot = right_knee + Vector(0, 30)

        left_shin_horiz = -abs(math.sin((math.pi * frames_since_last) / t) * 30)
        left_shin_vert = abs(math.cos((math.pi * frames_since_last) / t) * 30)
        left_foot = left_knee + Vector(left_shin_horiz, left_shin_vert)

    stroke_weight(4)
    stroke(0, 0, 150)
    line(hip_pos, left_knee)
    line(left_knee, left_foot)

    stroke(150, 0, 0)
    line(hip_pos, right_knee)
    line(right_knee, right_foot)


def target_frame_count():
    global step_rate
    return round(FRAME_RATE / step_rate)


run(frame_rate=FRAME_RATE)
