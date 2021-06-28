#version 330

in vec2 UV;

uniform sampler2D Texture;
uniform vec2 SCREEN;

uniform float alpha = 0.5;

void main()
{
  gl_FragColor = vec4(texture(Texture, UV).rgb, alpha);
}
