#version 330

in vec2 UV;

uniform sampler2D Texture;
uniform vec2 SCREEN;

uniform float red = 1.0;
uniform float green = 1.0;
uniform float blue = 1.0;

void main()
{
  vec4 tex = texture(Texture, UV);
  tex.r *= red;
  tex.g *= green;
  tex.b *= blue;
  gl_FragColor = tex;
}
