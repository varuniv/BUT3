#version 150 core

// couleur émise pour le pixel
in vec4 color;

out vec4 frag_color;
in vec3 lightDir;
in vec3 eyeVec;
in vec3 out_normal;

void main( void )
{
  vec3 L = normalize(lightDir);
  vec3 N = normalize(out_normal);
  vec3 E = normalize(eyeVec);
  vec3 R = reflect(-L, N);
  float specular = pow(max(dot(R, E), 0.5),2);


  float intensity = max(dot(L,N),0.0);
  vec4 vert = vec4(0, 1.0, 0, 1.0);
  vec4 final_color= vert*specular;
  final_color += 0.7* intensity;
  frag_color = final_color;
}
