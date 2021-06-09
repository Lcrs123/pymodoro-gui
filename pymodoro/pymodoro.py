import datetime
import tkinter
from tkinter.messagebox import showerror
from tkinter.ttk import *
from winsound import Beep


class PomodoroApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('Pymodoro')
        self.resizable(width=False,height=False)
        self.work_time = tkinter.IntVar(self,value=25)
        self.break_time = tkinter.IntVar(self, value=5)
        self.time_dict = {'work': self.work_time, 'break': self.break_time}
        self.interval_count = 0
        self.cycles = tkinter.IntVar(self,value=0)
        self.init_gui()

    def init_gui(self):
        self.frame = Frame(self,padding='5 5')
        self.frame.grid(row=0,column=0, sticky=tkinter.NSEW)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(0,weight=1)
        Label(self.frame,text='Welcome to Pymodoro!\nChoose the amount of minutes for work and interval and get to work!',justify='center').grid(row=0,column=0,columnspan=2)
        Separator(self.frame, orient='horizontal',).grid(row=1,columnspan=2,sticky=tkinter.EW,pady=10)
        Label(self.frame, text='Work:',justify='right').grid(row=2, column=0)
        Spinbox(self.frame, textvariable=self.work_time, from_=1, increment=1,
                to=59).grid(row=2, column=1)
        Label(self.frame, text='Break:', justify='right').grid(row=3, column=0)
        Spinbox(self.frame, textvariable=self.break_time, from_=1, increment=1,
                to=59).grid(row=3, column=1)
        Separator(self.frame, orient='horizontal', ).grid(row=4, columnspan=2,sticky=tkinter.EW,pady=10)
        Button(self.frame, text='Start!',command=self.start_pomodoro).grid(row=5,columnspan=2)

    def start_pomodoro(self,interval_type='work'):
        if self.is_entry_valid():
            self.withdraw()
            self.make_countdown_gui()
            self.play_beep(repeat=2)
            final_time = datetime.datetime.now() + datetime.timedelta(
                minutes=self.time_dict[interval_type].get())
            self.countdown(final_time=final_time)
        else:
            return

    def make_countdown_gui(self,interval_type='work'):
        self.countdown_toplevel = tkinter.Toplevel(self)
        self.countdown_toplevel.resizable(width=False, height=False)
        self.countdown_toplevel.title('Pymodoro')
        cd_frame = Frame(self.countdown_toplevel, padding='5 5')
        cd_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        cd_frame.columnconfigure(0, weight=1)
        cd_frame.rowconfigure(0, weight=1)
        chosen_worktime = datetime.time(minute=self.work_time.get())
        self.chosen_worktime = tkinter.StringVar(self,
                                                 value=f'{chosen_worktime.minute}:{chosen_worktime.second}')
        self.current_stage_str = tkinter.StringVar(self, value=(
            f'{interval_type.capitalize()}!'))
        Label(cd_frame, textvariable=self.current_stage_str,
              justify='center').grid(row=0, columnspan=2)
        Separator(cd_frame, orient='horizontal').grid(row=1, columnspan=3,
                                                          sticky=tkinter.EW,
                                                          pady=10)
        Label(cd_frame, text='Time remaining:').grid(row=2, column=0)
        Label(cd_frame, textvariable=self.chosen_worktime).grid(row=2,
                                                                column=1)
        Label(cd_frame, text='Completed cycles:').grid(row=3, column=0)
        Label(cd_frame, textvariable=self.cycles).grid(row=3, column=1)
        Separator(cd_frame, orient='horizontal').grid(row=4, columnspan=3,
                                                          sticky=tkinter.EW,
                                                          pady=10)
        Button(cd_frame, text='Stop', command=self.stop_pomodoro).grid(row=5,
                                                                       column=0,
                                                                       columnspan=2)
        self.countdown_toplevel.protocol('WM_DELETE_WINDOW',
                                         self.stop_pomodoro)

    def stop_pomodoro(self):
        self.countdown_toplevel.destroy()
        self.wm_deiconify()

    def countdown(self,final_time,interval_type:str='work'):
        assert interval_type in self.time_dict.keys()
        if datetime.datetime.now() < final_time and self.countdown_toplevel.winfo_exists():
            diff = final_time - datetime.datetime.now()
            min_and_seconds = divmod(diff.seconds,60)
            self.chosen_worktime.set(value=f'{min_and_seconds[0]}:{min_and_seconds[1]}')
            self.after(100,self.countdown,final_time,interval_type)
        elif datetime.datetime.now() >= final_time:
            if interval_type == 'work':
                self.switch_countdown(switch_to='break')
            elif interval_type == 'break':
                self.switch_countdown(switch_to='work')

    def switch_countdown(self,switch_to:str):
        self.play_beep()
        self.update_cycle_count()
        self.display_switch_message(switch_to=switch_to)
        self.current_stage_str.set(value=f'{switch_to.capitalize()}!')
        final_time = datetime.datetime.now() + datetime.timedelta(minutes=self.time_dict[switch_to].get())
        self.countdown(final_time=final_time,interval_type=switch_to)

    def display_switch_message(self,switch_to):
        message_dict = {'work': 'Break time is over, back to work!',
                        'break': 'Time for a break!'}
        self.countdown_toplevel.wm_deiconify()
        mbox = tkinter.Toplevel(master=self.countdown_toplevel)
        Label(mbox,text=message_dict[switch_to]).pack()
        Button(mbox,command=mbox.destroy,text='Ok').pack()
        mbox.wm_deiconify()

    def update_cycle_count(self):
        self.interval_count+=1
        self.cycles.set(value=self.interval_count // 2)

    @staticmethod
    def play_beep(frequency=1000,duration=800,repeat=3):
        for _ in range(repeat):
            Beep(frequency, duration)

    def is_entry_valid(self):
        try:
            assert self.work_time.get() in range(1,
                                                 60) and self.break_time.get() in range(
                1, 60)
            return True
        except:
            AssertionError(showerror('Error',
                                     message='Work and Break times must be numbers from 1 to 59 minutes'))
            return False

def main():
    app = PomodoroApp()
    app.mainloop()


if __name__ == '__main__':
    main()
