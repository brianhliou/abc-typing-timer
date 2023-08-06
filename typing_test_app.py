import tkinter as tk
from tkinter import messagebox
import time
import heapq

class TypingTestApp:
    def __init__(self, master):
        self.master = master
        self.start_time = 0
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.current_char_index = 0
        self.is_typing = False
        self.labels = []
        self.fastest_times = []

        for i, char in enumerate(self.alphabet):
            label = tk.Label(master, text=char, font=("Helvetica", 24))
            label.grid(row=0, column=i)
            self.labels.append(label)

        self.timer_label = tk.Label(master, text="0.0", font=("Helvetica", 24))
        self.timer_label.grid(row=1, column=0, columnspan=len(self.alphabet), sticky='we')

        self.restart_button = tk.Button(master, text="Restart", command=self.restart)
        self.restart_button.grid(row=2, column=0, columnspan=len(self.alphabet), sticky='we')

        self.high_scores_button = tk.Button(master, text="High Scores", command=self.show_high_scores)
        self.high_scores_button.grid(row=3, column=0, columnspan=len(self.alphabet), sticky='we')

        master.bind('<Key>', self.key_press)

    def update_timer(self):
        if self.is_typing:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"{elapsed_time:.1f}")
            self.master.after(100, self.update_timer)

    def key_press(self, event):
        if event.char == self.alphabet[self.current_char_index]:
            if not self.is_typing:
                self.is_typing = True
                self.start_time = time.time()
                self.update_timer()
            self.labels[self.current_char_index].config(fg='green')
            self.current_char_index += 1
            if self.current_char_index < len(self.alphabet):
                self.labels[self.current_char_index].config(fg='black')
        else:
            self.labels[self.current_char_index].config(fg='red')
        if self.current_char_index == len(self.alphabet):
            self.is_typing = False
            elapsed_time = time.time() - self.start_time
            messagebox.showinfo("Time", f"Your time: {elapsed_time} seconds")
            if len(self.fastest_times) < 3 or elapsed_time < -self.fastest_times[0]:
                if len(self.fastest_times) == 3:
                    heapq.heappop(self.fastest_times)
                heapq.heappush(self.fastest_times, -elapsed_time)
            self.restart()

    def restart(self):
        self.is_typing = False
        self.current_char_index = 0
        for label in self.labels:
            label.config(fg='black')
        self.timer_label.config(text="0.0")

    def show_high_scores(self):
        scores = sorted([-x for x in self.fastest_times])
        messagebox.showinfo("High Scores", "\n".join(f"{x:.2f}" for x in scores))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Typing Test")
    app = TypingTestApp(root)
    root.mainloop()
