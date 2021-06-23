import datetime
import tkinter
from tkinter.messagebox import showerror
from tkinter.ttk import *
from winsound import Beep
from itertools import cycle


class PomodoroApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('Pymodoro')
        self.resizable(width=False, height=False)
        self.init_time_attributes()
        self.init_longbreak_attributes()
        self.init_cycles_attributes()
        self.init_pause_attributes()
        self.current_stage_dict = {
            'work': "Work!",
            'break': "Break!",
            'longbreak': "Long break!"
        }
        self.beep_fail = False
        self.init_gui()

    def init_time_attributes(self):
        self.work_time = tkinter.IntVar(self, value=25)
        self.break_time = tkinter.IntVar(self, value=5)
        self.longbreak_time = tkinter.IntVar(self,value=15)
        self.time_dict = {
            'work': self.work_time,
            'break': self.break_time,
            'longbreak': self.longbreak_time
        }

    def init_longbreak_attributes(self):
        self.cycles_before_longbreak = tkinter.IntVar(self, value=3)
        self.do_longbreak = tkinter.BooleanVar(self, value=True)

    def init_cycles_attributes(self):
        self.interval_cycle = None
        self.interval_count = 0
        self.cycles = tkinter.IntVar(self, value=0)

    def init_pause_attributes(self):
        self.paused = tkinter.BooleanVar(self, value=False, name='PAUSE_STATE')
        self.pause_button_text = tkinter.StringVar(self, value='Pause')
        self.pause_time = None

    def init_gui(self):
        self.frame = Frame(self, padding='5 5')
        self.frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        Label(self.frame,
              text='Welcome to Pymodoro!\nChoose the amount of minutes for work/break and get to work!',
              justify='center'
              ).grid(row=0, column=0, columnspan=2)
        Separator(self.frame, orient='horizontal').grid(row=1, columnspan=2,
                                                          sticky=tkinter.EW,
                                                          pady=10
                                                        )
        Label(self.frame, text='Work:', justify='right').grid(row=2, column=0)
        Spinbox(self.frame, textvariable=self.work_time, from_=1, increment=1,
                to=59
                ).grid(row=2, column=1)
        Label(self.frame, text='Break:', justify='right').grid(row=3, column=0)
        Spinbox(self.frame, textvariable=self.break_time, from_=1, increment=1,
                to=59
                ).grid(row=3, column=1)
        Separator(self.frame, orient='horizontal', ).grid(row=4, columnspan=2,
                                                          sticky=tkinter.EW,
                                                          pady=10
                                                          )
        Label(self.frame, text='Do long breaks?', justify='right').grid(row=5,
                                                                        column=0
                                                                        )
        Checkbutton(self.frame,variable=self.do_longbreak,onvalue=True,
                    offvalue=False,command=self.toggle_longbreak
                    ).grid(row=5,column=1)
        Label(self.frame, text='Work cycles before long break:',
              justify='right'
              ).grid(row=6,column=0)
        Spinbox(self.frame, textvariable=self.cycles_before_longbreak, from_=1,
                increment=1,to=59, name='longbreak_cycles'
                ).grid(row=6, column=1)
        Label(self.frame, text='Long Break time:', justify='right').grid(row=7,
                                                                         column=0
                                                                         )
        Spinbox(self.frame, textvariable=self.longbreak_time, from_=1, increment=1,
                to=59, name='longbreak_time'
                ).grid(row=7, column=1)
        Separator(self.frame, orient='horizontal').grid(row=8, columnspan=2,
                                                          sticky=tkinter.EW,
                                                          pady=10
                                                          )
        Button(self.frame, text='Start!', command=self.start_pomodoro
               ).grid(row=9,columnspan=2)
        self.bind(sequence='<Return>', func=self.start_pomodoro)

    def start_pomodoro(self, event=None):
        if self.is_entry_valid():
            self.withdraw()
            self.interval_cycle = self.make_interval_cycle()
            self.make_countdown_gui()
            self.play_beep(repeat=2)
            final_time = datetime.datetime.now() + datetime.timedelta(
                minutes=self.time_dict[next(self.interval_cycle)].get())
            self.countdown(final_time=final_time)
        else:
            return

    def make_countdown_gui(self, interval_type='work'):
        self.countdown_toplevel = tkinter.Toplevel(self)
        self.countdown_toplevel.resizable(width=False, height=False)
        self.countdown_toplevel.title('Pymodoro')
        cd_frame = Frame(self.countdown_toplevel, padding='5 5')
        cd_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        cd_frame.columnconfigure(0, weight=1)
        cd_frame.rowconfigure(0, weight=1)
        chosen_worktime = datetime.time(minute=self.work_time.get())
        self.chosen_worktime = tkinter.StringVar(self,
                                                 value=f'{chosen_worktime.minute}:{chosen_worktime.second}'
                                                 )
        self.current_stage_str = tkinter.StringVar(self,
                                                   value=(f'{self.current_stage_dict[interval_type]}')
                                                   )
        Label(cd_frame, textvariable=self.current_stage_str,justify='center'
              ).grid(row=0, columnspan=2)
        Separator(cd_frame, orient='horizontal').grid(row=1, columnspan=3,
                                                      sticky=tkinter.EW,
                                                      pady=10
                                                      )
        Label(cd_frame, text='Time remaining:').grid(row=2, column=0)
        Label(cd_frame, textvariable=self.chosen_worktime).grid(row=2,
                                                                column=1
                                                                )
        Label(cd_frame, text='Completed cycles:').grid(row=3, column=0)
        Label(cd_frame, textvariable=self.cycles).grid(row=3, column=1)
        Separator(cd_frame, orient='horizontal').grid(row=4, columnspan=3,
                                                      sticky=tkinter.EW,
                                                      pady=10
                                                      )
        Button(cd_frame, text='Exit', command=self.stop_pomodoro).grid(row=5,
                                                                       column=0,
                                                                       columnspan=2
                                                                       )
        Button(cd_frame, textvariable=self.pause_button_text,
               command=self.pause_unpause).grid(row=6,column=0,columnspan=2)
        # Needed to get back to the start if user closes countdown through "x"
        # instead of clicking exit
        self.countdown_toplevel.protocol('WM_DELETE_WINDOW',self.stop_pomodoro)

    def stop_pomodoro(self):
        self.countdown_toplevel.destroy()
        self.reset_pause()
        self.reset_cycles()
        self.wm_deiconify()

    def countdown(self, final_time: datetime.datetime,
                  interval_type: str = 'work'):
        assert interval_type in self.time_dict.keys()
        if not self.paused.get():
            # Simply reducing the remaining time by a second every loop
            # will cause desync with real-time due to proccess time, even
            # if wait time is exactly 1 second. Need to calculate "now"
            # every loop and check against stored final_time.
            now = datetime.datetime.now()
            if now < final_time and self.countdown_toplevel.winfo_exists():
                diff = final_time - now
                min_and_seconds = divmod(diff.seconds, 60)
                self.chosen_worktime.set(
                    value=f'{min_and_seconds[0]}:{min_and_seconds[1]}')
                self.after(100, self.countdown, final_time, interval_type)
            elif now >= final_time:
                self.switch_countdown(switch_to=next(self.interval_cycle))

        else:
            self.wait_variable(name='PAUSE_STATE')
            # stop the function if the countdown was closed while paused
            if not self.countdown_toplevel.winfo_exists():
                return
            time_paused = datetime.datetime.now() - self.pause_time
            min_and_seconds = divmod(time_paused.seconds, 60)
            final_time = final_time + datetime.timedelta(
                minutes=min_and_seconds[0], seconds=min_and_seconds[1])
            self.countdown(final_time=final_time, interval_type=interval_type)

    def switch_countdown(self, switch_to: str):
        self.play_beep()
        self.update_cycle_count()
        self.display_switch_message(switch_to=switch_to)
        self.current_stage_str.set(value=self.current_stage_dict[switch_to])
        final_time = datetime.datetime.now() + datetime.timedelta(
            minutes=self.time_dict[switch_to].get())
        self.countdown(final_time=final_time, interval_type=switch_to)

    def display_switch_message(self, switch_to):
        message_dict = {
            'work': 'Break time is over, back to work!',
            'break': 'Time for a break!',
            'longbreak': 'Time for a long break!'
        }
        self.countdown_toplevel.wm_deiconify()
        mbox = tkinter.Toplevel(master=self.countdown_toplevel)
        Label(mbox, text=message_dict[switch_to]).pack()
        Button(mbox, command=mbox.destroy, text='Ok').pack()
        mbox.wm_deiconify()

    def update_cycle_count(self):
        self.interval_count += 1
        self.cycles.set(value=self.interval_count // 2)

    def play_beep(self,frequency=1000, duration=800, repeat=3):
        if self.beep_fail:
            return
        try:
            for _ in range(repeat):
                Beep(frequency, duration)
        except RuntimeError:
            self.beep_fail = True
            showerror(message='Could not beep.\nProgram will continue without beeping between cycles.')


    def is_entry_valid(self):
        try:
            if any(x.get() not in range(1,60) for x in [
                self.work_time,
                self.break_time,
                self.longbreak_time,
                self.cycles_before_longbreak
            ]
                   ):
                raise ValueError
            else:
                return True
        # TclError is raised by IntVar.get() when entry is not a number
        except (tkinter.TclError, ValueError):
            showerror(message='Work, Break, Long Break times and cycles must be numbers from 1 to 59 minutes')
            return False

    def pause_unpause(self):
        self.paused.set(value=not self.paused.get())
        if self.paused.get():
            self.pause_time = datetime.datetime.now()
            self.pause_button_text.set(value='Unpause')
        else:
            self.pause_button_text.set(value='Pause')

    def reset_pause(self):
        self.pause_button_text.set(value='Pause')
        self.paused.set(value=False)
        self.pause_time = None

    def reset_cycles(self):
        self.cycles.set(value=0)
        self.interval_count = 0

    def toggle_longbreak(self):
        # Setting True to "active", "on" or "normal" doesn't work. The "disabled"
        # flag works independently and must be reversed through !disabled
        state_dict = {
            True:'!disabled',
            False:'disabled'
        }
        longbreak_widgets = [x for x in self.frame.winfo_children() if str(x.winfo_name()).startswith('longbreak')]
        for x in longbreak_widgets:
            x.state([state_dict[self.do_longbreak.get()]])

    def make_interval_cycle(self):
        if self.do_longbreak.get():
            interval_cycle = ['work','break']*self.cycles_before_longbreak.get()
            interval_cycle[-1] = 'longbreak'
            return cycle(interval_cycle)
        else:
            return cycle(['work','break'])


def main() -> None:
    app = PomodoroApp()
    app.mainloop()


if __name__ == '__main__':
    main()