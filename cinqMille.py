import random

# TODO
# Pas le droit de dépasser la cible
# Strikes
# Affichage
# Passer à 10 000

scores = []
dice = []
state = []
players = []
nb_players = 0
current_player = -1


def register_players():
    global players
    global nb_players
    global scores

    nb_players = ""
    while(not isinstance(nb_players, int) or nb_players < 1 or nb_players > 10):
        try:
            nb_players = int(input("Combien êtes-vous ? "))
        except:
            print("Veuillez entrer un nombre entier, entre 1 et 10.")
    
    scores = [0 for i in range(nb_players)]
    players = ["" for i in range(nb_players)]
    
    for i in range(nb_players):
        players[i] = input("j" + str(i) + ", comment t'appelles-tu ? ")



def check_quinte():
    global scores
    global dice
    global state
    global current_player

    if(state.count(0) > 4): # Check qu'il y a assez de dés
        if(dice.count(dice[0]) == 5): # Est-ce qu'on a le même chiffre 5 fois
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            if(dice[0] == 1):
                scores[current_player] += 4000
            else:
                scores[current_player] += dice[0] * 400
            print("Une quinte ! Ton score est maintenant de", scores[current_player])
            return 1
        else:
            print("Pas de quinte :(")
            return 0
    
    else:
        return 0



def check_suite():
    global scores
    global dice
    global state

    if(state.count(0) > 4): # Check qu'il y a assez de dés

        ok = 1
        for i in range(1, 5):
            if(dice[i] != dice[i-1] + 1):
                ok = 0
                
        if(ok):
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            scores[current_player] += 1500
            print("Une suite ! Ton score est maintenant de", scores[current_player])
            return 1
        else:
            print("Pas de suite :(")
            return 0
    
    else:
        return 0


def check_full():
    global scores
    global dice
    global state

    if(state.count(0) > 4): # Check qu'il y a assez de dés
        current_score = scores[current_player]
        nope = 0

        if(check_brelan(False)):
            others = [x for i, x in enumerate(dice) if state[i] == 0]
            if(others.count(others[0]) == 2):
                state = [1 for i in range(5)]
                scores[current_player] = current_score
                scores[current_player] += 1500
                print("Un full ! Ton score est maintenant de", scores[current_player])
                return 1
            else:
                nope = 1
        else:
            nope = 1
        
        if(nope):
            scores[current_player] = current_score
            state = [0 for i in range (5)]
            print("Pas de full :(")
            return 0
    
    else:
        return 0
        


def check_carre():
    global scores
    global dice
    global state

    if(state.count(0) > 3): # Check s'il y a encore au moins 4 dés
    
        if(dice.count(dice[0]) == 4 and state[:-1].count(0) == 4): # Les 4 premiers dés
            state[:-1] = [1 for i in range(4)]
            if(dice[0] == 1):
                scores[current_player] += 2000
            else:
                scores[current_player] += dice[0] * 200
            print("Un carré ! Ton score est maintenant de", scores[current_player])
            return 1

        elif(dice.count(dice[1]) == 4 and state[1:].count(0) == 4): # Les 4 derniers dés
            state[1:] = [1 for i in range(4)]
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            if(dice[0] == 1):
                scores[current_player] += 2000
            else:
                scores[current_player] += dice[0] * 200
            print("Un carré ! Ton score est maintenant de", scores[current_player])
            return 1

        else:
            print("Pas de carré :(")
            return 0
    
    else:
        return 0



def check_brelan(message):
    global scores
    global dice
    global state

    if(state.count(0) > 2): # Check s'il y a encore au moins 3 dés

        if(dice.count(dice[0]) == 3 and state[0:3].count(0) == 3):
            state[0:3] = [1 for i in range(3)]
            if(dice[0] == 1):
                scores[current_player] += 1000
            else:
                scores[current_player] += dice[0] * 100
            
            if(message):
                print("Un brelan ! Ton score est maintenant de", scores[current_player])
            return 1

        elif(dice.count(dice[1]) == 3 and state[1:4].count(0) == 3):
            state[1:4] = [1 for i in range(3)]
            if(dice[1] == 1):
                scores[current_player] += 1000
            else:
                scores[current_player] += dice[1] * 100

            if(message):
                print("Un brelan ! Ton score est maintenant de", scores[current_player])
            return 1
        
        elif(dice.count(dice[2]) == 3 and state[2:5].count(0) == 3):
            state[2:5] = [1 for i in range(3)]
            if(dice[2] == 1):
                scores[current_player] += 1000
            else:
                scores[current_player] += dice[2] * 100

            if(message):
                print("Un brelan ! Ton score est maintenant de", scores[current_player])
            return 1

        else:
            if(message):
                print("Pas de brelan :(")
            return 0
    
    else:
        return 0


def check_unique():
    global scores
    global dice
    global state

    if(state.count(0) > 0): # Check s'il y a encore au moins 1 dé
        score_temp = 0
        nb5 = 0

        for i in range(5):
            if(dice[i] == 5 and state[i] == 0):
                score_temp += 50
                print("Un 5 !")
                nb5 += 1
                state[i] = 1
            elif(dice[i] == 1 and state[i] == 0):
                score_temp += 100
                print("Un 1 !")
                state[i] = 1
        
        if(nb5 == 2): 
                fuse = input("Il y a deux 5, veux-tu qu'ils fusionnent pour former un 1 ? (0 pour non, 1 pour oui) : ")
                if(fuse == "1"):
                    for i in range(5):
                        if(state[i] == 1):
                            state[i] = 0
                            break
        
        if(score_temp != 0):
            scores[current_player] += score_temp
            print("Ton score est maintenant de", scores[current_player])
            return 1
        else:
            print("Pas de 1 ou de 5 :(")
            return 0
    
    else:
        return 0
            



def main():
    global scores
    global dice
    global state
    global nb_players
    global current_player
    global players

    register_players()

    while(scores[current_player] < 1000):
        keep_going = 1
        state = [0, 0, 0, 0, 0]
        current_player = (current_player + 1)%3
        current_score = scores[current_player]

        while(keep_going):
            _ = input(players[current_player] + " c'est ton tour, lance !")
            unsorted_dice = [(random.randrange(6) + 1) for i in range(5)]
            print("*roule roule roule...*\n")

            dice = unsorted_dice.copy()
            dice.sort()

            printed_dice = [dice[i] for i in range(5) if(state[i] == 0)]
            print(printed_dice, "\n")

            res = 0
            res += check_quinte()
            res += check_suite()
            res += check_full()
            res += check_carre()
            res += check_brelan(True)
            res += check_unique()

            if(not res):
                print("Aïe aïe aïe... Tu n'as rien obtenu. Ton score revient à", current_score, "\n")
                keep_going = 0
                scores[current_player] = current_score
            else:
                if(state.count(0) == 0):
                    state = [0 for i in range(5)]

                sentence = "\nIl te reste " + str(state.count(0)) + " dé(s)."
                
                if(scores[current_player]%100 != 0):
                    print("\nTon score finit par 50, tu ne peux pas t'arrêter. " + sentence + "\n")
                elif(scores[current_player] < 600):
                    print("Tu as moins de 600, tu n'as pas le droit de t'arrêter. " + sentence + "\n")
                else:
                    keep_going = input(sentence + " Continuer ? (0 pour non, 1 pour oui) : ")
                
                    if(keep_going == "1"):
                        print("Ok, on continue !\n")
                    else:
                        print("Ok ! Tour suivant.\n")
                        keep_going = 0
    
    print("Bravo ! Tu as atteint 1000 !")


main()