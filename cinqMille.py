import random

# TODO
# Strikes
# Reprise de score
# Si plus de 2000, grosse barre
# Coup de poing
# Affichage
# Passer à 10 000

scores = []
current_score_position = []
small_strikes = []
big_strikes = []
dice = []
state = []
players = []
nb_players = 0
current_player = 0
just_fell = 0


def register_players():
    global scores
    global players
    global nb_players

    nb_players = ""
    while(not isinstance(nb_players, int) or nb_players < 1 or nb_players > 10):
        try:
            nb_players = int(input("Combien êtes-vous ? "))
        except:
            print("Veuillez entrer un nombre entier, entre 1 et 10.")
    
    scores = [[0] for i in range(nb_players)]
    current_score_position = [0 for i in range(nb_players)]
    small_strikes = [[0] for i in range(nb_players)]
    big_strikes = [[0] for i in range(nb_players)]
    players = ["" for i in range(nb_players)]
    
    for i in range(nb_players):
        players[i] = input("j" + str(i) + ", comment t'appelles-tu ? ")


def check_big_strikes():
    for i in range(1, len(scores[current_player])-2):
        if(big_strikes[current_player][i-1] and big_strikes[current_player][i] and big_strikes[current_player][i+1]):
            return 1
    return 0


def check_strikes(first_throw):
    global scores
    global current_score_position
    global small_strikes
    global big_strikes
    global current_player
    global just_fell

    if(len(scores[current_player]) != 1):
        small_strikes[current_player][current_score_position] += 1

        if(small_strikes[current_player][current_score_position] == 3 or first_throw):
            if(first_throw):
                print("Rien du 1er coup ! Tu gagnes une grande barre et retombes d'un palier.")
            else:
                print("Mais... C'est ta 3e petite barre ! Elle se transforme en grande barre, et tu perds un palier.")

            big_strikes[current_player][current_score_position] += 1
        
            if(check_big_strikes()):
                print("Oh non ! C'est ta troisième grande barre ! Ce sont les règles, tu retombes à 0.\n")
                scores[current_player] = [0]
                small_strikes[current_player] = [0]
                big_strikes[current_player] = [0]
            elif(just_fell):
                print("Oh non ! Tu venais déjà de tomber, et maintenant tu gagnes une grosse barre.\n")
                big_strikes[current_player][current_score_position] = 1
            else:
                del scores[current_player][-1]
                del small_strikes[current_player][-1]
                just_fell = 1
                print("Ton score revient à", scores[current_player][-1], "\n")
        else:
            print("Aïe aïe aïe... Tu n'as rien obtenu. Tu gagnes une petite barre et ton score revient à", scores[current_player][-1])
    else:
        if(first_throw):
            players[current_player] = input("Rien du 1er coup, alors que tu as 0 ? C'est pas de chance ! Tes camarades peuvent choisir un nouveau nom pour toi : ")
        else:
            print("Aïe aïe aïe... Tu n'as rien obtenu.\n")


def insert_score():
    global scores
    global current_score
    global current_score_position
    global current_player
    global small_strikes
    global big_strikes

    i = 1
    while(i < len(scores[current_player]) and scores[current_player][i] <= current_score):
        i += 1
    current_score_position = i

    scores[current_player].insert(current_score_position, current_score)
    small_strikes[current_player].insert(current_score_position, 0)
    big_strikes[current_player].insert(current_score_position, 0)
    

    




def check_quinte():
    global current_score
    global dice
    global state
    global current_player

    if(state.count(0) > 4): # Check qu'il y a assez de dés
        if(dice.count(dice[0]) == 5): # Est-ce qu'on a le même chiffre 5 fois
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            if(dice[0] == 1):
                current_score += 4000
            else:
                current_score += dice[0] * 400
            print("Une quinte ! Ton score est maintenant de", current_score)
            return 1
        else:
            print("Pas de quinte :(")
            return 0
    
    else:
        return 0



def check_suite():
    global current_score
    global dice
    global state
    global current_player

    if(state.count(0) > 4): # Check qu'il y a assez de dés

        ok = 1
        for i in range(1, 5):
            if(dice[i] != dice[i-1] + 1):
                ok = 0
                
        if(ok):
            state = [1 for i in range (5)] # Tous les dés ont été utilisés
            current_score += 1500
            print("Une suite ! Ton score est maintenant de", current_score)
            return 1
        else:
            print("Pas de suite :(")
            return 0
    
    else:
        return 0


def check_full():
    global current_score
    global dice
    global state
    global current_player

    entry_score = current_score

    if(state.count(0) > 4): # Check qu'il y a assez de dés
        nope = 0

        if(check_brelan(False)):
            others = [x for i, x in enumerate(dice) if state[i] == 0]
            if(others.count(others[0]) == 2):
                state = [1 for i in range(5)]
                current_score = entry_score
                current_score += 1500
                print("Un full ! Ton score est maintenant de", current_score)
                return 1
            else:
                nope = 1
        else:
            nope = 1
        
        if(nope):
            current_score = entry_score
            state = [0 for i in range (5)]
            print("Pas de full :(")
            return 0
    
    else:
        return 0
        


def check_carre():
    global current_score
    global dice
    global state
    global current_player

    if(state.count(0) > 3): # Check s'il y a encore au moins 4 dés
    
        if(dice[:-1].count(dice[0]) == 4 and state[:-1].count(0) == 4): # Les 4 premiers dés
            state[:-1] = [1 for i in range(4)]
            if(dice[0] == 1):
                current_score += 2000
            else:
                current_score += dice[0] * 200
            print("Un carré ! Ton score est maintenant de", current_score)
            return 1

        elif(dice[1:].count(dice[1]) == 4 and state[1:].count(0) == 4): # Les 4 derniers dés
            state[1:] = [1 for i in range(4)]
            if(dice[1] == 1):
                current_score += 2000
            else:
                current_score += dice[0] * 200
            print("Un carré ! Ton score est maintenant de", current_score)
            return 1

        else:
            print("Pas de carré :(")
            return 0
    
    else:
        return 0



def check_brelan(message):
    global current_score
    global dice
    global state
    global current_player

    if(state.count(0) > 2): # Check s'il y a encore au moins 3 dés

        if(dice[0:3].count(dice[0]) == 3 and state[0:3].count(0) == 3):
            state[0:3] = [1 for i in range(3)]
            if(dice[0] == 1):
                current_score += 1000
            else:
                current_score += dice[0] * 100
            
            if(message):
                print("Un brelan ! Ton score est maintenant de", current_score)
            return 1

        elif(dice[1:4].count(dice[1]) == 3 and state[1:4].count(0) == 3):
            state[1:4] = [1 for i in range(3)]
            if(dice[1] == 1):
                current_score += 1000
            else:
                current_score += dice[1] * 100

            if(message):
                print("Un brelan ! Ton score est maintenant de", current_score)
            return 1
        
        elif(dice[2:5].count(dice[2]) == 3 and state[2:5].count(0) == 3):
            state[2:5] = [1 for i in range(3)]
            if(dice[2] == 1):
                current_score += 1000
            else:
                current_score += dice[2] * 100

            if(message):
                print("Un brelan ! Ton score est maintenant de", current_score)
            return 1

        else:
            if(message):
                print("Pas de brelan :(")
            return 0
    
    else:
        return 0


def check_unique():
    global current_score
    global dice
    global state
    global current_player

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
            current_score += score_temp
            print("Ton score est maintenant de",current_score)
            return 1
        else:
            print("Pas de 1 ou de 5 :(")
            return 0
    
    else:
        return 0
            



def main():
    global scores
    global current_score
    global current_score_position
    global dice
    global state
    global nb_players
    global current_player
    global players
    global just_fell

    register_players()
    current_player = nb_players-1

    while(scores[current_player][current_score_position[current_player]] < 1000):
        keep_going = 1
        state = [0, 0, 0, 0, 0]
        current_player = (current_player + 1)%nb_players
        current_score = scores[current_player][current_score_position[current_player]]
        first_throw = 1

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

            if(not res or scores[current_player][-1] > 1000):
                keep_going = 0
                check_strikes()
            else:
                if(state.count(0) == 0):
                    state = [0 for i in range(5)]

                sentence = "\nIl te reste " + str(state.count(0)) + " dé(s)."
                
                if(current_score%100 != 0):
                    print("\nTon score finit par 50, tu ne peux pas t'arrêter. " + sentence + "\n")
                elif(current_score < 600):
                    print("Tu as moins de 600, tu ne peux pas t'arrêter. " + sentence + "\n")
                elif(state.count(0) == 5):
                    print(sentence + " C'est une main pleine, tu ne peux pas t'arrêter.\n")
                else:
                    just_fell = 0
                    keep_going = input(sentence + " Continuer ? (0 pour non, 1 pour oui) : ")
                
                    if(keep_going == "1"):
                        print("Ok, on continue !\n")
                    else:
                        print("Ok ! Tour suivant.\n")
                        insert_score()
                        keep_going = 0
            
            first_throw = 0
    
    print("Bravo ! Tu as atteint 1000 !")


main()