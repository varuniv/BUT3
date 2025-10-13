/*
	sudo apt install libsdl2-2.0-0 libsdl2-gfx-1.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-net-2.0-0 libsdl2-ttf-2.0-0
	sudo apt-get install libsdl2-ttf-dev
	gcc -Wall rotations3d.c -o rotations3d $(sdl2-config --cflags --libs) -lSDL2 -lSDL2_image -lSDL2_ttf -lm -lSDL2_gfx
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
#define tailleSprite			64
#define centreX				(tailleFenetreW / 2) - (tailleSprite / 2)
#define centreY				(tailleFenetreH / 2) - (tailleSprite / 2)
#define zoom					4096
#define zProjection			48

#define nbPoints	8
float mesh [] = 
{ 
	-1,1,1,
	1,1,1,
	1,-1,1,
	-1,-1,1,
	-1,1,-1,
	1,1,-1,
	1,-1,-1,
	-1,-1,-1
};

// Creation de la fenetre et du canvas de la fenetre
int init(SDL_Window ** mafenetre, SDL_Renderer * canvas, SDL_Renderer ** renderer)
{
	int res=0;
	if (SDL_VideoInit(NULL) < 0)  res = 1;  // SDL_VideoInit renvoie 0 en cas de succes
	SDL_CreateWindowAndRenderer(tailleFenetreW,tailleFenetreH, SDL_WINDOW_SHOWN,mafenetre,renderer);
	SDL_SetRenderDrawColor(canvas, 0, 0, 0, 255);
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
	float positionZ;
};

int main() 
{
	SDL_Window * mafenetre; 		// Fenetre du programme
	SDL_Event event; 					// Structure pour gerer les evenements clavier, souris, joystick
	SDL_Renderer * renderer;		// Canvas

    TTF_Init();
	TTF_Font * font = TTF_OpenFont("time.ttf", 16);
	SDL_Color blanc = {255, 255, 255}; //attention ce n'est pas un Uint32
	SDL_Surface * texte;
	SDL_Rect textPosition;
	textPosition.x = 0;
	textPosition.y = 0;
	textPosition.w = 128;
	textPosition.h = 32;
	char letemps [48];
		
	init(&mafenetre,renderer,&renderer);

	struct balls tabBalls[nbPoints];
	SDL_Texture *  ballTexGen_1 = getTextureFromImage("ball_1.png", renderer);
	SDL_Texture *  ballTexGen_2 = getTextureFromImage("ball_2.png", renderer);
	SDL_Texture *  ballTexGen_3 = getTextureFromImage("ball_3.png", renderer);
	SDL_Texture *  ballTexGen_4 = getTextureFromImage("ball_4.png", renderer);

	for (int i = 0; i < nbPoints; i++)
	{
		tabBalls[i].texture = ballTexGen_1;
		tabBalls[i].position.w = 64;	
		tabBalls[i].position.h = 64;
	}

	int fin = 0;
	float inc = (3.14 * 2)/360;  
	float a,b,c = 0;
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

		/*
			Calcul de la matrice 3D
		*/
		float xxp = cos(a) * cos(b);
		float xyp = sin(a) * cos(b);
		float xzp = sin(b);

		float yxp = sin(a) * cos(c) + cos(a) * sin(b) * sin(c);
		float yyp = -cos(a) * cos(c) + sin(a) * sin(b) * sin(c);
		float yzp = -cos(b) * sin(c);

		float zxp = sin(a) * sin(c) - cos(a) * sin(b) * cos(c);
		float zyp = -cos(a) * sin(c) - sin(a) * sin(b) * cos(c);
		float zzp = cos(b) * cos(c);

		/*
			Calcul des coords 3d
		*/
		int zzMin = 99999;
		int zzMax = -99999;		
		for (int sommet = 0; sommet < nbPoints; sommet ++)
		{	
			int x = mesh[sommet * 3] * zoom;
			int y = mesh[sommet * 3 + 1] * zoom;
			int z = mesh[sommet * 3 + 2] * zoom;
			int zz = (x*zxp + y*zyp + z*zzp) ;	
			int xx = (x*xxp + y*xyp + z*xzp) / zProjection;
			int yy = (x*yxp + y*yyp + z*yzp) / zProjection;
			
			if (zz < zzMin) zzMin = zz;
			if (zz > zzMax) zzMax = zz;
			
			tabBalls[sommet].position.x = xx + centreX;
			tabBalls[sommet].position.y = yy + centreY;
			tabBalls[sommet].positionZ = zz;
			if (tabBalls[sommet].positionZ < -3000) tabBalls[sommet].texture = ballTexGen_1;
			else if (tabBalls[sommet].positionZ < -1000) tabBalls[sommet].texture = ballTexGen_2;
			else if (tabBalls[sommet].positionZ < 1000) tabBalls[sommet].texture = ballTexGen_3;
			else if (tabBalls[sommet].positionZ < 3000) tabBalls[sommet].texture = ballTexGen_4;			
		}

		/*
			Tri sur les Z - A vous de jouer ...
		*/
		
		
		/*
			Affichage des vector balls triées
		*/
		for (int sommet = 0; sommet < nbPoints; sommet ++)
		{
			SDL_RenderCopy(renderer, tabBalls[sommet].texture,NULL,&tabBalls[sommet].position);			
		}
		
		/*
			Operation sur les angles de rotations
		*/
		a += inc; 
		b -= inc;
		c += inc;
		
		// Vertical sync => Attente 60 fps
		Uint64 end= SDL_GetPerformanceCounter() ;
		float elapseTime = (end - start) / 1000000000.f;		
		while(1.0f / elapseTime > 60)
		{
			end= SDL_GetPerformanceCounter() ;
			elapseTime = (end - start) / 1000000000.f;				
		}

		// Affichage texte haut gauche
		sprintf(letemps ," %d %d",zzMin,zzMax);
		texte = TTF_RenderText_Solid(font, letemps, blanc) ;
		SDL_Texture * message = SDL_CreateTextureFromSurface(renderer, texte);
		SDL_RenderCopy(renderer, message,NULL,&textPosition);

		SDL_RenderPresent(renderer);
	}
	
	SDL_DestroyWindow(mafenetre);
	SDL_FreeSurface(texte);
	TTF_CloseFont(font);
    TTF_Quit();
	SDL_Quit();
	exit(0);
}
