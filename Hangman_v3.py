from struct import pack
import tkinter as tk
from tkinter import BOTH, RIGHT, YES, Label, PhotoImage, messagebox
import random
import pygame
from unidecode import unidecode


class PenduGame:  # classe contenant tout le Tkinter
    def __init__(self, master):
        pygame.mixer.music.load("background.mp3")
        pygame.mixer.music.play(loops=-1)
        with open(
            "Liste_mots.txt", "r"
        ) as file:  # on y inclut la liste de mots en .txt
            motus = file.readlines()
        self.master = master  # fenetre principale de l'écran
        self.master.title("pendu de Etane et Abygaël v3 final")
        self.master.geometry("1920x1080")
        self.master.iconbitmap("pendu.ico")
        self.mots_a_deviner = motus  # on affecte la liste de mots
        self.mot_secret = (
            self.choix_mot()
        )  # lié à la fonction le mot secret est placé ici
        self.lettres_trouvees = []  # les lettres trouvés seront placés ici
        self.nombre_essais = 7
        self.mot_trouve = False

        self.label_mot = tk.Label(
            master, text=self.gen_mot_a_afficher(), font=("ARIAL", 50)
        )  # ici, sera gardé le mot secré en tirets pour cacher les lettres non trouvés
        self.label_mot.pack(expand=YES, padx=10, pady=10)

        self.label_essais = tk.Label(
            master, text=f"Essais restants : {self.nombre_essais}"  # nombres d'essais
        )
        self.label_essais.pack()

        self.entry_lettre = tk.Entry(
            master, width=50, font=("Arial", 25)
        )  # zone de texte
        self.entry_lettre.pack(expand=YES, padx=10, pady=10)

        self.btn_proposer = tk.Button(
            master,
            text="Proposer",
            command=self.proposer_lettre,  # pour lancer la proposition
        )
        self.btn_proposer.pack(side=RIGHT, fill=BOTH, padx=10, pady=10)
        self.image_pendu = PhotoImage(file=f"pendu_{self.nombre_essais}.png")
        self.label_pendu = Label(master, image=self.image_pendu)
        self.label_pendu.pack(expand=YES)

    def choix_mot(self):
        motus_cosus = random.choice(self.mots_a_deviner)
        return unidecode(motus_cosus)

    def proposer_lettre(self):
        lettre_proposee = self.entry_lettre.get().lower()
        self.entry_lettre.delete(0, tk.END)  # Effacer le champ d'entrée

        self.nombre_essais = self.verif_lettre(lettre_proposee)

        self.label_mot.config(text=self.gen_mot_a_afficher())
        self.label_essais.config(text=f"Essais restants : {self.nombre_essais}")

        if self.gen_mot_a_afficher() == self.mot_secret:
            self.mot_trouve = True
            messagebox.showinfo("Bravo !", f"Tu as trouvé le mot : {self.mot_secret}")
            pygame.mixer.music.unload()
            pygame.mixer.music.load("youhou.mp3")
            pygame.mixer.music.play()
            self.master.destroy()
        elif self.nombre_essais == 0:
            pygame.mixer.music.unload()
            pygame.mixer.music.load("oh_no.mp3")
            pygame.mixer_music.play(loops=-1)
            messagebox.showinfo(
                "perdu...",
                f"Le mot c'est : {self.mot_secret}",
            )
            self.master.destroy()

    def verif_lettre(self, lettre):
        if lettre in self.lettres_trouvees:
            messagebox.showinfo("Oops !", "Tu as déjà proposé cette lettre. Réessaie !")
        elif lettre in self.mot_secret:
            messagebox.showinfo("Bonne lettre !", "Bien joué !")
            self.lettres_trouvees.append(lettre)
        else:
            messagebox.showinfo("Mauvaise lettre.", "Essai suivant.")
            self.nombre_essais -= 1
            self.lettres_trouvees.append(lettre)
            self.image_pendu = PhotoImage(file=f"pendu_{self.nombre_essais}.png")
            self.label_pendu.config(image=self.image_pendu)

        return self.nombre_essais

    def gen_mot_a_afficher(self):
        mot_affiche = ""
        for char in self.mot_secret:
            if char in self.lettres_trouvees:
                mot_affiche += char
            else:
                mot_affiche += "_ "
        return mot_affiche.strip()


def game():
    pygame.mixer.init()
    root = tk.Tk()
    root.configure(bg="White")
    game_instance = PenduGame(root)
    root.mainloop()


if __name__ == "__main__":
    game()
