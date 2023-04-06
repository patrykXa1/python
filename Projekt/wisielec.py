#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
import random
import json
from base import Players, Scores, Session


loss_count = 0
win_count = 0
score = 0
number_of_left_letters = 32
session = Session()
color = '#e5eeba'
player_nick = ""
player_id = 0
category = ""


class Window:
    @staticmethod
    def init(self):
        """ Displays two buttons to select a player
        Parameters
        ----------
        self:Tk()
        """
        self.geometry("1100x600")
        self.config(bg=color)

        image_new_player = PhotoImage(file='button_nowy-gracz.png')
        new_player_btn = Button(self, bd=0, bg=color, activebackground=color, font=10, image=image_new_player)
        new_player_btn.image = image_new_player
        new_player_btn['command'] = lambda: Window.new_player(self, new_player_btn, select_account_btn)
        new_player_btn.place(x=450, y=175)

        image_select_account = PhotoImage(file='button_wybierz-konto.png')
        select_account_btn = Button(self, bd=0, bg=color, activebackground=color, font=10, image=image_select_account)
        select_account_btn.image = image_select_account
        select_account_btn['command'] = lambda: Window.select_player(self, new_player_btn, select_account_btn)
        select_account_btn.place(x=450, y=375)

    @staticmethod
    def select_player(self, new_player_btn, select_account_btn):
        """ Command for button to select a player
        Create entry for nick

        Parameters
        ----------
        self: Tk()
        new_player_btn:button
        select_account_btn:button
        """
        font = ("Comic Sans MS", 10)
        select_account_btn.destroy()
        new_player_btn.destroy()

        nick_label = Label(self, text="Wpisz swój nick:", bg=color, font=font)
        nick_label.place(x=370, y=275)

        nick_entry = Entry(self)
        nick_entry.place(x=520, y=275)

        submit_button = Button(self, text="submit", bg=color, activebackground=color, font=font)
        submit_button['command'] = lambda: Window.submit_select_player(self, nick_entry)
        submit_button.place(x=370, y=315)

    @staticmethod
    def submit_select_player(self, nick_entry):
        """ Command for submit select player
            if nick in correct (it is in database) displays categories
            else
            display alert

            Parameters
            ----------
            self:Tk()
            nick_entry:entry
        """
        nick = nick_entry.get()
        global player_id, player_nick
        font2 = ('Comic Sans Ms', 8,)
        if nick != "":
            if len(session.query(Players).filter(Players.nick == nick).all()) != 0:
                player_id = session.query(Players).filter(Players.nick == nick).all()[0].id
                player_nick = nick
                Window.delete_widgets(self)
                Window.categories(self)
            else:
                alert = Label(self, text="wpisz prawidłowy nick", bg=color, font=font2)
                alert.place(x=430, y=315)

    @staticmethod
    def new_player(self, new_player_btn, select_account_btn):
        """
        Displays entry for nick and e-mail of new player,
        display submit button to save data and start the game

        Parameters
        ----------
        self:Tk()
        new_player_btn:button
        select_account_btn:button
        """
        font = ("Comic Sans MS", 10)
        select_account_btn.destroy()
        new_player_btn.destroy()

        nick_label = Label(self, text="nick:", bg=color, font=font)
        nick_label.place(x=460, y=265)

        e_mail_label = Label(self, text="e-mail:", bg=color, font=font)
        e_mail_label.place(x=460, y=315)

        nick_entry = Entry(self)
        nick_entry.place(x=510, y=265)

        e_mail_entry = Entry(self)
        e_mail_entry.place(x=510, y=315)

        submit_button = Button(self, text="submit", bg=color, activebackground=color, font=font)
        submit_button['command'] = lambda: Window.submit_new_player(self, nick_entry, e_mail_entry)
        submit_button.place(x=460, y=375)

    @staticmethod
    def submit_new_player(self, nick_entry, e_mail_entry):
        """If nick is uniq display categories
        else
        display alert

        Parameters
        ----------
        self:Tk()
        nick_entry:entry
        e_mail_entry:entry
        """
        nick = nick_entry.get()
        e_mail = e_mail_entry.get()
        global player_id, player_nick
        font2 = ('Comic Sans Ms', 8)
        if nick != "" and e_mail != "":
            if len(session.query(Players).filter(Players.nick == nick).all()) ==0:
                session.add(Players(nick, e_mail))
                player_nick = nick
                player_id = session.query(Players).filter(Players.nick == nick).all()[0].id
                Window.delete_widgets(self)
                Window.categories(self)
            else:
                alert = Label(self, text="wpisz unikalny nick", bg=color, font=font2)
                alert.place(x=470, y=400)

    @staticmethod
    def categories(self):
        """Display categories for of words for the game"""
        self.geometry("1100x600")

        self.config(bg=color)
        categories = ['geografia', 'jedzenie', 'anatomia', 'muzyka','zwierzęta']
        buttons = ['button_geografia', 'button_jedzenie', 'button_anatomia', 'button_muzyka', 'button_zwierzeta']
        y = 40
        for i in range(0, 5):
            image = PhotoImage(file='{}.png'.format(buttons[i]))
            button = Button(self, bd=0, bg=color, activebackground=color, font=10, image=image)
            button.image = image
            button.place(x=450, y=y)
            y += 120
            button['command'] = lambda category= categories[i]: Window.select_category(self, category)

    @staticmethod
    def random_word():
        """Select random word from file in chosen category"""
        global category
        index = random.randint(0, 25)
        with open('kategorie.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
            word = data[category][index]
        return word

    @staticmethod
    def select_category(self, this_category):
        """Save category to variable and start the game"""
        global category
        category = this_category
        Window.delete_widgets(self)
        Window.board(self)

    @staticmethod
    def board(self):
        """Displays alphabet buttons
        Displays labels for player,score and category
        calls function check_the_letter after click on letter button"""

        player_label = Label(self,text=f'Gracz: {player_nick}',bg=color, font=("arial", 20))
        player_label.place(x=700,y=25)

        score_label = Label(self,text = f'Wynik:{score}',bg=color, font=("arial", 20))
        score_label.place(x=900,y=25)

        category_label = Label(self, text=f'Kategoria: {category}', bg=color, font=("arial", 20))
        category_label.place(x=700, y=75)

        x = 300
        label = []
        the_word = Window.random_word()
        for i in range(0, len(the_word)):
            x += 60
            label.append(Label(self, text="_", bg=color, font=("arial", 40)))
            label[i].place(x=x, y=150)

        hangman = []
        h_images = ['draw1', 'draw2', 'draw3', 'draw4', 'draw5', 'draw6', 'draw7', 'draw8', 'draw9', 'draw10', 'draw11']
        for image in h_images:
            draw = PhotoImage(file="{}.png".format(image))
            hangman.append(Label(self, bg=color, image=draw))
            hangman[len(hangman) - 1].image = draw

        alphabet = ['button_a', 'button_ą', 'button_b', 'button_c', 'button_ć', 'button_d', 'button_e', 'button_ę', 'button_f', 'button_g', 'button_h', 'button_i', 'button_j','button_k','button_l','button_ł', 'button_m',
                    'button_n', 'button_ń', 'button_o', 'button_ó', 'button_p', 'button_r', 'button_s', 'button_ś', 'button_t', 'button_u', 'button_w',
                    'button_y', 'button_z', 'button_ź', 'button_ż']
        x = 240
        y = 350
        for letter in alphabet:
            x += 60
            image = PhotoImage(file="{}.png".format(letter))
            button = Button(self, bd=0, bg=color, activebackground=color, font=10, image=image)
            button['command'] = lambda last_letter=letter[len(letter)-1], button=button: Window.check_the_letter(self,last_letter,label,the_word,button,hangman,score_label)
            # Use default parameter to avoid late-binding issue (Otherwise last_letter is bound when the lambda function is called, not when it is created):
            button.image = image  # keep reference because of garbage collector
            button.place(x=x, y=y)
            if x == 720:
                x = 240
                y += 60




    @staticmethod
    def check_the_letter(self, letter, label, the_word, button, hangman, score_label):
        """
        Check if variable letter is in string the word

        Parameters
        ----------
        self:Tk()
        letter:string
        label:Label
        the_word:string
        button:Button
        hangman:Label
        score_label:Label
        """
        global win_count, loss_count, score, number_of_left_letters
        button.destroy()
        #print(the_word)
        number_of_left_letters -= 1
        if letter in the_word:
            for i in range(0, len(the_word)):
                if letter == the_word[i]:
                    win_count += 1
                    score += 1
                    label[i].config(text=letter)
                    score_label.config(text=f'Wynik:{score}')
            if win_count == len(the_word):

                answer = messagebox.askyesno('Koniec gry', 'Wygrałeś!\nChcesz zagrać jeszcze raz?')
                if answer:
                    win_count = 0
                    loss_count = 0
                    score *= number_of_left_letters
                    # save score to session
                    session.add(Scores(player_id, score))
                    number_of_left_letters = 26
                    score = 0
                    Window.delete_widgets(self)
                    Window.board(self)
                else:
                    self.destroy()

        else:
            loss_count += 1
            hangman[loss_count-1].place(x=0, y=0)

            if loss_count == 11:
                answer = messagebox.askyesno('Koniec gry', 'Przegrałeś!\nChcesz zagrać jeszcze raz?')
                if answer:
                    win_count = 0
                    loss_count = 0
                    score -= number_of_left_letters
                    # save score to session
                    session.add(Scores(player_id, score))
                    number_of_left_letters = 26
                    score = 0
                    Window.delete_widgets(self)
                    Window.board(self)
                else:
                    self.destroy()

    @staticmethod
    def delete_widgets(self):
        """
        Delete all widgets

        """
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = Tk()
    Window.init(root)
    root.mainloop()

session.commit()
session.close()






