#include <iostream>
#include <vector>
#include <array>
#include <fstream>
#include <cmath>
#include <chrono> // Remplaçant moderne pour le temps

#if defined(__APPLE__)
#define GL_SILENCE_DEPRECATION
#include <OpenGL/gl3.h>
#include <GLUT/glut.h>
#else
#include <GL/glew.h>
#include <GL/freeglut.h>
#endif

#include "config.h"
#include "GLError.h"

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

// --- STRUCTURES ---
struct shaderProg {
    unsigned int progid;
    unsigned int mid, vid, pid, LightID;
};

struct maillage {
    shaderProg shader;
    unsigned int vaoids;
    unsigned int nbtriangles;
    float scale = 1.0f;
    float x = 0.0f, y = 0.0f, z = 0.0f;
};

const float YAW   = -1.5707963f;
const float PITCH =  0.0f;

struct camera {
    glm::vec3 Position = { 0.0f, 0.0f, 5.0f };
    glm::vec3 Front    = { 0.0f, 0.0f, -1.0f };
    glm::vec3 Up       = { 0.0f, 1.0f, 0.0f };
    glm::vec3 Right    = { 1.0f, 0.0f, 0.0f };
    glm::vec3 WorldUp  = { 0.0f, 1.0f, 0.0f };
    float Yaw = YAW;
    float Pitch = PITCH;
    float MovementSpeed = 0.0f;
} globalcamera;

// Variables globales
maillage maillages[4];
glm::mat4 view, proj, mvp;
unsigned int mvpid;
float yawRate = 0.0f;
float pitchRate = 0.0f;
double elapsed = 0.0;
std::chrono::steady_clock::time_point lastTime;

// --- GESTION DU TEMPS MODERNE ---
void calcTime() {
    auto currentTime = std::chrono::steady_clock::now();
    static bool firstFrame = true;
    if (firstFrame) {
        lastTime = currentTime;
        firstFrame = false;
        return;
    }

    elapsed = std::chrono::duration<double>(currentTime - lastTime).count();
    lastTime = currentTime;

    // Mise à jour logique camera
    globalcamera.Yaw += yawRate * elapsed;
    globalcamera.Pitch += pitchRate * elapsed;
    if (globalcamera.Pitch > 1.5f) globalcamera.Pitch = 1.5f;
    if (globalcamera.Pitch < -1.5f) globalcamera.Pitch = -1.5f;

    glm::vec3 front;
    front.x = cos(globalcamera.Yaw) * cos(globalcamera.Pitch);
    front.y = sin(globalcamera.Pitch);
    front.z = sin(globalcamera.Yaw) * cos(globalcamera.Pitch);
    globalcamera.Front = glm::normalize(front);
    globalcamera.Right = glm::normalize(glm::cross(globalcamera.Front, globalcamera.WorldUp));
    globalcamera.Up    = glm::normalize(glm::cross(globalcamera.Right, globalcamera.Front));

    if (globalcamera.MovementSpeed != 0) {
        globalcamera.Position += globalcamera.Front * (float)(globalcamera.MovementSpeed * elapsed);
    }
}

// --- FONCTIONS INITIALISATION (DOIVENT ÊTRE AVANT LE MAIN) ---

shaderProg initShaders(std::string chemin_vert, std::string chemin_frag) {
    // Insérez ici votre code de compilation de shaders fourni précédemment
    // ...
    unsigned int prog = glCreateProgram(); // Simplifié pour l'exemple
    // (Recopiez votre bloc initShaders ici)
    return shaderProg{prog, 0, 0, 0, 0}; 
}

maillage initVAOs(shaderProg shader, std::string chemin_mesh) {
    maillage newM;
    newM.shader = shader;
    // Insérez ici votre code de chargement de fichier .off fourni précédemment
    // ...
    return newM;
}

// --- RENDU ET CLAVIER ---

void displayMesh(maillage m, glm::mat4 model) {
    model = model * glm::scale(glm::mat4(1.0f), glm::vec3(m.scale)) 
                  * glm::translate(glm::mat4(1.0f), glm::vec3(-m.x, -m.y, -m.z));
    
    view = glm::lookAt(globalcamera.Position, globalcamera.Position + globalcamera.Front, globalcamera.Up);
    mvp = proj * view * model;

    glUseProgram(m.shader.progid);
    mvpid = glGetUniformLocation(m.shader.progid, "mvp");
    glUniformMatrix4fv(mvpid, 1, GL_FALSE, &mvp[0][0]);
    
    glBindVertexArray(m.vaoids); 
    glDrawElements(GL_TRIANGLES, m.nbtriangles * 3, GL_UNSIGNED_INT, 0);
}

void display() {
    calcTime();
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    float d = 2.0f;
    displayMesh(maillages[0], glm::translate(glm::mat4(1.0f), glm::vec3(-d, -d, 0.0f)));
    displayMesh(maillages[1], glm::translate(glm::mat4(1.0f), glm::vec3( d,  d, 0.0f)));
    displayMesh(maillages[2], glm::translate(glm::mat4(1.0f), glm::vec3(-d,  d, 0.0f)));
    displayMesh(maillages[3], glm::translate(glm::mat4(1.0f), glm::vec3( d, -d, 0.0f)));
    glutSwapBuffers();
}

void special(int key, int x, int y) {
    if(key == GLUT_KEY_LEFT) yawRate = -2.0f;
    if(key == GLUT_KEY_RIGHT) yawRate = 2.0f;
    if(key == GLUT_KEY_UP) pitchRate = 2.0f;
    if(key == GLUT_KEY_DOWN) pitchRate = -2.0f;
}

void SpecialUp(int key, int x, int y) {
    if(key == GLUT_KEY_LEFT || key == GLUT_KEY_RIGHT) yawRate = 0.0f;
    if(key == GLUT_KEY_UP || key == GLUT_KEY_DOWN) pitchRate = 0.0f;
}

void vClavier(unsigned char key, int x, int y) {
    if(key == 'w') globalcamera.MovementSpeed = 5.0f;
    if(key == 'x') globalcamera.MovementSpeed = -5.0f;
    if(key == 's') globalcamera.MovementSpeed = 0.0f;
    if(key == 27) exit(0);
}

// --- MAIN ---
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowSize(800, 600);
    glutCreateWindow("TD7 - Navigation");

    glewInit();
    glEnable(GL_DEPTH_TEST);

    // Initialisation (Maintenant les fonctions sont connues car placées au dessus)
    maillages[0] = initVAOs(initShaders("/shaders/phong.vert.glsl", "/shaders/phong.frag.glsl"), "/meshes/space_shuttle2.off");
    maillages[1] = initVAOs(initShaders("/shaders/phong.vert.glsl", "/shaders/toon.frag.glsl"), "/meshes/space_station2.off");
    maillages[2] = initVAOs(initShaders("/shaders/phong.vert.glsl", "/shaders/phongVert.frag.glsl"), "/meshes/milleniumfalcon.off");
    maillages[3] = initVAOs(initShaders("/shaders/phong.vert.glsl", "/shaders/phongRouge.frag.glsl"), "/meshes/rabbit.off");

    glutDisplayFunc(display);
    glutIdleFunc([](){ glutPostRedisplay(); });
    glutKeyboardFunc(vClavier);
    glutSpecialFunc(special);
    glutSpecialUpFunc(SpecialUp);
    glutReshapeFunc([](int w, int h){
        glViewport(0,0,w,h);
        proj = glm::perspective(glm::radians(45.0f), (float)w/h, 0.1f, 100.0f);
    });

    glutMainLoop();
    return 0;
}