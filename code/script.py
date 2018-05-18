###########################
# Fichier classe.py       #
# 06/05/18                #
# La communauté de l'info #
###########################

from classe import *
from projet import *


def entree():
    while True:
        try:
            x = int(input(""))
            if x <= 0:
                raise ValueError
            break
        except ValueError:
            print("Oups ! Vous devez entrer un nombre entier strictement positif, essayez encore...")
    return x


listeBW = []
input(
    "Bonjour. Vous allez découvrir le code réalisé par la Communauté de l\'info pour le projet HMM."
    " Pour continuer appuyez sur entrée.")
print()

choice = int(input(
    "Que voulez-vous faire ? 1 = Tester les fonctionnalités de la classe, 2 = Générer un mot dans une langue choisie, "
    "3 = Prédire la langue d'un mot, 4 = Arrêter : "))

while choice < 1 or choice > 4:
    choice = int(input("réponse incorrecte, réessayez : "))

while choice != 4:
    if choice == 1:
        print("---TEST DE LA CLASSE HMM---")
        while True:
            try:
                adr = input("Veuillez entrer un chemin vers un HMM stocké sous format texte : ")
                h = HMM.load(adr)
                break
            except:
                print("Le chemin n'est pas valide, essayez encore...")

        print()
        print("Le HMM qui a été chargé est le suivant :")
        print()
        print(h)

        var = 'o'
        while var == 'o':
            print()
            print("Veuillez entrer une longueur de mot à générer aléatoire grâce au HMM chargé : ")
            n = entree()
            print()

            w = h.generate_random(n)
            print("Le mot de", n, "lettres qui a été généré aléatoirement est", w)
            listeBW += [w]
            print("La probabilité que ce mot soit généré était de", h.pfw(w), ", soit une log-vraisemblance de",
                  h.logV([w]))
            chemin, p = h.viterbi(w)
            print("Le cheminement d'états le plus probable pour la génération de ce mot est", chemin,
                  "avec une probabilité logarithmique de", p)
            prochaine = h.predit(w)
            print("Si l'on continuait à générer des lettres pour ce mot, la prochaine serait le plus probalement",
                  prochaine)
            print()
            var = input("Voulez-vous générer une autre séquence afin d'utiliser Baum Welch (o/n) ? ")

            while var != 'o' and var != 'n':
                print("Choisissez o ou n...")
                print()
                var = input("Voulez-vous générer une autre séquence afin d'utiliser Baum Welch (o/n) ? ")

        print()
        print("La log-vraisemblance de l'échantillon", listeBW, "est de", h.logV(listeBW))
        print("Combien de fois voulez-vous effectuer Baum Welch ? ")
        nb = entree()

        print()
        for i in range(nb):
            h.bw1(listeBW)
            print("étape", i + 1, ": La log-vraisemblance de l'échantillon", listeBW, "est de", h.logV(listeBW))

        print()
        print("Le nouveau HMM pour lequel la vraisemblance de l'échantillon", listeBW, "a été augmentée", nb,
              "fois est le suivant :")
        print()
        print(h)
        print()
        print("La vraisemblance de l'échantillon", listeBW, "est désormais de", h.logV(listeBW))

        while True:
            try:
                print()
                reponse = input("Voulez vous enregistrer le nouveau HMM dans un fichier texte (o/n) ? ")
                if reponse not in ["o", "n"]:
                    raise ValueError
                break
            except:
                print("Veuillez entrer une réponse valide...")

        if reponse == "o":
            while True:
                try:
                    print()
                    chemin = input('Entrez le chemin du fichier de sortie : ')
                    h.save(chemin)
                    break
                except:
                    print("Le chemin n'est pas valide, essayez encore...")

        print()

    if choice == 2:
        print("--- GENERATION DE MOTS ---")

        langues = ["allemand", "anglais", "elfique", "espagnol", "neerlandais", "suedois"]

        i = int(input(
            "Choisissez une langue : 1 = Allemand, 2 = Anglais, 3 = Elfique, 4 = Espagnol, "
            "5 = Neerlandais, 6 = Suedois : "))

        while i > (len(langues)):
            i = int(input("erreur, réessayez : "))
        h = HMM.load("hmm_" + langues[i - 1])
        print(langues[i - 1])
        nb_mots = int(input("Combien de mots voulez-vous générer? "))
        for i in range(nb_mots):
            n = random.randint(3, 8)
            print(h.gen_mot_lettres(n))

        print()

    if choice == 3:
        print("---PREDICTION DE LA LANGUE D'UN MOT---")
        choix = "o"

        while choix == 'o':
            mot = input("Entrez un mot en allemand, anglais, elfique, espagnol, neerlandais ou suedois : ").lower()
            print('Langue la plus probable pour ce mot = ', reconnaitre_langue(mot))
            choix = input("Voulez-vous prédire la langue d'un autre mot (o/n) ? ")
            while choix not in ['o', 'n']:
                choix = input("Réponse invalide, réessayez : ")

        print()

    choice = int(input(
        "Que voulez-vous faire ? 1 = Tester les fonctionnalités de la classe, "
        "2 = Générer un mot dans une langue choisie, 3 = Prédire la langue d'un mot, 4 = Arrêter : "))

    while choice < 1 or choice > 4:
        choice = int(input("réponse incorrecte, réessayez : "))

print("Merci d'avoir utilisé notre programme !")


