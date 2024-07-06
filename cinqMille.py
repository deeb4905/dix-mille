import random

# TODO
# Pas le droit de dépasser la cible
# Sortir à 650
# Strikes
# 2 joueurs
# Affichage
# Passer à 10 000

score = 0
dice = []
state = []



def check_quinte():
    global score
    global dice
    global state

    if(state.count(0) > 4): # Check qu'il y a assez de dés
        if(dice.count(dice[0]) == 5): # Est-ce qu'on a le même chiffre 5 fois
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            if(dice[0] == 1):
                score += 4000
            else:
                score += dice[0] * 400
            print("Une quinte ! Ton score est maintenant de", score)
            return 1
        else:
            print("Pas de quinte :(")
            return 0
    
    else:
        return 0



def check_suite():
    global score
    global dice
    global state

    if(state.count(0) > 4): # Check qu'il y a assez de dés

        ok = 1
        for i in range(1, 5):
            if(dice[i] != dice[i-1] + 1):
                ok = 0
                
        if(ok):
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            score += 1500
            print("Une suite ! Ton score est maintenant de", score)
            return 1
        else:
            print("Pas de suite :(")
            return 0
    
    else:
        return 0


def check_full():
    global score
    global dice
    global state

    if(state.count(0) > 4): # Check qu'il y a assez de dés
        current_score = score

        if(check_brelan(False)):
            others = [x for i, x in enumerate(dice) if state[i] == 0]
            if(others.count(others[0]) == 2):
                state = [1 for i in range(5)]
                score = current_score
                score += 1500
                print("Un full ! Ton score est maintenant de", score)
                return 1
        else:
            score = current_score
            state = [0 for i in range (5)]
            print("Pas de full :(")
            return 0
    
    else:
        return 0
        


def check_carre():
    global score
    global dice
    global state

    if(state.count(0) > 3): # Check s'il y a encore au moins 4 dés
    
        if(dice.count(dice[0]) == 4 and state[:-1].count(0) == 4): # Les 4 premiers dés
            state[:-1] = [1 for i in range(4)]
            if(dice[0] == 1):
                score += 2000
            else:
                score += dice[0] * 200
            print("Un carré ! Ton score est maintenant de", score)
            return 1

        elif(dice.count(dice[1]) == 4 and state[1:].count(0) == 4): # Les 4 derniers dés
            state[1:] = [1 for i in range(4)]
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            if(dice[0] == 1):
                score += 2000
            else:
                score += dice[0] * 200
            print("Un carré ! Ton score est maintenant de", score)
            return 1

        else:
            print("Pas de carré :(")
            return 0
    
    else:
        return 0



def check_brelan(message):
    global score
    global dice
    global state

    if(state.count(0) > 2): # Check s'il y a encore au moins 3 dés

        if(dice.count(dice[0]) == 3 and state[0:3].count(0) == 3):
            state[0:3] = [1 for i in range(3)]
            if(dice[0] == 1):
                score += 1000
            else:
                score += dice[0] * 100
            
            if(message):
                print("Un brelan ! Ton score est maintenant de", score)
            return 1

        elif(dice.count(dice[1]) == 3 and state[1:4].count(0) == 3):
            state[1:4] = [1 for i in range(3)]
            if(dice[1] == 1):
                score += 1000
            else:
                score += dice[1] * 100

            if(message):
                print("Un brelan ! Ton score est maintenant de", score)
            return 1
        
        elif(dice.count(dice[2]) == 3 and state[2:5].count(0) == 3):
            state[2:5] = [1 for i in range(3)]
            if(dice[2] == 1):
                score += 1000
            else:
                score += dice[2] * 100

            if(message):
                print("Un brelan ! Ton score est maintenant de", score)
            return 1

        else:
            if(message):
                print("Pas de brelan :(")
            return 0
    
    else:
        return 0


def check_unique():
    global score
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
            score += score_temp
            print("Ton score est maintenant de", score)
            return 1
        else:
            print("Pas de 1 ou de 5 :(")
            return 0
    
    else:
        return 0
            



def main():
    global score
    global dice
    global state

    while(score < 1000):
        keep_going = 1
        state = [0, 0, 0, 0, 0]
        current_score = score

        while(keep_going):
            _ = input("Lance !")
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
                print("Aïe aïe aïe... Tu n'as rien obtenu. Ton score revient à", current_score)
                keep_going = 0
                score = current_score
            else:
                if(state.count(0) == 0):
                    state = [0 for i in range(5)]

                sentence = "\nIl te reste " + str(state.count(0)) + " dé(s)."
                
                if(score%100 != 0):
                    print("\nTon score finit par 50, tu ne peux pas t'arrêter. " + sentence + "\n")
                elif(score < 600):
                    print("Tu as moins de 600, tu n'as pas le droit de t'arrêter. " + sentence + "\n")
                else:
                    keep_going = input(sentence + " Continuer ? (0 pour non, 1 pour oui) : ")
                
                    if(keep_going == "1"):
                        print("Ok, on continue !\n")
                    else:
                        print("Ok ! Tour suivant, on recommence avec 5 dés.\n")
                        keep_going = 0
    
    print("Bravo ! Tu as atteint 1000 !")


main()