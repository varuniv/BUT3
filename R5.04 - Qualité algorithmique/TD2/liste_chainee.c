#include <stdio.h>

struct maillon {
    int val;
    struct maillon *suivant;
};

typedef struct maillon* liste;

int longeur(liste l){
    if (l == NULL){
        return 0;
    }else {
        return longeur(l->suivant) +1; 
    }
}

void affiche(liste l){

    printf("[ ");
    struct maillon * courant = l;
    while (courant != NULL) {
        printf("%d, ", courant-> val);
        courant = courant->suivant;
    }
    printf("]");
}

void insere_en_tete(liste l, int v){
    struct maillon * p_tete = malloc(sizeof(struct maillon));
    p_tete->val = v;
    p_tete->suivant = l;
    return p_tete;

    
} 
struct maillon* recherche(liste l,int x){
    if(l==NULL){
        return NULL;
    }
    if (l->val == x){
        return l;
    }else{
        return recherche(l-> suivant, x);
    }
}

int main() {
    liste liste_vide = NULL;
    struct maillon depart = {0,NULL};
    liste  liste_un_elt = &depart;
    struct maillon m3 = {3,NULL};
    struct maillon m7 = {7,NULL};
    m3.suivant = &m7;
    liste liste_deux_elt = &m3;
}