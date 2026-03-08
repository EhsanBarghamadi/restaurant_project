import os
import sys
import time


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def type_text(text, speed=0.03, color=""):
    for char in text:
        sys.stdout.write(color + char + "\033[0m")
        sys.stdout.flush()
        time.sleep(speed)
    print()

def progress_bar(label, duration=1.5):
    width = 30
    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = "█" * i + " " * (width - i)
        sys.stdout.write(f"\r\033[1;33m{label}\033[0m [{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / width)
    print()

def show_start():
        clear()

        GOLD = "\033[1;33m"
        DIM = "\033[2m"

        print(GOLD + """
        ╔══════════════════════════════════════╗
        ║                                      ║
        ║        RESTAURANT MANAGER            ║
        ║        Premium Edition               ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """ + "\033[0m")
        
        time.sleep(0.8)

        type_text("Initializing system...", 0.04, DIM)
        progress_bar("Loading modules", 1.2)
        progress_bar("Connecting database", 1.4)
        progress_bar("Preparing interface", 1.1)

        print()
        type_text("System ready ✓", 0.06, GOLD)
        type_text("Don't be like me. (°_ °〃) ✓", 0.15, GOLD)
        time.sleep(1.2)

        clear()