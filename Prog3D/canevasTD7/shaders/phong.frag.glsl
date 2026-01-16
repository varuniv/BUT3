#version 150 core

in vec4 color;

out vec4 frag_color;
in vec3 lightDir;
in vec3 eyeVec;
in vec3 out_normal;

vec4 toonify(in float intensity) {
  vec4 color;
  if (intensity > 0.98)
    color = vec4(0.8,0.8,0.8,1.0);
  else if (intensity > 0.5)
    color = vec4(0.4,0.4,0.8,1.0);
  else if (intensity > 0.25)
    color = vec4(1.0, 0.0, 0.0, 1.0);
  else
    color = vec4(0.1,0.1,0.1,1.0);
  return(color);
}

void main( void )
{
  vec3 L = normalize(lightDir);
  vec3 N = normalize(out_normal);
  vec3 E = normalize(eyeVec);
  vec3 R = reflect(-L, N);
  float specular = pow(max(dot(R, E), 0.5),2);


  float intensity = max(dot(L,N),0.0);
  vec4 gris = vec4(0.5, 0.5, 0.5, 1.0);
  vec4 final_color= gris*specular;
  final_color += 0.7*intensity;
  frag_color = final_color;

}
