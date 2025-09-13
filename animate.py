# animate.py
import sys, time, random, string, os

def _enable_ansi_on_windows():
    """เปิด ANSI escape บน Windows ให้รองรับ ANSI escape codes"""
    if os.name != "nt":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    except Exception:
        pass

def animated_reveal(password: str, cycles_per_char: int = 8, delay: float = 0.02):
    """
    แสดงเอฟเฟ็กต์สุ่มตัวอักษรวิ่งก่อนเฉลย
    - cycles_per_char: จำนวนรอบสุ่มก่อนเฉลยในแต่ละตำแหน่ง
    - delay: เวลาหน่วงต่อเฟรม (วินาที)
    """
    _enable_ansi_on_windows()
    RANDSET = string.ascii_letters + string.digits + string.punctuation
    shown = ["•"] * len(password)   # เริ่มด้วย bullet
    hide_cursor = "\x1b[?25l"
    show_cursor = "\x1b[?25h"
    clear_line  = "\x1b[2K"

    try:
        sys.stdout.write(hide_cursor)
        sys.stdout.flush()
        for i, real_ch in enumerate(password):
            # สุ่มไหลๆ ก่อนเฉลย
            for _ in range(max(1, cycles_per_char)):
                shown[i] = random.choice(RANDSET)
                sys.stdout.write("\r" + clear_line + "Generated Password: " + "".join(shown))
                sys.stdout.flush()
                time.sleep(max(0.0, delay))
            # เฉลยตัวจริง
            shown[i] = real_ch
            sys.stdout.write("\r" + clear_line + "Generated Password: " + "".join(shown))
            sys.stdout.flush()
        sys.stdout.write("\n")
    finally:
        sys.stdout.write(show_cursor)
        sys.stdout.flush()
