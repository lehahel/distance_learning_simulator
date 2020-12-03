import flask
import json
from server import lib
import tkinter
from server import checker

app = flask.Flask("Distance Learning Server")

student = lib.Student('Unknown', 0)

default_ip = "localhost:8000"
registered = False


@app.route('/start', methods=['POST'])
def start():
    global student
    name = flask.request.args['name']
    weight = flask.request.args['weight']
    student = lib.Student(name, int(weight))
    return "Done"


@app.route('/get_params', methods=['GET'])
def get_params():
    return json.dumps(list(map(str, [student.energy, student.fat, student.get_mood(), student.xp])))


@app.route('/eat', methods=['POST'])
def eat():
    global student
    text = student.eat()
    return text


@app.route('/sleep', methods=['POST'])
def sleep():
    global student
    text = student.sleep()
    return text


@app.route('/play', methods=['POST'])
def play():
    global student
    text = student.play_games()
    return text


@app.route('/study', methods=['POST'])
def study():
    global student
    text = student.study()
    return text


class ServerWindow:
    def __init__(self):
        self.ip = "localhost"
        self.port = 8000
        self.root = tkinter.Tk()
        self.error_text = tkinter.StringVar()

        tkinter.Label(self.root, text="Server ip: ").grid(row=0, column=0)
        self.entry = tkinter.Entry(self.root)

        tkinter.Button(self.root, text="Start", width=20, command=self.start_server)\
            .grid(row=1, column=0, columnspan=3)

        tkinter.Label(self.root, textvariable=self.error_text, foreground="red").grid(row=2, column=0, columnspan=3)
        self.entry.insert(tkinter.END, default_ip)
        self.entry.grid(row=0, column=1, columnspan=2)

    def start(self):
        self.root.mainloop()

    def start_server(self):
        global app, registered
        ip = self.entry.get()
        if not checker.check_ip(ip):
            self.error_text.set("Error!\nip should have format *.*.*.*:*")
            return
        registered = True
        self.ip = ip
        self.root.destroy()


def main():
    server_window = ServerWindow()
    server_window.start()
    if not registered:
        exit()
    ip_port = server_window.ip.split(':')
    print(ip_port)
    app.run(ip_port[0], int(ip_port[1]), debug=False)


if __name__ == '__main__':
    main()
