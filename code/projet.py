###########################
# Fichier projet.py       #
# 16/05/18                #
# La communauté de l'info #
###########################

from classe import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import random


def chaine_to_tuple(mot):
    w = ()
    for i in range(len(mot)):
        w += (HMM.lettre_to_num(mot[i]),)
    return w


def text_to_list(adr):  # transforme un document texte contenant des mot en liste de mots compréhensibles par le HMM
    """
    :param adr: addresse du fichier texte à convertir
    :return: liste de tuples correspondant aux mots se trouvant dans le fichier texte
    """
    data = open(adr, 'r')
    texte = data.read()
    L = texte.split('\n')
    data.close()
    L2 = []
    for w in L:
        L2 += [chaine_to_tuple(w)]
    return L2[:-1]


def xval(nbFolds, S, nbL, nbSMin, nbSMax, nbIter, nbInit):
    n = len(S)
    l = np.random.permutation(n)
    lvOpt = -float("inf")
    for nbS in range(nbSMin, nbSMax + 1):
        lv = 0
        for i in range(1, nbFolds + 1):
            f1 = int((i - 1) * n / nbFolds)
            f2 = int(i * n / nbFolds)
            learn = [S[l[j]] for j in range(f1)]
            learn += [S[l[j]] for j in range(f2, n)]
            test = [S[l[j]] for j in range(f1, f2)]
            h = HMM.bw3(nbS, nbL, learn, nbIter, nbInit)
            lv += h.logV(test)
        if lv > lvOpt:
            lvOpt = lv
            nbSOpt = nbS
    return lvOpt, nbSOpt


def func(x, a, b, c):  # fonction utilisée pour le fitting de certaines courbes
    return - a * np.exp(-x / b) - 25580 + c


def logV_vs_nb_iteration_bw1(nb_iter_max, nbS, S,
                             nbL=26):  # trace la log vraisemblance en fonction du nombre d'itération de bw1
    """
    :param nb_iter_max: nombre d'itérations de bw1 à réaliser
    :param nbS: nb d'états
    :param S: liste de mots sur laquelle on entraine notre HMM
    :param nbL: nombre de lettres
    """

    hmm = HMM.gen_HMM(nbL, nbS)
    nb_iter = [0]
    logV = [hmm.logV(S)]
    for i in range(1, nb_iter_max + 1):
        try:
            hmm.bw1(S)
            nb_iter.append(i)
            logV.append(hmm.logV(S))
        except KeyboardInterrupt:
            break
    plt.plot(nb_iter, logV, '.', c='blue', label='logV en fonction du nombre d\'itération de bw1')
    plt.xlabel('nb d\'iteration')
    plt.ylabel('logV')
    titre = 'anglais2000' + ' / nombre d\'etat = ' + str(nbS)
    plt.title(titre)
    optimizedParameters, pcov = opt.curve_fit(func, nb_iter, logV)

    # Use the optimized parameters to plot the best fit
    plt.plot(nb_iter,
             [func(x, optimizedParameters[0], optimizedParameters[1], optimizedParameters[2]) for x in nb_iter],
             label='-' + str(optimizedParameters[0]) + 'exp(-x/' + str(optimizedParameters[1]) + ') + ' + str(
                 -25580 + optimizedParameters[2]))

    plt.legend()
    plt.show()


def logV_vs_intialisation(nb_init_max, nb_iter, nbS, S,
                          nbL=26):  # trace la logvraisemblance optimale en fonction de différentes initialisations
    """
    :param nb_init_max: nombre d'initialisations différentes à réaliser
    :param nb_iter: nombre d'itération dans bw2
    :param nbS: nombre d'états
    :param S: liste de mots sur laquelle on entraine nos HMM
    :param nbL: nombre de lettres
    """

    nb_init = []
    logV = []
    for i in range(1, nb_init_max + 1):
        print("init", i)
        try:
            h = HMM.bw2(nbS, nbL, S, nb_iter)
            nb_init.append(i)
            logV.append(h.logV(S))
            print("###################################")
            print(logV[-1])
            print("###################################")
        except KeyboardInterrupt:
            break
    plt.plot(nb_init, logV)
    plt.show()


def logV_vs_initialisation_variante(nb_init_max, limite, nbS, S,
                                    nbL=26):  # trace la logvraisemblance optimale en fonction de différentes initialisations
    """
    :param nb_init_max: nombre d'initialisations différentes à réaliser
    :param limite: limite pour bw2_variante
    :param nbS: nombre d'états
    :param S: liste de mots sur laquelle on entraine nos HMM
    :param nbL: nombre de lettres
    """

    nb_init = []
    logV = []
    for i in range(1, nb_init_max + 1):
        try:
            h = HMM.bw2_variante(nbS, nbL, S, limite)
            nb_init.append(i)
            logV.append(h.logV(S))
        except KeyboardInterrupt:
            break
    plt.plot(nb_init, logV)
    plt.show()


def efficiency_vs_nb_state(nbFolds, S, nbSMin, nbSMax, nbIter, nbInit,
                           nbL=26):  # trace la log vraisemblance moyenne sur les echantillons tests en fonction du nombre d'état
    """
    :param nbFolds: cardinal de la partition de S
    :param S: liste de mots sur laquelle on entraine notre HMM
    :param nbSMin: nombre d'etat minimum
    :param nbSMax: nombre d'etat maximum
    :param nbIter: nombre d'itérations pour bw3
    :param nbInit: nbombre d'initialisations pour bw3
    :param nbL: nombre de lettres pour le HMM
    """

    n = len(S)
    l = np.random.permutation(n)
    nb_state = []
    logV = []
    for nbS in range(nbSMin, nbSMax + 1):
        try:
            lv = 0
            for i in range(1, nbFolds + 1):
                f1 = int((i - 1) * n / nbFolds)
                f2 = int(i * n / nbFolds)
                learn = [S[l[j]] for j in range(f1)]
                learn += [S[l[j]] for j in range(f2, n)]
                test = [S[l[j]] for j in range(f1, f2)]
                h = HMM.bw3(nbS, nbL, learn, nbIter, nbInit)
                lv += h.logV(test)
            logV.append(lv / nbFolds)
            nb_state.append(nbS)
        except KeyboardInterrupt:
            break
    plt.plot(nb_state, logV)
    plt.show()


def efficiency_vs_nb_state_variante(nbFolds, S, nbSMin, nbSMax, limite, nbInit,
                                    nbL=26):  # trace la log vraisemblance moyenne sur les echantillons tests en fonction du nombre d'état
    """
    :param nbFolds: cardinal de la partition de S
    :param S: liste de mots sur laquelle on entraine notre HMM
    :param nbSMin: nombre d'etat minimum
    :param nbSMax: nombre d'etat maximum
    :param limite: limite pour bw3_variante
    :param nbInit: nbombre d'initialisations pour bw3
    :param nbL: nombre de lettres pour le HMM
    """

    n = len(S)
    l = np.random.permutation(n)
    nb_state = []
    logV = []
    for nbS in range(nbSMin, nbSMax + 1):
        try:
            lv = 0
            for i in range(1, nbFolds + 1):
                f1 = int((i - 1) * n / nbFolds)
                f2 = int(i * n / nbFolds)
                learn = [S[l[j]] for j in range(f1)]
                learn += [S[l[j]] for j in range(f2, n)]
                test = [S[l[j]] for j in range(f1, f2)]
                h = HMM.bw3_variante(nbS, nbL, learn, nbInit, limite)
                lv += h.logV(test)
            logV.append(lv / nbFolds)
            nb_state.append(nbS)
        except KeyboardInterrupt:
            break
    plt.plot(nb_state, logV)
    plt.show()


def reconnaitre_langue(w):
    """
    :param w: mot dont la langue doit être reconnue
    :return: haine de caractère correspondant à la langue la plus probable
    """
    mot = chaine_to_tuple(w)
    langues = ['anglais', 'allemand', 'espagnol', 'neerlandais', 'suedois', 'elfique']
    anglais = HMM.load('hmm_anglais_parfait')
    allemand = HMM.load('hmm_allemand')
    espagnol = HMM.load('hmm_espagnol')
    neerlandais = HMM.load('hmm_neerlandais')
    suedois = HMM.load('hmm_suedois')
    elfique = HMM.load('hmm_elfique')
    proba = np.array(
        [anglais.logV([mot]), allemand.logV([mot]), espagnol.logV([mot]), neerlandais.logV([mot]), suedois.logV([mot]),
         elfique.logV([mot])])
    langue = langues[np.argmax(proba)]
    return langue


def afficher_mots_anglais(n):
    """
    :param n: nombre de mots anglais à générer puis à afficher
    """
    h = HMM.load("hmm_anglais_parfait")
    for i in range(n):
        n = random.randint(3, 8)
        print(h.gen_mot_lettres(n))


# L = text_to_list('anglais2000')
# print('toc', xval(20, L, 26, 2, 10, 5, 5))

# logV_vs_nb_iteration_bw1(1000, 30, text_to_list('anglais2000'))


# efficiency_vs_nb_state(10, text_to_list('anglais2000'), 53, 1000, 100, 1)

# efficiency_vs_nb_state(10, text_to_list('allemand2000'), 2, 1000, 100, 1)


# logV_vs_nb_iteration_bw1(1000, 45, text_to_list('anglais2000'))



# HMM.bw3(45, 26, text_to_list('espagnol2000'), 55, 12).save("hmm_espagnol")
# HMM.bw3(45, 26, text_to_list('suedois2000'), 55, 12).save("hmm_suedois")
# HMM.bw3(45, 26, text_to_list('neerlandais2000'), 55, 12).save("hmm_neerlandais")
# HMM.bw3(45, 26, text_to_list('neerlandais2000'), 55, 12).save("hmm_neerlandais")
# HMM.bw3(45, 26, text_to_list('elfique'), 55, 12).save("hmm_elfique")
# HMM.bw3(100, 26, text_to_list('anglais2000'), 55, 15).save("hmm_anglais_v2")
# HMM.bw3(100, 26, text_to_list('allemand2000'), 55, 15).save("hmm_allemand_v2")
# HMM.bw3(100, 26, text_to_list('suedois2000'), 55, 15).save("hmm_suedois_v2")
# HMM.bw3(100, 26, text_to_list('neerlandais2000'), 55, 15).save("hmm_neerlandais_v2")

# HMM.bw3(45, 26, text_to_list('anglais2000'), 200, 20).save("hmm_anglais_parfait")

# logV_vs_intialisation(100, 400, 45, text_to_list('anglais2000'))

