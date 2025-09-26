#include <stdlib.h>
#include "liste.h"

liste ajouterEnTete(liste l, int x) {
    struct maillon* p_tete = malloc(sizeof(struct maillon));
    p_tete->val = x;
    p_tete->suivant = l;
    return p_tete;
}

liste supprimerEnTete(liste l) {
    liste next = l->suivant;
    free(l);
    return next;
}

void supprimerListe(liste l) {
    while (l!= NULL)
        l = supprimerEnTete(l);
}

liste recherche(liste l, int val) {
    if (l == NULL) {
        return NULL;
    }
    if (l->val == val) {
        return l;
    }
    else {
        return recherche(l->suivant, val);
    }
}

int longueur(liste l) {
    if (l == NULL) {
        return 0;
    }
    return longueur(l->suivant) + 1;
}