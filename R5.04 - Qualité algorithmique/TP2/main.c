#include "liste.h"
#include <stdio.h>
#include <time.h>

int main(void){
    int  n =  10000;
    struct timespec ts_debut, ts_fin;
    clock_gettime(CLOCKS_PROCESS_CPUTIME_ID, &ts_debut);
    liste l = NULL;
    for (int i = 0; i < n; i+=1){
        l = ajouterEnTete(l,i);
    }
    clock_gettime(CLOCKS_PROCESS_CPUTIME_ID);
    
    

        
}
