import random

scores = []
current_score_position = []
small_strikes = []
big_strikes = []
dice = []
state = []
players = []
nb_players = 0
current_player = 0
current_score = 0
just_fell = []
punch = []


def register_players():
    global scores
    global current_score_position
    global small_strikes
    global big_strikes
    global players
    global nb_players
    global just_fell
    global punch

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
    just_fell = [0 for i in range(nb_players)]
    punch = [1 for i in range(nb_players)]
    
    for i in range(nb_players):
        players[i] = input("j" + str(i) + ", comment t'appelles-tu ? ")

def display_scores():
    global scores
    global current_player

    score_component = ""
    strikes_component = ""

    print("Ta liste de scores actuelle :\n")

    for i in range(len(scores[current_player])):
        score_component = scores[current_player][i]

        if(small_strikes[current_player][i] == 3):
            strikes_component = "  X  "
        else:
            for j in range(small_strikes[current_player][i]):
                strikes_component += '|'
            strikes_component += "  "
        print(strikes_component, score_component)

        score_component = ""
        strikes_component = "     "
        



def check_duplicates():
    global scores
    global current_score
    global players
    global current_player
    global current_score_position
    global small_strikes
    global big_strikes

    for player in range(len(players)):
        if player != current_player:
            for i in range(len(scores[player])):
                if(scores[player][i] == current_score and big_strikes[player][i] == 0):
                    print("Mais... " + players[player] + " avait déjà eu ce score ! Désolé " + players[player] + ", tu gagnes une grande barre.")

                    actual_current_player = current_player
                    current_player = player

                    remove_score(i)

                    current_player = actual_current_player
                    
                    break


def check_big_strikes():
    global scores
    global current_player
    global big_strikes

    for i in range(1, len(scores[current_player])-1):
        if(big_strikes[current_player][i-1] and big_strikes[current_player][i] and big_strikes[current_player][i+1]):
            print("Oh non ! Tu as trois grandes barres d'afilée ! Ce sont les règles, tes scores précédents sont barrés.\n")
            scores[current_player] = scores[current_player][i+2:]
            if scores[current_player] == []:
                scores[current_player] = [0]
                small_strikes[current_player] = [0]
                big_strikes[current_player] = [0]
            else:
                small_strikes[current_player] = small_strikes[current_player][i+2:]
                big_strikes[current_player] = big_strikes[current_player][i+2:]

        return 1
    return 0

def check_strikes(first_throw):
    global scores
    global current_score
    global current_score_position
    global small_strikes
    global big_strikes
    global current_player
    global just_fell

    if(current_score_position[current_player] != 0):
        small_strikes[current_player][current_score_position[current_player]] += 1

        if(small_strikes[current_player][current_score_position[current_player]] == 3 or first_throw or just_fell[current_player] or current_score - scores[current_player][current_score_position[current_player]] > 1999):
            if(first_throw):
                print("Rien du 1er coup ! Tu gagnes une grande barre.\n")
            elif(just_fell[current_player]):
                print("Oh non ! Tu venais déjà de tomber, tu gagnes une grande barre.\n")
            elif(current_score - scores[current_player][current_score_position[current_player]] > 1999):
                print("Oh non ! Tu as échoué au dessus de 2000 points, tu gagnes une grande barre.\n")
            else:
                print("Oh non ! C'est ta troisième petite barre, tu gagnes une grande barre.\n")

            small_strikes[current_player][current_score_position[current_player]] = 3
            big_strikes[current_player][current_score_position[current_player]] += 1
        
            if(not check_big_strikes()):
                remove_score(current_score_position[current_player])
                just_fell[current_player] = 1
                print("Ton score revient à", scores[current_player][current_score_position[current_player]], "\n")
        else:
            print("Aïe aïe aïe... Tu n'as rien obtenu. Tu gagnes une petite barre et ton score revient à", scores[current_player][current_score_position[current_player]])
    else:
        if(first_throw):
            players[current_player] = input("Rien du 1er coup, alors que tu as 0 ? C'est pas de chance ! Tes camarades peuvent choisir un nouveau nom pour toi : ")
        else:
            print("Aïe aïe aïe... Tu n'as rien obtenu.\n")


def remove_score(indice :int) -> None: #bisous
    global current_score_position
    global current_player
    global big_strikes
    global small_strikes
    global players

    big_strikes[current_player][indice] = 1
    small_strikes[current_player][indice] = 3
    
    if not check_big_strikes():
        if indice == current_score_position[current_player]:
            while big_strikes[current_player][indice] == 1:
                indice -= 1
            current_score_position[current_player] = indice

    '''
    i = current_score_position[current_player]-1
    while(big_strikes[current_player][i] != 0):
        i -= 1
    current_score_position[current_player] = i
    '''


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
            print("Une quinte !")
            return 1
        else:
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
            print("Une suite !")
            return 1
        else:
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
                print("Un full !")
                return 1
            else:
                nope = 1
        else:
            nope = 1
        
        if(nope):
            current_score = entry_score
            state = [0 for i in range (5)]
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
            print("Un carré !")
            return 1

        elif(dice[1:].count(dice[1]) == 4 and state[1:].count(0) == 4): # Les 4 derniers dés
            state[1:] = [1 for i in range(4)]
            if(dice[1] == 1):
                current_score += 2000
            else:
                current_score += dice[1] * 200
            print("Un carré !")
            return 1

        else:
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
                print("Un brelan !")
            return 1

        elif(dice[1:4].count(dice[1]) == 3 and state[1:4].count(0) == 3):
            state[1:4] = [1 for i in range(3)]
            if(dice[1] == 1):
                current_score += 1000
            else:
                current_score += dice[1] * 100

            if(message):
                print("Un brelan !")
            return 1
        
        elif(dice[2:5].count(dice[2]) == 3 and state[2:5].count(0) == 3):
            state[2:5] = [1 for i in range(3)]
            if(dice[2] == 1):
                current_score += 1000
            else:
                current_score += dice[2] * 100

            if(message):
                print("Un brelan !")
            return 1

        else:
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
            return 1
        else:
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
    global punch

    register_players()

    end_game = 0
    res = 1
    current_player = nb_players-1
    pick_up_score = 0

    while(not end_game):
        keep_going = 1
        first_throw = 1
        current_player = (current_player + 1)%nb_players

        if(pick_up_score != 0):
            pick_up = input(players[current_player] + ", veux tu récupérer " + str(pick_up_score) + " avec " + str(state.count(0)) + " dé(s) ? (0 pour non, 1 pour oui) : ")
            if(pick_up == "1"):
                current_score = scores[current_player][current_score_position[current_player]] + pick_up_score
            else:
                state = [0, 0, 0, 0, 0]
                current_score = scores[current_player][current_score_position[current_player]]
        else:
            state = [0, 0, 0, 0, 0]
            current_score = scores[current_player][current_score_position[current_player]]

        display_scores()

        while(keep_going):
            _ = input(players[current_player] + " c'est ton tour, lance !")
            unsorted_dice = [(random.randrange(6) + 1) for i in range(5)]
            random.shuffle(state)
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

            if(not res or current_score > 10000):
                if(punch[current_player]):
                    use_punch = input("Aucun point ! Veux-tu utiliser ton coup de poing ? (0 pour non, 1 pour oui) : ")
                    if(use_punch == "1"):
                        print("*BANG*\n")
                        punch[current_player] = 0
                    else:
                        pick_up_score = 0
                        keep_going = 0
                        check_strikes(first_throw)
                else:
                    pick_up_score = 0
                    keep_going = 0
                    check_strikes(first_throw)

            else:
                print(f'Ton score est de {current_score - scores[current_player][current_score_position[current_player]]} pour ce lancer. Le total est {current_score}')
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
                    keep_going = input(sentence + " Continuer ? (0 pour non, 1 pour oui) : ")
                
                    if(keep_going == "1"):
                        print("Ok, on continue !\n")
                    else:
                        print("Ok ! Tour suivant.\n")
                        pick_up_score = current_score - scores[current_player][current_score_position[current_player]]
                        
                        scores[current_player].append(current_score)
                        current_score_position[current_player] += 1
                        small_strikes[current_player].append(0)
                        big_strikes[current_player].append(0)
                        
                        check_duplicates()
                        keep_going = 0
                        just_fell[current_player] = 0

                        end_game = scores[current_player][current_score_position[current_player]] == 10000
            
            first_throw = 0
    
    print("Bravo ! Tu as atteint 10000 !")


main()