#include <SDL.h>

#define CAPACITE 5

struct qTreeNode {
    SDL_Rect area;
    struct qTreeNode* enfants[4];
    int sprites[CAPACITE];
    int nbSprites;
};

// donne le SDL_Rect représentant le i-ième quartier de r dans l'ordre
// NW, NE, SW, SE
// 0 | 1
// -----
// 2 | 3
SDL_Rect quartier(SDL_Rect *r, int i) {
    SDL_Rect res;
    res.w = r->w / 2 + (i % 2 ? r->w % 2 : 0);
    res.h = r->h / 2 + (i < 2 ? 0 : r->h % 2);
    res.y = r->y + (i < 2 ? 0 : res.h);
    res.x = r->x + (i % 2 ? res.w : 0);
    return res; 
}

SDL_Point centre_rectangle(SDL_Rect * r) {
	SDL_Point c;
	c.x = r->x + r->w / 2;
	c.y = r->y + r-> h /2;
	return c;
}

// Renvoie un pointeur vers un qtree alloué pour contenir les sprites
// du tableau sprites.
struct qTreeNode *creer_qtree(
    SDL_Rect area,
    SDL_Rect tous_sprites[],
    int indices_de_mes_sprites[],
    int nbSprites)
{
    struct qTreeNode *res = malloc(sizeof(struct qTreeNode));
    struct qTreeNode *enfants = NULL;
    res->area = area;
    res->nbSprites = 0;

    if (nbSprites <= CAPACITE) {
        res->enfants[0] = NULL;
        res->nbSprites = nbSprites;
        for(int i = 0; i < nbSprites; i++) {
            res->sprites[i] = indices_de_mes_sprites[i];
        }
    } else {
        for(int i = 0; i < 4; i++) {
            SDL_Rect area_e = quartier(&area, i);
            int nbSprites_e = 0;
            int *indice_sprites_enfants = malloc(nbSprites*sizeof(int));
            for (int k = 0; k < nbSprites; k++) {
                int j = indices_de_mes_sprites[i];
                SDL_Point pos_centre = centre_rectangle(&tous_sprites[j]);

                if(SDL_PointInRect(&pos_centre, &area_e)) {
                    indice_sprites_enfants[nbSprites_e] = j;
                    nbSprites_e += 1;
                }
            }
            res->enfants[i] = creer_qtree(area_e, 
                tous_sprites,
                indice_sprites_enfants,
                nbSprites_e);
        }
    }

    return res;
}

// TODO
void liberer_qtree(struct qTreeNode *t);