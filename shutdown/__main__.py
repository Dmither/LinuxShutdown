import tkinter as tk
import tkinter.font as tkFont
import os

def main():
    window = tk.Tk()

    window.title("Shutdown timer")
    window.resizable(width=False, height=False)


    # Functions ===============================
    # Get delay -------------------------------
    def get_delay():
        hours = int("0" + ent_hours.get())
        minutes = int("0" + ent_minutes.get())
        seconds = int("0" + ent_seconds.get())
        delay = hours * 3600 + minutes * 60 + seconds
        return delay
    
    def get_full_time(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        full_time = f"{h:02d}h:{m:02d}m:{s:02d}s"
        return full_time

    # Timer -----------------------------------
    global running
    running = False
    global notified
    notified = False

    def countdown(count, func):
        global running
        global notified
        if running:
            if not notified and count < 61:
                notified = True
                os.system(f'notify-send "{func} in {count} seconds"')
            if count > 0:
                full_time = get_full_time(count)
                lbl_message["text"] = f"{func} in {full_time}"
                window.after(1000, countdown, count-1, func)
            else:
                lbl_message["text"] = "Ent = Sleep, Shft+Ent = Off"
                notified = False
                running = False
                match func:
                    case "Sleep": os.system("systemctl suspend")
                    case "Shutdown": os.system("systemctl poweroff")
                
    def start_timer(delay, func):
        if delay <= 0:
            return
        global running
        if running:
            return
        running = True
        countdown(delay, func)
    def stop_timer():
        global running
        running = False
        global notified
        notified = False
        lbl_message["text"] = "Ent = Sleep, Shft+Ent = Off"

    # Buttons functions ---------------------------
    def sleep():
        delay = get_delay()
        start_timer(delay, "Sleep")

    def shutdown():
        delay = get_delay()
        start_timer(delay, "Shutdown")

    def cancel():
        stop_timer()


    # Fonts ======================================
    font_title = tkFont.Font(
        family="Tiresias Signfont", 
        size=16, 
        weight=tkFont.BOLD
    )
    font_regular = tkFont.Font(
        family="Tiresias Signfont", 
        size=12, 
        weight=tkFont.NORMAL
    )
    

    # Wrapper block =================================
    frm_main = tk.Frame(
        master=window
    )
    frm_main.pack(padx=10, pady=10)

    # Header block ----------------------------------
    lbl_top = tk.Label(
        master=frm_main,
        text="Linux Shutdown Timer",
        font=font_title
    )
    lbl_top.pack(padx=5, pady=5)


    # Timer block -----------------------------------
    frm_timer = tk.Label(
        master=frm_main,
    )
    frm_timer.pack()

    lbl_time = tk.Label(
        master=frm_timer,
        text="Set delay:",
        font=font_regular
    )
    lbl_time.grid(row=0, column=0, sticky="w")

    ent_hours = tk.Entry(
        master=frm_timer,
        width=3
    )
    ent_hours.grid(row=0, column=1, sticky="e")

    lbl_separator1 = tk.Label(master=frm_timer, text=":")
    lbl_separator1.grid(row=0, column=2, sticky="e")

    ent_minutes = tk.Entry(
        master=frm_timer,
        width=3
    )
    ent_minutes.grid(row=0, column=3, sticky="e")

    lbl_separator2 = tk.Label(master=frm_timer, text=":")
    lbl_separator2.grid(row=0, column=4, sticky="e")

    ent_seconds = tk.Entry(
        master=frm_timer,
        width=3
    )
    ent_seconds.grid(row=0, column=5, sticky="e")

    # Message block -----------------------------------
    lbl_message = tk.Label(
        master=frm_main,
        text="Ent = Sleep, Shft+Ent = Off"
    )
    lbl_message.pack(padx=5, pady=5)

    frm_buttons = tk.Frame(
        master=frm_main
    )
    frm_buttons.pack()

    # Buttons block -----------------------------------
    btn_sleep = tk.Button(
        master=frm_buttons,
        text="Sleep",
        width=5,
        command=sleep
    )
    btn_sleep.grid(row=0, column=0, padx=5)

    btn_off = tk.Button(
        master=frm_buttons,
        text="Off",
        width=5,
        command=shutdown
    )
    btn_off.grid(row=0, column=1, padx=5)

    btn_cancel = tk.Button(
        master=frm_buttons,
        text="Cancel",
        width=5,
        command=cancel
    )
    btn_cancel.grid(row=0, column=2, padx=5)


    # =========================================

    def handle_keypress(event):
        match event.keysym:
            case "Escape":
                cancel()
            case "KP_Enter":
                match event.state:
                    case 16: sleep()
                    case 17: shutdown()
            case "Return":
                match event.state:
                    case 16: sleep()
                    case 17: shutdown()
    window.bind("<Key>", handle_keypress)

    window.mainloop()