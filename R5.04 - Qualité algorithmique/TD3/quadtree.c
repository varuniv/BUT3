#include <stdlib.h>
struct noeudQT
{
    struct noeudQT *enfent[4];
    int xg, yg, xd, yd;
    struct sprite* sprites[3];
};

typedef struct noeudQT* quadtree;


int estFeuille(quadtree q)
{
    return q->enfent[0] == NULL;
}

int nbCollisions(quadtree q)
{
    if (q == NULL) return 0;
    if (estFeuille(q))
    {
        
    }
}