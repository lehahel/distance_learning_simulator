import tkinter
import threading
from client import studlib
import requests
import ImageTk
import Image
import json
from time import sleep

registered = False
default_ip = "localhost:8000"

handlers = {
    'size': 3,
    'text': [
        "Enter your name",
        "Enter your weight",
        "Enter your ip (with port)"
    ],
    'checker': [
        studlib.check_name,
        studlib.check_weight,
        studlib.check_ip
    ],
    'error_text': [
        "Error!\nName can only contain symbols\nfrom latin alphabet!",
        "Error!\nWeight should be a number",
        "Error!\nip should have format *.*.*.*:*"
    ],
    'info_type': [
        'name',
        'weight',
        'ip'
    ]
}


class RegWindow:
    def __init__(self):
        self.root = tkinter.Tk()
        self.name_text = tkinter.StringVar()
        self.error_text = tkinter.StringVar()

        self.user_info = {info: None for info in handlers['info_type']}
        self.cur_handler = 0

        self.elements = {
            'label_name': tkinter.Label(self.root, textvariable=self.name_text, width="30"),
            'entry_name': tkinter.Entry(self.root, width="30"),
            'name_button': tkinter.Button(self.root, text="enter", width="20"),
            'label_error': tkinter.Label(self.root, textvariable=self.error_text, width="30", foreground="red")
        }

    def start(self):
        self.name_text.set(handlers['text'][self.cur_handler])
        self.elements['name_button'].bind("<Button-1>", self.set_stat)
        for element in self.elements.values():
            element.pack()
        self.root.title("DLS")
        self.name_text.set(handlers['text'][self.cur_handler])
        self.root.mainloop()

    def set_stat(self, *args):
        global handlers
        text = self.elements['entry_name'].get()
        if not handlers['checker'][self.cur_handler](text):
            self.error_text.set(handlers['error_text'][self.cur_handler])
            return

        self.user_info[handlers['info_type'][self.cur_handler]] = text
        self.cur_handler += 1
        if self.cur_handler >= handlers['size']:
            thread = threading.Thread(target=self.register, args=())
            thread.start()
            # self.register()
            return
        self.name_text.set(handlers['text'][self.cur_handler])
        self.elements['entry_name'].delete(0, 'end')
        if self.cur_handler == handlers['size'] - 1:
            self.elements['entry_name'].insert(tkinter.END, default_ip)
        self.error_text.set("")

    def register(self, *args):
        global registered
        try:
            requests.post('http://{}/start'.format(self.user_info['ip']),
                          params=dict(name=self.user_info['name'], weight=self.user_info['weight']))
            registered = True
            for widget in self.root.winfo_children():
                widget.destroy()
            self.root.quit()
        except requests.exceptions.ConnectionError:
            self.cur_handler -= 1
            self.error_text.set("No connection!")


class GameWindow:
    def __init__(self, root_, ip, name):
        self.root = root_
        self.status = tkinter.StringVar()
        self.ip = ip

        self.buttons = [
            ["Eat", "green2", lambda: self.act('eat')],
            ["Sleep", "maroon1", lambda: self.act('sleep')],
            ["Play", "blue2", lambda: self.act('play')],
            ["Study", "red", lambda: self.act('study')]
        ]
        self.label_texts = {stat: tkinter.StringVar() for stat in ['energy', 'fat', 'mood', 'xp']}

        for idx, text in enumerate(self.label_texts.values()):
            tkinter.Label(self.root, width=20, textvariable=text, borderwidth=2, relief="groove")\
                .grid(row=1, column=idx)

        for idx, button in enumerate(self.buttons):
            tkinter.Button(self.root, width=20, text=button[0], foreground=button[1], command=button[2]) \
                .grid(row=3, column=idx)

        tkinter.Label(self.root, width=40, height=2, text=name + "'s Learning", font=("Courier", 15)).grid(
            row=0, column=0, columnspan=4)
        tkinter.Label(self.root, textvariable=self.status).grid(row=4, column=0, columnspan=4)

    def start(self, *args):
        self.add_img()
        self.update()
        self.root.mainloop()

    def act(self, action):
        new_thread = threading.Thread(target=self.act_request, args=(action,))
        new_thread.start()

    def act_request(self, action):
        stat = requests.post(f'http://{self.ip}/{action}').text
        self.update()
        self.status.set(stat)

    def update(self, *args):
        status = requests.get(f'http://{self.ip}/get_params').text
        params = json.loads(status)
        for idx, key in enumerate(self.label_texts):
            self.label_texts[key].set(key + ': ' + params[idx])

    def add_img(self):
        load = Image.open('client/img/fat.jpg')
        render = ImageTk.PhotoImage(load)
        img = tkinter.Label(self.root, image=render)
        img.image = render
        img.grid(row=5, column=0, columnspan=4)


def main():
    reg_window = RegWindow()
    reg_window.start()
    if not registered:
        exit()

    main_window = GameWindow(reg_window.root, reg_window.user_info['ip'], reg_window.user_info['name'])
    main_window.start()


if __name__ == "__main__":
    main()
