#version 330
precision highp float;

in vec2 UV;

uniform sampler2D Texture;
uniform vec2 SCREEN;

uniform float offset = 3.0;

void main()
{
  vec3 left  = texture(Texture, vec2(UV.x - (offset / SCREEN.x), UV.y)).rgb;
  vec3 right = texture(Texture, vec2(UV.x + (offset / SCREEN.x), UV.y)).rgb;
  vec3 act  = vec3(left.r, sqrt(left.g*right.g), right.b);

  gl_FragColor = vec4(act, 1.0);
}
