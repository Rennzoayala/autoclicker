"""
KeepActive.py – system-tray keep-alive tool (portable EXE).
Right-click tray icon to toggle, set interval, or quit.
Sends SCROLLLOCK x2 at the chosen interval to prevent PC/Teams lock.
Single-instance via Windows named mutex.
Interval persisted in config.json next to the EXE.
Requires: pystray, Pillow
"""
import ctypes
import json
import os
import sys
import threading
import pystray
from PIL import Image, ImageDraw

# -- Constants ------------------------------------------------------------------
VK_SCROLL = 0x91
KEYEVENTF_KEYUP = 0x0002
ICON_SIZE = 64
MUTEX_NAME = "Global\\KeepActiveApp"

PRESETS = [
    ("30 seconds", 30),
    ("1 minute", 60),
    ("2 minutes", 120),
    ("5 minutes", 300),
]


# -- Config persistence ---------------------------------------------------------
def _config_path() -> str:
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "config.json")


def load_interval() -> int:
    try:
        with open(_config_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("interval_sec", 60))
    except Exception:
        return 60


def save_interval(sec: int):
    try:
        with open(_config_path(), "w", encoding="utf-8") as f:
            json.dump({"interval_sec": sec}, f, indent=2)
    except Exception:
        pass


# -- Keep-alive signal ----------------------------------------------------------
def send_keep_alive():
    """Tap Scroll Lock twice - net toggle state remains unchanged."""
    for _ in range(2):
        ctypes.windll.user32.keybd_event(VK_SCROLL, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_SCROLL, 0, KEYEVENTF_KEYUP, 0)


# -- Icon drawing ---------------------------------------------------------------
def _make_icon(active: bool) -> Image.Image:
    color = (220, 50, 50, 255) if active else (50, 200, 80, 255)
    img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = 6
    draw.ellipse([pad, pad, ICON_SIZE - pad, ICON_SIZE - pad], fill=color)
    return img


# -- Single instance ------------------------------------------------------------
def _acquire_mutex():
    """Return a mutex handle, or None if another instance is running."""
    handle = ctypes.windll.kernel32.CreateMutexW(None, True, MUTEX_NAME)
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        ctypes.windll.kernel32.CloseHandle(handle)
        return None
    return handle


# -- App ------------------------------------------------------------------------
class KeepActiveApp:
    def __init__(self):
        self._running = False
        self._interval_sec = load_interval()
        self._timer = None
        self._icon = None
        self._build_icon()

    def _build_menu(self):
        interval_items = [
            pystray.MenuItem(
                label,
                self._make_interval_setter(sec),
                checked=lambda item, s=sec: self._interval_sec == s,
                radio=True,
            )
            for label, sec in PRESETS
        ]

        return pystray.Menu(
            pystray.MenuItem(
                self._toggle_label,
                self._toggle,
                default=True,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Interval",
                pystray.Menu(*interval_items),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )

    def _build_icon(self):
        self._icon = pystray.Icon(
            "KeepActive",
            icon=_make_icon(False),
            title=self._tooltip(),
            menu=self._build_menu(),
        )

    # -- Menu helpers -----------------------------------------------------------
    def _toggle_label(self, item):
        return "Turn Off" if self._running else "Turn On"

    def _make_interval_setter(self, sec: int):
        def setter(icon, item):
            self._interval_sec = sec
            save_interval(sec)
            self._refresh_icon()
            if self._running:
                if self._timer:
                    self._timer.cancel()
                self._schedule_next()
        return setter

    # -- Keep-alive logic -------------------------------------------------------
    def _toggle(self, icon, item):
        if self._running:
            self._stop()
        else:
            self._start()

    def _start(self):
        self._running = True
        self._refresh_icon()
        send_keep_alive()
        self._schedule_next()

    def _stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None
        self._refresh_icon()

    def _schedule_next(self):
        if self._running:
            self._timer = threading.Timer(self._interval_sec, self._tick)
            self._timer.daemon = True
            self._timer.start()

    def _tick(self):
        send_keep_alive()
        self._schedule_next()

    # -- UI refresh -------------------------------------------------------------
    def _tooltip(self) -> str:
        label = next(
            (l for l, s in PRESETS if s == self._interval_sec),
            f"{self._interval_sec}s",
        )
        status = "Running" if self._running else "Idle"
        return f"Keep Active - {status} ({label})"

    def _refresh_icon(self):
        if self._icon:
            self._icon.icon = _make_icon(self._running)
            self._icon.title = self._tooltip()
            if hasattr(self._icon, "update_menu"):
                self._icon.update_menu()
            else:
                self._icon.menu = self._build_menu()

    # -- Quit -------------------------------------------------------------------
    def _quit(self, icon, item):
        self._stop()
        icon.stop()

    def run(self):
        self._icon.run()


# -- Entry point ----------------------------------------------------------------
if __name__ == "__main__":
    mutex = _acquire_mutex()
    if mutex is None:
        ctypes.windll.user32.MessageBoxW(
            0,
            "Keep Active is already running.\nCheck your system tray.",
            "Keep Active",
            0x40,  # MB_ICONINFORMATION
        )
        sys.exit(0)

    try:
        KeepActiveApp().run()
    finally:
        ctypes.windll.kernel32.ReleaseMutex(mutex)
        ctypes.windll.kernel32.CloseHandle(mutex)
