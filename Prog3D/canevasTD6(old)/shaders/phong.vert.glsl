#version 150 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

in vec3 in_pos;
in vec3 in_normal;

out vec3 lightDir;
out vec3 eyeVec;
out vec3 out_normal;

void main(void)
{
    // position du sommet dans l’espace vue
    vec4 vVertex = view * model * vec4(in_pos, 1.0);

    // vecteur vers l’œil
    eyeVec = -vVertex.xyz;

    // position de la lumière (fixe)
    vec4 LightSource_position = vec4(0.0, 0.0, 10.0, 1.0);
    lightDir = vec3(LightSource_position - vVertex);

    // transformation des normales
    out_normal = vec3(view * model * vec4(in_normal, 0.0));

    // position finale
    gl_Position = proj * view * model * vec4(in_pos, 1.0);
}
