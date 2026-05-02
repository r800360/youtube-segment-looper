import subprocess
import customtkinter as ctk
from tkinter import messagebox


def time_to_seconds(time_str: str) -> int:
    """
    Converts time strings like:
    90
    1:30
    01:02:03
    into total seconds.
    """
    time_str = time_str.strip()

    if not time_str:
        raise ValueError("Time cannot be empty.")

    parts = time_str.split(":")

    if not all(part.isdigit() for part in parts):
        raise ValueError("Time must use numbers only, like 90, 1:30, or 01:02:03.")

    parts = [int(part) for part in parts]

    if len(parts) == 1:
        return parts[0]

    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds

    if len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds

    raise ValueError("Invalid time format. Use seconds, MM:SS, or HH:MM:SS.")


def seconds_to_mpv_time(seconds: int) -> str:
    """
    mpv accepts raw seconds, so this returns a string version.
    """
    return str(seconds)


def launch_loop():
    url = url_entry.get().strip()
    start_raw = start_entry.get().strip()
    end_raw = end_entry.get().strip()
    audio_only = audio_only_var.get()

    if not url:
        messagebox.showerror("Missing URL", "Please paste a YouTube URL.")
        return

    try:
        start_seconds = time_to_seconds(start_raw)
        end_seconds = time_to_seconds(end_raw)
    except ValueError as e:
        messagebox.showerror("Invalid Time", str(e))
        return

    if end_seconds <= start_seconds:
        messagebox.showerror("Invalid Range", "End time must be after start time.")
        return

    command = [
        "mpv",
        url,
        f"--start={seconds_to_mpv_time(start_seconds)}",
        f"--ab-loop-a={seconds_to_mpv_time(start_seconds)}",
        f"--ab-loop-b={seconds_to_mpv_time(end_seconds)}",
        "--force-window=yes",
    ]

    if audio_only:
        command.append("--no-video")

    try:
        subprocess.Popen(command)
        status_label.configure(
            text=f"Looping {start_raw} → {end_raw}",
            text_color="green",
        )
    except FileNotFoundError:
        messagebox.showerror(
            "mpv Not Found",
            "Could not find mpv. Make sure mpv is installed and added to PATH.",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Could not launch mpv:\n{e}")


def stop_all_mpv():
    """
    Windows-friendly way to stop all mpv instances.
    """
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "mpv.exe", "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        status_label.configure(text="Stopped mpv.", text_color="orange")
    except Exception as e:
        messagebox.showerror("Error", f"Could not stop mpv:\n{e}")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("YouTube Segment Looper")
app.geometry("620x430")

title_label = ctk.CTkLabel(
    app,
    text="YouTube Segment Looper",
    font=ctk.CTkFont(size=26, weight="bold"),
)
title_label.pack(pady=(25, 10))

subtitle_label = ctk.CTkLabel(
    app,
    text="Paste a YouTube URL, choose a start and end time, then loop that section.",
    font=ctk.CTkFont(size=14),
)
subtitle_label.pack(pady=(0, 20))

frame = ctk.CTkFrame(app)
frame.pack(padx=30, pady=10, fill="both", expand=True)

url_label = ctk.CTkLabel(frame, text="YouTube URL")
url_label.pack(anchor="w", padx=20, pady=(20, 5))

url_entry = ctk.CTkEntry(
    frame,
    placeholder_text="https://www.youtube.com/watch?v=...",
    width=540,
)
url_entry.pack(padx=20, pady=(0, 15))

time_frame = ctk.CTkFrame(frame, fg_color="transparent")
time_frame.pack(padx=20, pady=5, fill="x")

start_container = ctk.CTkFrame(time_frame, fg_color="transparent")
start_container.pack(side="left", expand=True, fill="x", padx=(0, 10))

start_label = ctk.CTkLabel(start_container, text="Start time")
start_label.pack(anchor="w")

start_entry = ctk.CTkEntry(
    start_container,
    placeholder_text="Example: 1:23",
)
start_entry.pack(fill="x", pady=(5, 0))

end_container = ctk.CTkFrame(time_frame, fg_color="transparent")
end_container.pack(side="left", expand=True, fill="x", padx=(10, 0))

end_label = ctk.CTkLabel(end_container, text="End time")
end_label.pack(anchor="w")

end_entry = ctk.CTkEntry(
    end_container,
    placeholder_text="Example: 2:47",
)
end_entry.pack(fill="x", pady=(5, 0))

audio_only_var = ctk.BooleanVar(value=True)

audio_only_checkbox = ctk.CTkCheckBox(
    frame,
    text="Audio only",
    variable=audio_only_var,
)
audio_only_checkbox.pack(anchor="w", padx=20, pady=(15, 5))

button_frame = ctk.CTkFrame(frame, fg_color="transparent")
button_frame.pack(pady=20)

loop_button = ctk.CTkButton(
    button_frame,
    text="Loop Segment",
    width=180,
    command=launch_loop,
)
loop_button.pack(side="left", padx=10)

stop_button = ctk.CTkButton(
    button_frame,
    text="Stop Playback",
    width=180,
    fg_color="darkred",
    hover_color="#8B0000",
    command=stop_all_mpv,
)
stop_button.pack(side="left", padx=10)

status_label = ctk.CTkLabel(
    frame,
    text="Ready.",
    font=ctk.CTkFont(size=13),
)
status_label.pack(pady=(0, 15))

hint_label = ctk.CTkLabel(
    app,
    text="Time formats supported: 90, 1:30, 01:02:03",
    font=ctk.CTkFont(size=12),
    text_color="gray",
)
hint_label.pack(pady=(0, 15))

app.mainloop()
