#include <stdio.h>
#include <time.h>
#include "liste.h"
#include <linux/time.h>

// void temps_moyen(struct timespec deb, struct timespec fin, int nb_elem) {
//     double temps_s = fin.tv_sec - deb.tv_sec;
//     double temps_ns = fin.tv_nsec - deb.tv_nsec;
//     temps_ns = temps_s * 1e9 + temps_ns;
//     double temps_moyen = temps_ns / nb_elem;
//     printf("temps moyens : %fns\n", temps_moyen);
// }

int main(void) {
    int nbEssais = 100;
    int tailleListeMax = 100;
    struct timespec tsDeb, tsFin;

    for (int tailleListe = 1; tailleListe < tailleListeMax; tailleListe++) {
        double tempsTotal = 0;
        for (int j = 0; j < nbEssais; j++) {
            liste l = NULL;
            for (int i = 0; i < tailleListe; i++) {
                l = ajouterEnTete(l, i);
            }
            clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &tsDeb);
            supprimerEnTete(l);
            clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &tsFin);
            double tempsS = (double) (tsFin.tv_sec - tsDeb.tv_sec);
            double tempsNs = (double) (tsFin.tv_nsec - tsDeb.tv_nsec);
            tempsTotal += tempsS * 1e9 + tempsNs;
            double tempsMoyen = tempsTotal / nbEssais;
            printf("%d\t%f\n", tailleListe, tempsMoyen);
        }
    } 
    

    return 0;

    struct timespec ts_deb, ts_fin;
    liste l = NULL;
    int n = 10000;

    // Ajouter en tete
    printf("Ajouter en tete 10000 fois;   ");
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_deb);
    for (int i=0; i<n; ++i) {
        l = ajouterEnTete(l, i);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_fin);
    temps_moyen(ts_deb, ts_fin, n);

    // Rechercher 9999
    printf("Rechercher 9999 10000 fois;   ");
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_deb);
    for (int i=0; i<n; ++i) {
        recherche(l, 9999);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_fin);
    temps_moyen(ts_deb, ts_fin, n);

    // Rechercher 0
    printf("Rechercher 0 10000 fois;      ");
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_deb);
    for (int i=0; i<n; ++i) {
        recherche(l, 0);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_fin);
    temps_moyen(ts_deb, ts_fin, n);

    // Supprimer en tete
    printf("Supprimer en tete 10000 fois; ");
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_deb);
    while (l != NULL) {
        l = supprimerEnTete(l);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts_fin);
    temps_moyen(ts_deb, ts_fin, n);

    return 0;
}