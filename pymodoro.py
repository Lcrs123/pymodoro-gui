import tkinter, datetime
from tkinter.ttk import *
import winsound

class tkinterApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('Pymodoro')
        self.resizable(width=False,height=False)
        self.work_time = tkinter.IntVar(self,value=25)
        self.interval_time = tkinter.IntVar(self,value=5)
        self.time_dict = {'work':self.work_time,'interval':self.interval_time}
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
        Spinbox(self.frame,textvariable=self.work_time,from_=1,increment=1,to=999).grid(row=2,column=1)
        Label(self.frame, text='Interval:',justify='right').grid(row=3, column=0)
        Spinbox(self.frame, textvariable=self.interval_time,from_=1,increment=1,to=999).grid(row=3, column=1)
        Separator(self.frame, orient='horizontal', ).grid(row=4, columnspan=2,sticky=tkinter.EW,pady=10)
        Button(self.frame, text='Start!',command=self.start_pomodoro).grid(row=5,columnspan=2)

    def start_pomodoro(self,interval_type='work'):
        self.withdraw()
        self.make_countdown_gui()
        self.play_beep()
        final_time = datetime.datetime.now()+datetime.timedelta(minutes=self.time_dict[interval_type].get())
        self.countdown(final_time=final_time)

    def make_countdown_gui(self,interval_type='work'):
        self.timecounter_toplevel = tkinter.Toplevel(self)
        chosen_worktime = datetime.time(minute=self.work_time.get())
        self.chosen_worktime = tkinter.StringVar(self,
                                                 value=f'{chosen_worktime.minute}:{chosen_worktime.second}')
        self.current_stage_str = tkinter.StringVar(self, value=(
            f'{interval_type.capitalize()}!'))
        Label(self.timecounter_toplevel, textvariable=self.current_stage_str,
              justify='center').grid(row=0, columnspan=2)
        Separator(self.frame, orient='horizontal', ).grid(row=1, columnspan=2,
                                                          sticky=tkinter.EW,
                                                          pady=10)
        Label(self.timecounter_toplevel, text='Time remaining:').grid(row=2,
                                                                      column=0)
        Label(self.timecounter_toplevel,
              textvariable=self.chosen_worktime).grid(row=2, column=1)
        Label(self.timecounter_toplevel, text='Completed cycles:').grid(row=3,
                                                                        column=0)
        Label(self.timecounter_toplevel, textvariable=self.cycles).grid(row=3,
                                                                        column=1)
        Button(self.timecounter_toplevel, text='Stop',
               command=self.stop_pomodoro).grid(row=4, column=0, columnspan=2)
        Separator(self.frame, orient='horizontal', ).grid(row=1, columnspan=2,
                                                          sticky=tkinter.EW,
                                                          pady=10)

    def stop_pomodoro(self):
        self.timecounter_toplevel.destroy()
        self.wm_deiconify()

    def countdown(self,final_time,interval_type:str='work'):
        assert interval_type in self.time_dict.keys()
        if datetime.datetime.now() < final_time and self.timecounter_toplevel.winfo_exists():
            diff = final_time - datetime.datetime.now()
            min_and_seconds = divmod(diff.seconds,60)
            self.chosen_worktime.set(value=f'{min_and_seconds[0]}:{min_and_seconds[1]}')
            self.after(100,self.countdown,final_time,interval_type)
        elif datetime.datetime.now() >= final_time:
            if interval_type == 'work':
                self.switch_countdown(switch_to='interval')
            elif interval_type == 'interval':
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
                        'interval': 'Time for a break!'}
        self.timecounter_toplevel.wm_deiconify()
        mbox = tkinter.Toplevel(master=self.timecounter_toplevel)
        Label(mbox,text=message_dict[switch_to]).pack()
        Button(mbox,command=mbox.destroy,text='Ok').pack()
        mbox.wm_deiconify()

    def update_cycle_count(self):
        self.interval_count+=1
        self.cycles.set(value=self.interval_count // 2)

    @staticmethod
    def play_beep(frequency=1000,duration=800,repeat=3):
        for _ in range(repeat):
            winsound.Beep(frequency,duration)

def main():
    app = tkinterApp()
    app.mainloop()

if __name__ == '__main__':
    main()
