#version 150 core

in vec3 lightDir;
in vec3 eyeVec;
in vec3 out_normal;

out vec4 frag_color;

void main(void)
{
    vec3 baseColor = vec3(0.2, 0.8, 0.3);

    vec3 N = normalize(out_normal);
    vec3 L = normalize(lightDir);
    vec3 E = normalize(eyeVec);
    vec3 R = reflect(-L, N);

    float diff = max(dot(N, L), 0.0);
    float spec = pow(max(dot(R, E), 0.0), 32.0);

    vec3 ambient  = 0.2 * baseColor;
    vec3 diffuse  = diff * baseColor;
    vec3 specular = spec * vec3(1.0);

    frag_color = vec4(ambient + diffuse + specular, 1.0);
}
