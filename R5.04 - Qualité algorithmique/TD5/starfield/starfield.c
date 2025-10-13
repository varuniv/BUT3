/*
	gcc -Wall starfield.c -o stars $(sdl2-config --cflags --libs) -lSDL2 -lSDL2_image -lSDL2_ttf -lm
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <SDL.h>
#include <SDL_image.h>
#include <time.h>
#include <SDL_ttf.h>
#include <math.h>

#define tailleFenetreH		400
#define tailleFenetreW	640
#define centreX				tailleFenetreW / 2
#define centreY				tailleFenetreH / 2

// Creation de la fenetre et du canvas de la fenetre
int init(SDL_Window ** mafenetre, SDL_Renderer * canvas, SDL_Renderer ** renderer)
{
	int res=0;
	if (SDL_VideoInit(NULL) < 0)  res = 1;  // SDL_VideoInit renvoie 0 en cas de succes
	SDL_SetRenderDrawColor(canvas, 255, 255, 255, 255);
	SDL_CreateWindowAndRenderer(tailleFenetreW,tailleFenetreH, SDL_WINDOW_SHOWN,mafenetre,renderer);
	SDL_RenderClear(canvas);
	return res;
}

SDL_Texture * getTextureFromImage(const char * nomPic, SDL_Renderer * renderer)
{
	SDL_Surface * image = IMG_Load(nomPic);
	if(!image)
	{
		printf("Erreur de chargement de l'image : %s",SDL_GetError());
		return NULL;
	}
	
	SDL_Texture * texSprite=SDL_CreateTextureFromSurface(renderer, image);
	SDL_FreeSurface(image);

	return texSprite;
}

struct balls
{
	SDL_Texture *  texture;
	SDL_Rect position;
};

int main() 
{
	SDL_Window * mafenetre; 		// Fenetre du programme
	SDL_Event event; 					// Structure pour gerer les evenements clavier, souris, joystick
	SDL_Renderer * renderer;		// Canvas
		
	init(&mafenetre,renderer,&renderer);

	#define nbPoints	125
	#define wideUniverse	48000
	float mesh [nbPoints * 3];
	for (int i = 0; i < nbPoints * 3; i += 3)
	{ 
		mesh [i] = (rand()%wideUniverse) - (wideUniverse / 2);
		mesh [i + 1] = (rand()%wideUniverse) - (wideUniverse / 2);
		mesh [i + 2] = (rand()%250) + 1;
	};

	struct balls tabBalls[nbPoints];
	SDL_Texture *  ballTexGen = getTextureFromImage("asteroid.png", renderer);
	for (int i = 0; i < nbPoints; i++)
	{
		tabBalls[i].texture = ballTexGen;
		tabBalls[i].position.x = 64;
		tabBalls[i].position.y = 64;		
		tabBalls[i].position.w = 32;	
		tabBalls[i].position.h = 32;
	}
	
	int fin = 0;
	while (!fin) 
	{
		Uint64 start = SDL_GetPerformanceCounter();		
		
		SDL_RenderClear(renderer);

		// Boucle principale
		if (SDL_PollEvent(&event)) 
		{ 												// Scrute sans cesse les evenements et renvoie 1
			switch (event.type) 
			{
				case SDL_QUIT: 			// Evenement fermeture de la fenetre
				fin=1;
				break;
				
				case SDL_KEYDOWN:
                if(event.key.keysym.sym == SDLK_ESCAPE) fin = 1;					
				break;
			}
		}

		// Calcul des coords 3d			
		for (int sommet = 0; sommet < nbPoints; sommet ++)
		{			
			int ind_x = (sommet * 3) ;
			int ind_y = (sommet * 3) + 1;			
			int ind_z = (sommet * 3) + 2;
			
			int x = (mesh[ind_x]  / mesh[ind_z]) + centreX;
			int y = (mesh[ind_y]  / mesh[ind_z]) + centreY;

			tabBalls[sommet].position.x = x;
			tabBalls[sommet].position.y = y;	
			
			SDL_RenderCopy(renderer, tabBalls[sommet].texture,NULL,&tabBalls[sommet].position);
		}		
		
		// Vertical sync => Attente 60 fps
		Uint64 end= SDL_GetPerformanceCounter() ;
		float elapseTime = (end - start) / 1000000000.f;		
		while(1.0f / elapseTime > 60)
		{
			end= SDL_GetPerformanceCounter() ;
			elapseTime = (end - start) / 1000000000.f;				
		}

		SDL_RenderPresent(renderer);
	}
	
	SDL_DestroyWindow(mafenetre);
	SDL_Quit();
	exit(0);
}
