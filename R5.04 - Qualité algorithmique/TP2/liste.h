#ifndef LISTE_H
#define LISTE_H

/**
BUT3 Info Orleans R504 - fichier d'en-tête pour les listes chainées
*/

/**
Un maillon contient une valeur entière et un pointer vers un autre maillon
*/
struct maillon {
    int val;
    struct maillon *suivant;
};

typedef struct maillon* liste ;

// liste creerListe();
void supprimerListe(liste l);
liste ajouterEnTete(liste l, int x);
// void inserer(liste l, int val, int i);
liste supprimerEnTete(liste l);
// int supprimer(liste l, int i);
// void afficherListe(liste l);
int longueur(liste l);
liste recherche(liste l, int val);

#endif
