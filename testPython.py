
def afficher_info_personne(nomP, ageP):
    print("vous vous appelez " + nomP + " et vous avez " + str(ageP) + " ans, l'annee prochaine vous aurez " + str(
        ageP + 1) + " ans")


    if ageP == 17:
        print("vous etes presque majeur")
    elif 12 <= ageP <18:
        print("vous etes adolessant")
    elif ageP ==1 or ageP == 2:
        print("vous etes un bebe")
    elif ageP < 10:
        print("vous etes enfant")
    elif ageP == 18:
        print("vous etes tout juste majeur")
    elif ageP > 60:
        print("vous etes senior")
    elif ageP > 18:
        print("vous etes majeur")
    else:
        print("vous etes mineur")


def demander_nom():
    reponse_nom = ""
    while reponse_nom == "":
        reponse_nom = input("Quel est ton nom ?")
    return  reponse_nom


def demander_age(nom_personne):
    age_int = 0
    while age_int == 0:
        age_str = input(nom_personne + " quel est votre age ?")
        try:
            age_int = int(age_str)

        except:
            print("ERREUR: vous devez rentrer un nombre pour l'age")
    return age_int


#nom1 = demander_nom()
#nom2 = demander_nom()
#age1 = demander_age(nom1)
#age2 = demander_age(nom2)
#afficher_info_personne(nom1, age1)
#afficher_info_personne(nom2, age2)

for i in range(0, 3):
    nom = "personne" + str(i+1)
    age = demander_age(nom)
    afficher_info_personne(nom, age)




