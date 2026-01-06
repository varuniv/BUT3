#version 150 core

// couleur émise pour le pixel
in vec3 color;

out vec4 frag_color;

void main( void )
{
  float stripe = mod(ceil(gl_FragCoord.x/10),3);
  frag_color = vec4(stripe < 1.0 ? 1.0 : 0.0, stripe > 1.0 ? 1.0 : 0.0, 0.0, 1.0);
}
