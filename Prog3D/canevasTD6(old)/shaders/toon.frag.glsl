#version 150 core

in vec3 lightDir;
in vec3 out_normal;

out vec4 frag_color;

void main(void)
{
    vec3 N = normalize(out_normal);
    vec3 L = normalize(lightDir);

    float intensity = dot(N, L);

    vec4 color;
    if (intensity > 0.95)
        color = vec4(0.2, 0.3, 1.0, 1.0);
    else if (intensity > 0.5)
        color = vec4(0.15, 0.2, 0.7, 1.0);
    else if (intensity > 0.25)
        color = vec4(0.1, 0.15, 0.4, 1.0);
    else
        color = vec4(0.05, 0.05, 0.2, 1.0);

    frag_color = color;
}
