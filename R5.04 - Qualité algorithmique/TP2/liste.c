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

// liste recherche(liste elem, int val) {
//     if (elem == NULL) {
//         return NULL;
//     }
//     if (elem->val == val) {
//         return elem;
//     }
//     else {
//         return recherche(elem->next, val);
//     }
// }

int longueur(liste l) {
    if (l == NULL) {
        return 0;
    }
    return longueur(l->suivant) + 1;
}

// void print_maillon(liste elem) {
//     printf("[");
//     while (elem != NULL) {
//         printf("%d, ", elem->val);
//         elem = elem->next;
//     }
//     printf("]\n");
// }