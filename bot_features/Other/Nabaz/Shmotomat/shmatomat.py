import os
import random
from time import sleep

from APIs.TalpiotAPIs import *
from bot_framework.Feature.bot_feature import BotFeature
from bot_framework.View.button_group_view import ButtonGroupView
from bot_framework.View.image_view import ImageView
from bot_framework.View.view_container import ViewContainer
from bot_framework.session import Session
from bot_framework.ui.button import Button
from bot_framework.ui.ui import UI

IMAGE_EXT = ['.jpg', '.png', '.bmp', '.jpeg']
# games_dict = {}
# current_dir_text = None
# START_WIDTH = 480
# START_HEIGHT = 250
# WIDTH = 560
# HEIGHT = 480
# references = []
# g_buttons = {}
mahzors_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mahzors')


class Shmotomat(BotFeature):

    def __init__(self, ui: UI):
        super().__init__(ui)
        self.chosen_mahzor_dir = {}
        self.cadets_names: {str: {str: str}} = {}
        self.successes: {str: {str: int}} = {}

        self.image_view: {str: ImageView} = {}
        self.options_buttons_view: {str: ButtonGroupView} = {}

    def main(self, session: Session):
        self.ui.create_text_view(session, "👥 השמותומ\"ט 👥").draw()
        mahzors = [d for d in os.listdir(mahzors_dir) if os.path.isdir(os.path.join(mahzors_dir, d))]
        buttons = [Button(mahzor, lambda s, d=mahzor: self.init_game(s, d)) for mahzor in mahzors]
        buttons.append(Button('🔙 יציאה', self.remove_items))
        self.ui.create_button_group_view(session, "בחרו מחזור",  buttons).draw()

    def is_authorized(self, user: User) -> bool:
        return 'מתלם' in user.role

    def init_game(self, session, dir_):
        telegram_id = session.user.telegram_id
        self.chosen_mahzor_dir[telegram_id] = os.path.join(mahzors_dir, dir_)
        chosen_mahzor_dir = self.chosen_mahzor_dir[telegram_id]
        self.cadets_names[telegram_id] = {os.path.splitext(f)[0]: f for f in os.listdir(chosen_mahzor_dir)
                                          if os.path.isfile(os.path.join(chosen_mahzor_dir, f))
                                          and os.path.splitext(f)[-1].lower() in IMAGE_EXT}
        self.successes[telegram_id] = {name: 0 for name in self.cadets_names[telegram_id]}

        buttons = [
            Button('משחק 🎮',  self.guess_image),
            Button('למידה 📚', self.learn),
            Button('יציאה 🔙', self.reset_game),
        ]
        self.ui.create_button_group_view(session, "רוצים לשחק או ללמוד", buttons).draw()

    def reset_game(self, session):
        self.remove_items(session)
        self.main(session)

    def remove_items(self, session):
        try:
            self.options_buttons_view[session.user.telegram_id].remove()
            self.image_view[session.user.telegram_id].remove()
        except KeyError:
            self.ui.clear(session)

    def learn(self, session: Session):
        self.remove_items(session)
        telegram_id = session.user.telegram_id
        buttons = [Button(name, lambda s, n=name: self.send_image(s, n))
                   for name in self.cadets_names[telegram_id]]

        buttons.append(Button('🔙 חזרה', self.reset_game))
        self.options_buttons_view[telegram_id] = self.ui.create_button_group_view(session, "שמות הצוערים", buttons, )
        self.options_buttons_view[telegram_id].draw()

    def send_image(self, session, cadet_name):
        self.remove_items(session)
        telegram_id = session.user.telegram_id
        image_path = os.path.join(self.chosen_mahzor_dir[telegram_id],
                                  self.cadets_names[telegram_id][cadet_name])
        self.image_view[telegram_id] = self.ui.create_image_view(session, cadet_name, image_path)
        self.image_view[telegram_id].draw()
        name_list = list(self.cadets_names[telegram_id].keys())
        next_name = name_list[(name_list.index(cadet_name) + 1) % len(name_list)]
        buttons = [
            Button('⏭️התמונה הבאה', lambda s: self.send_image(s, next_name)),
            Button('🔙 חזרה', self.learn),
        ]
        self.options_buttons_view[telegram_id] = self.ui.create_button_group_view(session, cadet_name, buttons)
        self.options_buttons_view[telegram_id].draw()

    def guess_image(self, session: Session):
        self.ui.clear(session)
        telegram_id = session.user.telegram_id
        names = [name for name in self.cadets_names[telegram_id] if self.successes[telegram_id][name] < 2]
        if not names:
            self.ui.create_text_view(session, "🥳🥳🥳🥳🥳 ניצחת! כל הכבוד!!! 🥳🥳🥳🥳🥳").draw()
            self.reset_game(session)
            return
        sample_size = min(len(names), 4)
        options_names = random.sample(names, sample_size)
        chosen_name = random.choice(options_names)
        chosen_image_path = os.path.join(self.chosen_mahzor_dir[telegram_id],
                                         self.cadets_names[telegram_id][chosen_name])

        container = ViewContainer(session, self.ui)
        self.image_view[telegram_id] = self.ui.create_image_view(session, "נחשו מי בתמונה", chosen_image_path,
                                                                 view_container=container)
        self.image_view[telegram_id].draw()
        options_buttons = [Button(name, lambda s, c=chosen_name, n=name: self.check_guess(s, c, n))
                           for name in options_names]

        options_buttons.append(Button('יציאה 🔙', self.reset_game))
        self.options_buttons_view[telegram_id] = self.ui.create_button_group_view(session, "אפשרויות", options_buttons,
                                                                     view_container=container)
        self.options_buttons_view[telegram_id].draw()

    def check_guess(self, session, answer, guess):
        buttons = []
        if answer == guess:
            self.successes[session.user.telegram_id][answer] += 1

        for button in self.options_buttons_view[session.user.telegram_id].buttons[:-1]:
            if button.title == answer:
                button.title += ' 🟢 '

            else:
                button.title += ' ❌ '
            buttons.append(button)
        buttons.append(self.options_buttons_view[session.user.telegram_id].buttons[-1])
        self.options_buttons_view[session.user.telegram_id].update("תשובות", buttons)
        sleep(1)
        self.remove_items(session)
        self.guess_image(session)

    
# def guess_name():
#     global root
#     global g_buttons
#     options = random.sample(images, 4)
#     full_options = [os.path.join(dir, opt) for opt in options]
#     chosen = os.path.splitext(random.choice(options))[0]
#     options = [os.path.splitext(f)[0] for f in options]
#     label = tk.Label(root, text=chosen, font=("David", 40))
#     label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
#     button1 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, options[0]))
#     button1.place(relx = 0.25, rely = 0.4, anchor=tk.CENTER)
#     button2 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, options[1]))
#     button2.place(relx = 0.75, rely = 0.4, anchor=tk.CENTER)
#     button3 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, options[2]))
#     button3.place(relx = 0.25, rely = 0.8, anchor=tk.CENTER)
#     button4 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, options[3]))
#     button4.place(relx = 0.75, rely = 0.8, anchor=tk.CENTER)
#     buttons = [button4, button3, button2, button1]
#     for opt in full_options:
#         image = ImageTk.PhotoImage(Image.open(opt).resize((int(WIDTH / 3), int(HEIGHT / 3))))
#         references.append(image)
#         buttons.pop()['image'] = image
#     g_buttons = {button1: options[0], button2: options[1], button3: options[2], button4: options[3]}
#
# def guess_wrong_match():
#     global root
#     global g_buttons
#     options = random.sample(images, 5)
#     chosen = random.randint(0, 3)
#     full_options = [os.path.join(dir, opt) for opt in options[:-1]]
#     options = [os.path.splitext(f)[0] for f in options]
#     button1 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, 0))
#     button1.place(relx = 0.25, rely = 0.4, anchor=tk.CENTER)
#     button2 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, 1))
#     button2.place(relx = 0.75, rely = 0.4, anchor=tk.CENTER)
#     button3 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, 2))
#     button3.place(relx = 0.25, rely = 0.8, anchor=tk.CENTER)
#     button4 = tk.Button(root, height=int(HEIGHT / 3), width=int(WIDTH / 3), font=('Chunk', 14), command=lambda: check_guess(chosen, 3))
#     button4.place(relx = 0.75, rely = 0.8, anchor=tk.CENTER)
#     buttons = [button4, button3, button2, button1]
#     label = tk.Label(root, text="Guess the wrong match", font=("David", 40))
#     label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
#     label1 = tk.Label(root, text=options[0], font=("David", 20))
#     label1.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
#     label2 = tk.Label(root, text=options[1], font=("David", 20))
#     label2.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
#     label3 = tk.Label(root, text=options[2], font=("David", 20))
#     label3.place(relx=0.25, rely=0.9, anchor=tk.CENTER)
#     label4 = tk.Label(root, text=options[3], font=("David", 20))
#     label4.place(relx=0.75, rely=0.9, anchor=tk.CENTER)
#     labels = [label1, label2, label3, label4]
#     labels[chosen]['text'] = options[-1]
#     for opt in full_options:
#         image = ImageTk.PhotoImage(Image.open(opt).resize((int(WIDTH / 3), int(HEIGHT / 3))))
#         references.append(image)
#         buttons.pop()['image'] = image
#     g_buttons = {button1: 0, button2: 1, button3: 2, button4: 3}
#
# def guess_wrong_name():
#     global root
#     global g_buttons
#     options = random.sample(images, 5)
#     chosen = random.randint(0, 3)
#     full_options = [os.path.join(dir, opt) for opt in options[:-1]]
#     label = tk.Label(root, text="Guess the wrong name", font=("David", 40))
#     label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
#     options = [os.path.splitext(f)[0] for f in options]
#     button1 = tk.Button(root, text=options[0], height=1, width=16, font=('Chunk', 20), command=lambda: check_guess(chosen, 0))
#     button1.place(relx = 0.25, rely = 0.4, anchor=tk.CENTER)
#     button2 = tk.Button(root, text=options[1], height=1, width=16, font=('Chunk', 20), command=lambda: check_guess(chosen, 1))
#     button2.place(relx = 0.75, rely = 0.4, anchor=tk.CENTER)
#     button3 = tk.Button(root, text=options[2], height=1, width=16, font=('Chunk', 20), command=lambda: check_guess(chosen, 2))
#     button3.place(relx = 0.25, rely = 0.7, anchor=tk.CENTER)
#     button4 = tk.Button(root, text=options[3], height=1, width=16, font=('Chunk', 20), command=lambda: check_guess(chosen, 3))
#     button4.place(relx = 0.75, rely = 0.7, anchor=tk.CENTER)
#     buttons = [button1, button2, button3, button4]
#     buttons[chosen]['text'] = buttons[chosen]['text'].split()[0] + " " + " ".join(options[-1].split()[1:])
#     g_buttons = {button1: 0, button2: 1, button3: 2, button4: 3}
# # endregion
#
#
# # region - - - M E T H O D S - - -
# def choose_dir():
#     global dir
#     global current_dir_text
#     global root
#     dir = filedialog.askdirectory()
#     current_dir_text.delete(1.0, tk.END)
#     current_dir_text.insert(tk.INSERT, "Images Dir: \"{0}\"".format(dir))
#
# def init_game():
#     global images
#     global current_dir_text
#     try:
#         images = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and os.path.splitext(f)[-1].lower() in IMAGE_EXT]
#         if len(images) < 4:
#             current_dir_text.delete(1.0, tk.END)
#             current_dir_text.insert(tk.INSERT, "Error: Directory has less than 4 images")
#             return
#     except:
#         current_dir_text.delete(1.0, tk.END)
#         current_dir_text.insert(tk.INSERT, "Error: Invalid Directory")
#         return
#     load_game()
#
# def clear():
#     references.clear()
#     for child in root.winfo_children():
#         child.destroy()
#
# def start_train():
#     os.system("matlab -nosplash -nodesktop -r \"run('Trainer')\"")
#
# def load_menu():
#     global root
#     global current_dir_text
#     global dir
#     subdirs = next(os.walk(dir))[1]
#     if subdirs:
#         dir = os.path.join(dir, subdirs[0])
#
#     choose_button = tk.Button(root, text="Choose Directory", height=1, width=30, font=('Chunk', 18), command=choose_dir)
#     start_button = tk.Button(root, text="Start Playing", height=1, width=30, font=('Chunk', 18), command=init_game)
#     train_button = tk.Button(root, text="Matlab Version", height=1, width=30, font=('Chunk', 18), command=start_train)
#     current_dir_text = tk.Text(root, height=2, width=50)
#     current_dir_text.insert(tk.INSERT, "Images Dir: \"{0}\"".format(dir))
#     current_dir_text.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
#     choose_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
#     start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#     train_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
#     menubar = tk.Menu(root)
#     gamesmenu = tk.Menu(menubar, tearoff=0)
#     for game in GAMES:
#         games_dict[game] = tk.BooleanVar(root)
#         gamesmenu.add_checkbutton(label=game.__name__.replace('_', ' '), onvalue=True, offvalue=False, variable=games_dict[game])
#         games_dict[game].set(True)
#     menubar.add_cascade(label="Games", menu=gamesmenu)
#     root.config(menu=menubar)
#
#
# def refresh_dir():
#     global current_dir_text
#     current_dir_text.delete(1.0, tk.END)
#     current_dir_text.insert(tk.INSERT, "Images Dir: \"{0}\"".format(dir))
#
# def check_guess(answer, guess):
#     text = tk.Label(root, font=('David', 18))
#     text.place(relx = 0.5, rely=0.55, anchor=tk.CENTER)
#     for button, id in list(g_buttons.items()):
#         if id == answer:
#             button.config(bg="green")
#         else:
#             button.config(bg="red")
#     if answer == guess:
#         text['text'] = 'CORRECT!'
#         text.config(bg='green')
#     else:
#         text['text'] = 'WRONG!'
#         text.config(bg='red')
#
#     root.after(1000, load_game)
# # endregion

