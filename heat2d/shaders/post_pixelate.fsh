#version 330

in vec2 UV;

uniform sampler2D Texture;
uniform vec2 SCREEN;

uniform float pixelSize = 1.0;

void main()
{
  gl_FragColor = texture(Texture, (round((UV * SCREEN) / pixelSize) * pixelSize) / SCREEN);
}
