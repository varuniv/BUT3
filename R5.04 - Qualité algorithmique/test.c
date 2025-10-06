#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

#define WINDOW_W 800
#define WINDOW_H 600
#define FPS 60
#define FRAME_TARGET (1000 / FPS)

#define MAX_BULLETS 128
#define MAX_ENEMIES 12
#define MAX_ENEMY_BULLETS 256
#define MAX_POWERUPS 10

#define SHIELD_USES_INITIAL 3

#define POWERUP_SIZE 20
#define POWERUP_SPEED 150
#define POWERUP_LIFETIME 7000
#define POWERUP_DROP_CHANCE 30 // %

typedef enum {
    ENEMY_NORMAL,
    ENEMY_FAST,
    ENEMY_DISPERSED,
    ENEMY_TANK
} EnemyType;

typedef struct {
    float x, y;
    float w, h;
    float vx, vy;
    bool active;
    int hp;
    EnemyType type;
} Enemy;

typedef struct {
    float x, y;
    float w, h;
    float vx, vy;
    bool active;
} Entity;

typedef enum {
    POWERUP_NONE,
    POWERUP_SHIELD,
    POWERUP_CLEAR,
    POWERUP_SCORE
} PowerupType;

typedef struct {
    float x, y;
    float w, h;
    float vy;
    PowerupType type;
    bool active;
    Uint32 spawn_time;
} Powerup;

static bool rects_intersect(float ax, float ay, float aw, float ah,
                            float bx, float by, float bw, float bh) {
    return !(ax + aw < bx || bx + bw < ax || ay + ah < by || by + bh < ay);
}

int main(void) {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER) != 0) {
        fprintf(stderr, "SDL_Init Error: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window *win = SDL_CreateWindow("Shoot 'Em Up SDL2 - Ennemis Variés",
                                       SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                       WINDOW_W, WINDOW_H, SDL_WINDOW_SHOWN);
    SDL_Renderer *renderer = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    srand((unsigned int)time(NULL));

    Entity ship = {WINDOW_W / 2.0f - 16, WINDOW_H - 64, 32, 32, 0, 0, true};
    Entity bullets[MAX_BULLETS] = {0};
    Entity enemyBullets[MAX_ENEMY_BULLETS] = {0};
    Enemy enemies[MAX_ENEMIES] = {0};
    Powerup powerups[MAX_POWERUPS] = {0};

    int score = 0;
    int weaponLevel = 1;
    int shieldUses = SHIELD_USES_INITIAL;
    bool shieldActive = false;
    bool running = true;
    bool shooting = false;
    Uint32 last_shot_time = 0;
    Uint32 shoot_delay = 150;
    Uint32 last_frame_time = SDL_GetTicks();
    Uint32 enemy_shoot_timer = 0;

    // --- Initialisation ennemis ---
    for (int i = 0; i < MAX_ENEMIES; i++) {
        enemies[i].active = true;
        enemies[i].w = 40;
        enemies[i].h = 20;
        enemies[i].x = 50 + i * 60;
        enemies[i].y = 60 + rand() % 60;
        enemies[i].type = rand() % 4;

        switch (enemies[i].type) {
            case ENEMY_NORMAL:
                enemies[i].vx = (rand()%2==0 ? 60 : -60);
                enemies[i].vy = (rand()%2==0 ? 40 : -40);
                enemies[i].hp = 1;
                break;
            case ENEMY_FAST:
                enemies[i].vx = (rand()%2==0 ? 100 : -100);
                enemies[i].vy = (rand()%2==0 ? 80 : -80);
                enemies[i].hp = 1;
                break;
            case ENEMY_DISPERSED:
                enemies[i].vx = (rand()%2==0 ? 40 : -40);
                enemies[i].vy = (rand()%2==0 ? 30 : -30);
                enemies[i].hp = 2;
                break;
            case ENEMY_TANK:
                enemies[i].vx = (rand()%2==0 ? 30 : -30);
                enemies[i].vy = (rand()%2==0 ? 20 : -20);
                enemies[i].hp = 5;
                break;
        }
    }
    for (int i = 0; i < MAX_BULLETS; i++) bullets[i].active = false;
    for (int i = 0; i < MAX_ENEMY_BULLETS; i++) enemyBullets[i].active = false;
    for (int i = 0; i < MAX_POWERUPS; i++) powerups[i].active = false;

    const Uint32 enemy_shoot_interval_base = 1200;

    while (running) {
        Uint32 frame_start = SDL_GetTicks();
        Uint32 dt_ms = frame_start - last_frame_time;
        last_frame_time = frame_start;
        float dt = dt_ms / 1000.0f;

        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) running = false;
            if (e.type == SDL_KEYDOWN) {
                if (e.key.keysym.sym == SDLK_ESCAPE) running = false;
                if (e.key.keysym.sym == SDLK_SPACE) shooting = true;
                if ((e.key.keysym.sym == SDLK_LSHIFT || e.key.keysym.sym == SDLK_RSHIFT) && shieldUses > 0) {
                    shieldActive = true;
                    shieldUses--;
                }
            }
            if (e.type == SDL_KEYUP && e.key.keysym.sym == SDLK_SPACE)
                shooting = false;
        }

        // --- Déplacement du joueur ---
        const Uint8 *kb = SDL_GetKeyboardState(NULL);
        float speed = 360.0f;
        if (kb[SDL_SCANCODE_LEFT] || kb[SDL_SCANCODE_A]) ship.x -= speed * dt;
        if (kb[SDL_SCANCODE_RIGHT] || kb[SDL_SCANCODE_D]) ship.x += speed * dt;
        if (kb[SDL_SCANCODE_UP] || kb[SDL_SCANCODE_W]) ship.y -= speed * dt;
        if (kb[SDL_SCANCODE_DOWN] || kb[SDL_SCANCODE_S]) ship.y += speed * dt;

        if (ship.x < 0) ship.x = 0;
        if (ship.x + ship.w > WINDOW_W) ship.x = WINDOW_W - ship.w;
        if (ship.y < 0) ship.y = 0;
        if (ship.y + ship.h > WINDOW_H) ship.y = WINDOW_H - ship.h;

        // --- Tir automatique joueur ---
        if (shooting && frame_start - last_shot_time >= shoot_delay) {
            last_shot_time = frame_start;
            for (int a = 0; a < weaponLevel; a++) {
                for (int i = 0; i < MAX_BULLETS; i++) {
                    if (!bullets[i].active) {
                        bullets[i].active = true;
                        bullets[i].w = 4; bullets[i].h = 12;
                        bullets[i].x = ship.x + ship.w/2 - 2 + a*8 - (weaponLevel-1)*4;
                        bullets[i].y = ship.y - 12;
                        bullets[i].vy = -600;
                        bullets[i].vx = 0;
                        break;
                    }
                }
            }
        }

        // --- Mise à jour des bullets ---
        for (int i = 0; i < MAX_BULLETS; i++) {
            if (!bullets[i].active) continue;
            bullets[i].y += bullets[i].vy * dt;
            bullets[i].x += bullets[i].vx * dt;
            if (bullets[i].y + bullets[i].h < 0) bullets[i].active = false;
        }

        // --- Mise à jour des ennemis ---
        for (int i = 0; i < MAX_ENEMIES; i++) {
            if (!enemies[i].active) continue;
            enemies[i].x += enemies[i].vx * dt;
            enemies[i].y += enemies[i].vy * dt;

            if (enemies[i].x < 0 || enemies[i].x + enemies[i].w > WINDOW_W) enemies[i].vx *= -1;
            if (enemies[i].y < 20 || enemies[i].y + enemies[i].h > 200) enemies[i].vy *= -1;
        }

        // --- Tir des ennemis selon leur type ---
        enemy_shoot_timer += dt_ms;
        if (enemy_shoot_timer >= enemy_shoot_interval_base) {
            enemy_shoot_timer = 0;
            for (int i = 0; i < MAX_ENEMIES; i++) {
                if (!enemies[i].active) continue;
                int ex = (int)(enemies[i].x + enemies[i].w/2);
                int ey = (int)(enemies[i].y + enemies[i].h);

                switch(enemies[i].type) {
                    case ENEMY_NORMAL: // tir simple
                        for (int j = 0; j < MAX_ENEMY_BULLETS; j++) {
                            if (!enemyBullets[j].active) {
                                enemyBullets[j].active = true;
                                enemyBullets[j].x = ex;
                                enemyBullets[j].y = ey;
                                enemyBullets[j].w = 4; enemyBullets[j].h = 12;
                                enemyBullets[j].vx = 0;
                                enemyBullets[j].vy = 300;
                                break;
                            }
                        }
                        break;

                    case ENEMY_FAST: // tir simple mais plus rapide
                        for (int j = 0; j < MAX_ENEMY_BULLETS; j++) {
                            if (!enemyBullets[j].active) {
                                enemyBullets[j].active = true;
                                enemyBullets[j].x = ex;
                                enemyBullets[j].y = ey;
                                enemyBullets[j].w = 4; enemyBullets[j].h = 12;
                                enemyBullets[j].vx = 0;
                                enemyBullets[j].vy = 400;
                                break;
                            }
                        }
                        break;

                    case ENEMY_DISPERSED: // tir triple
                        for (int k = -1; k <= 1; k++) {
                            for (int j = 0; j < MAX_ENEMY_BULLETS; j++) {
                                if (!enemyBullets[j].active) {
                                    enemyBullets[j].active = true;
                                    enemyBullets[j].x = ex;
                                    enemyBullets[j].y = ey;
                                    enemyBullets[j].w = 4; enemyBullets[j].h = 12;
                                    enemyBullets[j].vx = k * 100;
                                    enemyBullets[j].vy = 300;
                                    break;
                                }
                            }
                        }
                        break;

                    case ENEMY_TANK: // tir lent mais multiple
                        for (int k = -2; k <= 2; k++) {
                            for (int j = 0; j < MAX_ENEMY_BULLETS; j++) {
                                if (!enemyBullets[j].active) {
                                    enemyBullets[j].active = true;
                                    enemyBullets[j].x = ex;
                                    enemyBullets[j].y = ey;
                                    enemyBullets[j].w = 4; enemyBullets[j].h = 12;
                                    enemyBullets[j].vx = k * 60;
                                    enemyBullets[j].vy = 250;
                                    break;
                                }
                            }
                        }
                        break;
                }
            }
        }

        // --- Mise à jour des bullets ennemis ---
        for (int i = 0; i < MAX_ENEMY_BULLETS; i++) {
            if (!enemyBullets[i].active) continue;
            enemyBullets[i].x += enemyBullets[i].vx * dt;
            enemyBullets[i].y += enemyBullets[i].vy * dt;
            if (enemyBullets[i].y > WINDOW_H || enemyBullets[i].x < 0 || enemyBullets[i].x > WINDOW_W)
                enemyBullets[i].active = false;
        }
        // --- Collisions bullets → ennemis ---
        for (int b = 0; b < MAX_BULLETS; b++) {
            if (!bullets[b].active) continue;
            for (int en = 0; en < MAX_ENEMIES; en++) {
                if (!enemies[en].active) continue;
                if (rects_intersect(bullets[b].x, bullets[b].y, bullets[b].w, bullets[b].h,
                                    enemies[en].x, enemies[en].y, enemies[en].w, enemies[en].h)) {
                    bullets[b].active = false;
                    enemies[en].hp--;
                    if (enemies[en].hp <= 0) {
                        enemies[en].active = false;
                        score += 10;

                        // --- Drop power-up ---
                        if (rand() % 100 < POWERUP_DROP_CHANCE) {
                            for (int p = 0; p < MAX_POWERUPS; p++) {
                                if (!powerups[p].active) {
                                    powerups[p].active = true;
                                    powerups[p].x = enemies[en].x + enemies[en].w/2 - POWERUP_SIZE/2;
                                    powerups[p].y = enemies[en].y;
                                    powerups[p].w = POWERUP_SIZE;
                                    powerups[p].h = POWERUP_SIZE;
                                    powerups[p].vy = POWERUP_SPEED;
                                    powerups[p].spawn_time = SDL_GetTicks();
                                    int type = rand() % 3;
                                    powerups[p].type = (type == 0) ? POWERUP_SHIELD :
                                                       (type == 1) ? POWERUP_CLEAR : POWERUP_SCORE;
                                    break;
                                }
                            }
                        }

                        // --- Respawn ennemi ---
                        enemies[en].active = true;
                        enemies[en].x = rand() % (WINDOW_W - 40);
                        enemies[en].y = 50 + rand() % 100;
                        enemies[en].type = rand() % 4;
                        switch (enemies[en].type) {
                            case ENEMY_NORMAL: enemies[en].vx = (rand()%2==0?60:-60); enemies[en].vy = (rand()%2==0?40:-40); enemies[en].hp=1; break;
                            case ENEMY_FAST: enemies[en].vx = (rand()%2==0?100:-100); enemies[en].vy = (rand()%2==0?80:-80); enemies[en].hp=1; break;
                            case ENEMY_DISPERSED: enemies[en].vx = (rand()%2==0?40:-40); enemies[en].vy = (rand()%2==0?30:-30); enemies[en].hp=2; break;
                            case ENEMY_TANK: enemies[en].vx = (rand()%2==0?30:-30); enemies[en].vy = (rand()%2==0?20:-20); enemies[en].hp=5; break;
                        }
                    }
                }
            }
        }

        // --- Collisions bullets ennemis → joueur ---
        for (int i = 0; i < MAX_ENEMY_BULLETS; i++) {
            if (!enemyBullets[i].active) continue;
            if (rects_intersect(enemyBullets[i].x, enemyBullets[i].y, enemyBullets[i].w, enemyBullets[i].h,
                                ship.x, ship.y, ship.w, ship.h)) {
                enemyBullets[i].active = false;
                if (shieldActive) shieldActive = false;
                else running = false;
            }
        }

        // --- Power-ups ---
        for (int p = 0; p < MAX_POWERUPS; p++) {
            if (!powerups[p].active) continue;
            powerups[p].y += powerups[p].vy * dt;
            if (SDL_GetTicks() - powerups[p].spawn_time > POWERUP_LIFETIME || powerups[p].y > WINDOW_H)
                powerups[p].active = false;

            if (rects_intersect(powerups[p].x, powerups[p].y, powerups[p].w, powerups[p].h,
                                ship.x, ship.y, ship.w, ship.h)) {
                switch(powerups[p].type) {
                    case POWERUP_SHIELD: shieldUses++; break;
                    case POWERUP_CLEAR: for (int i=0;i<MAX_ENEMY_BULLETS;i++) enemyBullets[i].active=false; break;
                    case POWERUP_SCORE: score += 50; break;
                }
                powerups[p].active = false;
            }
        }

        // --- Weapon upgrades ---
        if (score >= 50) weaponLevel = 2;
        if (score >= 150) weaponLevel = 3;
        if (score >= 250) weaponLevel = 4;
        if (score >= 500) weaponLevel = 5;
        if (score % 100 == 0 && score > 0) shieldUses = SHIELD_USES_INITIAL;

        // --- Rendu ---
        SDL_SetRenderDrawColor(renderer, 10, 10, 30, 255);
        SDL_RenderClear(renderer);

        // Ship
        SDL_SetRenderDrawColor(renderer, 50, 200, 240, 255);
        SDL_Rect ship_rect = {(int)ship.x, (int)ship.y, (int)ship.w, (int)ship.h};
        SDL_RenderFillRect(renderer, &ship_rect);

        if (shieldActive) {
            SDL_SetRenderDrawColor(renderer, 50, 255, 50, 128);
            SDL_Rect shieldRect = {(int)ship.x-5, (int)ship.y-5, (int)ship.w+10, (int)ship.h+10};
            SDL_RenderFillRect(renderer, &shieldRect);
        }

        // Player bullets
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
        for (int i = 0; i < MAX_BULLETS; i++) {
            if (!bullets[i].active) continue;
            SDL_Rect r = {(int)bullets[i].x, (int)bullets[i].y, (int)bullets[i].w, (int)bullets[i].h};
            SDL_RenderFillRect(renderer, &r);
        }

        // Enemies (couleur selon type)
        for (int i = 0; i < MAX_ENEMIES; i++) {
            if (!enemies[i].active) continue;
            switch(enemies[i].type) {
                case ENEMY_NORMAL: SDL_SetRenderDrawColor(renderer, 220,80,80,255); break;
                case ENEMY_FAST: SDL_SetRenderDrawColor(renderer, 255,255,0,255); break;
                case ENEMY_DISPERSED: SDL_SetRenderDrawColor(renderer, 255,140,0,255); break;
                case ENEMY_TANK: SDL_SetRenderDrawColor(renderer, 150,50,200,255); break;
            }
            SDL_Rect r = {(int)enemies[i].x,(int)enemies[i].y,(int)enemies[i].w,(int)enemies[i].h};
            SDL_RenderFillRect(renderer,&r);
        }

        // Enemy bullets
        SDL_SetRenderDrawColor(renderer, 255,200,50,255);
        for (int i = 0; i < MAX_ENEMY_BULLETS; i++) {
            if (!enemyBullets[i].active) continue;
            SDL_Rect r = {(int)enemyBullets[i].x,(int)enemyBullets[i].y,(int)enemyBullets[i].w,(int)enemyBullets[i].h};
            SDL_RenderFillRect(renderer,&r);
        }

        // Power-ups
        for (int p = 0; p < MAX_POWERUPS; p++) {
            if (!powerups[p].active) continue;
            SDL_Rect r = {(int)powerups[p].x,(int)powerups[p].y,(int)powerups[p].w,(int)powerups[p].h};
            switch(powerups[p].type) {
                case POWERUP_SHIELD: SDL_SetRenderDrawColor(renderer,50,255,50,255); break;
                case POWERUP_CLEAR: SDL_SetRenderDrawColor(renderer,80,80,255,255); break;
                case POWERUP_SCORE: SDL_SetRenderDrawColor(renderer,255,255,80,255); break;
            }
            SDL_RenderFillRect(renderer,&r);
        }

        // HUD simple
        SDL_SetRenderDrawColor(renderer,255,255,255,255);
        SDL_Rect hud = {10,10,200,20};
        SDL_RenderDrawRect(renderer,&hud);
        int bar = (score % 200) < 200 ? (score % 200) : 200;
        SDL_Rect fill = {10,10,bar,20};
        SDL_RenderFillRect(renderer,&fill);

        for (int i=0;i<shieldUses;i++){
            SDL_Rect s = {10 + i*15, 40, 10,10};
            SDL_SetRenderDrawColor(renderer,50,255,50,255);
            SDL_RenderFillRect(renderer,&s);
        }

        SDL_RenderPresent(renderer);

        // --- Limiter FPS ---
        Uint32 frame_time = SDL_GetTicks() - frame_start;
        if(frame_time < FRAME_TARGET) SDL_Delay(FRAME_TARGET - frame_time);
    }

    printf("Game Over! Score: %d\n",score);

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(win);
    SDL_Quit();
    return 0;
}
