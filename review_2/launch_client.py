import tkinter
from client import studlib
import requests
import ImageTk
import Image

registered = False


class RegWindow:
    def __init__(self):
        self.root = tkinter.Tk()
        self.name_text = tkinter.StringVar()
        self.error_text = tkinter.StringVar()

        self.name = "_"
        self.weight = -1
        self.server_ip = "_"

        self.name_button = tkinter.Button(self.root, text="enter", width="20")
        self.label_name = tkinter.Label(self.root, textvariable=self.name_text, width="30")
        self.entry_name = tkinter.Entry(self.root, width="30")
        self.label_error = tkinter.Label(self.root, textvariable=self.error_text, width="30", foreground="red")

    def start(self):
        self.name_text.set("Enter your name")
        self.name_button.bind("<Button-1>", self.set_name)

        self.label_name.pack()
        self.entry_name.pack()
        self.name_button.pack()
        self.label_error.pack()

        # self.root.geometry("200x140")
        self.root.title("reg")
        self.name_text.set("Enter your name")

        self.root.mainloop()

    def set_name(self, *args):
        text = self.entry_name.get()
        if not studlib.check_name(text):
            self.error_text.set("Error!\nName can only contain symbols\nfrom latin alphabet!")
            return
        self.name = self.entry_name.get()
        self.name_text.set("Enter your weight")
        self.entry_name.delete(0, 'end')
        self.error_text.set("")
        self.name_button.bind("<Button-1>", self.set_weight)

    def set_weight(self, *args):
        text = self.entry_name.get()
        if not studlib.check_weight(text):
            self.error_text.set("Error!\nWeight should be a number")
            return

        self.weight = int(self.entry_name.get())
        self.name_text.set("Enter your ip (with port)")
        self.entry_name.delete(0, 'end')
        self.error_text.set("")
        self.name_button.bind("<Button-1>", self.set_ip)

    def set_ip(self, *args):
        text = self.entry_name.get()
        if not studlib.check_ip(text):
            self.error_text.set("Error!\nip should have format *.*.*.*:*")
            return
        self.server_ip = text.replace(" ", "")
        self.entry_name.delete(0, 'end')
        self.error_text.set("")
        self.register()

    def register(self, *args):
        global registered
        requests.post(f'http://{self.server_ip}/start', params=dict(name=self.name,
                                                                    weight=str(self.weight)))
        registered = True
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.quit()
        # self.root.destroy()


reg_window = RegWindow()
reg_window.start()

if not registered:
    exit()


class GameWindow:
    def __init__(self, root_, weight, name, ip):
        self.root = root_

        self.energy_text = tkinter.StringVar()
        self.fat_text = tkinter.StringVar()
        self.mood_text = tkinter.StringVar()
        self.xp_text = tkinter.StringVar()

        self.eat_text = tkinter.StringVar()
        self.sleep_text = tkinter.StringVar()
        self.play_text = tkinter.StringVar()
        self.study_text = tkinter.StringVar()

        self.status = tkinter.StringVar()

        self.name = name
        self.weight = weight
        self.ip = ip

    def start(self, *args):
        tkinter.Label(self.root, width=40, height=2, text=self.name + "'s Learning", font=("Courier", 15)).grid(
            row=0, column=0, columnspan=4)

        tkinter.Label(self.root, width=20, textvariable=self.energy_text, borderwidth=2, relief="groove").grid(row=1,
                                                                                                               column=0)
        tkinter.Label(self.root, width=20, textvariable=self.fat_text, borderwidth=2, relief="groove").grid(row=1,
                                                                                                            column=1)
        tkinter.Label(self.root, width=20, textvariable=self.mood_text, borderwidth=2, relief="groove").grid(row=1,
                                                                                                             column=2)
        tkinter.Label(self.root, width=20, textvariable=self.xp_text, borderwidth=2, relief="groove").grid(row=1,
                                                                                                           column=3)

        self.energy_text.set("Energy: 0")
        self.fat_text.set("Fat: " + str(self.weight))
        self.mood_text.set("Mood: neutral")
        self.xp_text.set("XP: 0")

        self.eat_text.set("Eat")
        self.sleep_text.set("Sleep")
        self.play_text.set("Play games")
        self.study_text.set("Study")

        button_eat = tkinter.Button(self.root, width=20, textvariable=self.eat_text, foreground="green2")
        button_sleep = tkinter.Button(self.root, width=20, textvariable=self.sleep_text, foreground="maroon1")
        button_play = tkinter.Button(self.root, width=20, textvariable=self.play_text, foreground="blue2")
        button_study = tkinter.Button(self.root, width=20, textvariable=self.study_text, foreground="red")

        button_eat.bind("<Button-1>", self.eat)
        button_sleep.bind("<Button-1>", self.sleep)
        button_play.bind("<Button-1>", self.play)
        button_study.bind("<Button-1>", self.study)

        button_eat.grid(row=3, column=0)
        button_sleep.grid(row=3, column=1)
        button_play.grid(row=3, column=2)
        button_study.grid(row=3, column=3)

        tkinter.Label(self.root, text="").grid(row=2, column=0)
        tkinter.Label(self.root, textvariable=self.status).grid(row=4, column=0, columnspan=4)

        self.add_img()

        self.root.mainloop()

    def eat(self, *args):
        stat = requests.post(f'http://{self.ip}/eat').text
        self.update()
        self.status.set(stat)

    def sleep(self, *args):
        stat = requests.post(f'http://{self.ip}/sleep').text
        self.update()
        self.status.set(stat)

    def play(self, *args):
        stat = requests.post(f'http://{self.ip}/play').text
        self.update()
        self.status.set(stat)

    def study(self, *args):
        stat = requests.post(f'http://{self.ip}/study').text
        self.update()
        self.status.set(stat)

    def update(self, *args):
        status = requests.get(f'http://{self.ip}/get_params').text
        params = status.split('\n')
        self.energy_text.set("Energy: " + params[1])
        self.fat_text.set("Fat: " + params[2])
        self.mood_text.set("Mood: " + params[3])
        self.xp_text.set("XP: " + params[4])

    def add_img(self):
        load = Image.open('client/img/fat.jpg')
        render = ImageTk.PhotoImage(load)

        img = tkinter.Label(self.root, image=render)
        img.image = render
        img.grid(row=5, column=0, columnspan=4)


main_window = GameWindow(reg_window.root, reg_window.weight, reg_window.name, reg_window.server_ip)
main_window.start()
