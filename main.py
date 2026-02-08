import random

import psutil

from Count_Min_Sketch import CountMinSketch

# Initialize the Sketch with d = 5 and w = 1000, it will only use 5000 bytes(approx 5KB) of memory
sketch = CountMinSketch(width=1000, depth=5)

TOTAL_EVENTS = 1000000
BOT_USER = "hacker_99"
NORMAL_USERS = [f"user_{i}" for i in range(100)]  # 100 normal users

print(f"---- Starting Simulation of {TOTAL_EVENTS} events ----")

# Simulate the stream
for i in range(TOTAL_EVENTS):
    # the prob. of bot attacking is 10% otherwise it is a normal user
    if random.random() < 0.1:
        user = BOT_USER
    else:
        user = random.choice(NORMAL_USERS)

    # add user to the sketch
    sketch.add(user)

    if i % 1000 == 0:  # for every 1000 events
        bot_estimate = sketch.estimate(BOT_USER)
        random_user = random.choice(NORMAL_USERS)
        normal_estimate = sketch.estimate(random_user)

        print(
            f"Event {i}: Bot count ~ {bot_estimate} | Random User ({random_user}) ~ {
                normal_estimate
            }"
        )

print("\n---- Results ----")
print(f"Actual Bot Count: {int(TOTAL_EVENTS * 0.1)}")
print(f"Sketch Bot Estimate: {sketch.estimate(BOT_USER)}")

process = psutil.Process()
mem_info = process.memory_info().rss / (1024 * 1024)  # in MB
print(f"Actual Process Memory Used: {mem_info:.2f} MB")
print(f"Sketch Matrix size: {(sketch.table.nbytes / 1024):.2f} KB (Pure Data)")
