#include <stdio.h>
#include <stdlib.h>

int
main(void)
{
    int t_stat[10];
    int * t_dyn;
    t_dyn = (int *)malloc(10*sizeof(int));

    /* Zone mémoire non initialisée */
    t_stat[0] = 37;
    t_dyn[0] = 18;
    printf("%d\n",t_stat[0]);
    printf("%d\n",t_dyn[0]);

    /* Accès à une zone mémoire non allouée */
    t_stat[10] = 42;
    printf("%d",t_stat[10]);
    t_dyn[10] = 42;
    printf("%d",t_dyn[10]);

    /* Fuite mémoire */
    t_dyn += 11; 

    /* Mémoire doublement libérée */
    int * t = (int *)malloc(sizeof(int));
    free(t);
    free(t);

    /* pointeur pendant */
    int * t3;
    t3 = malloc(sizeof(int));
    t3[0] = 42;
    free(t3);
    printf("%d",t3[0]);
    return 0;
}