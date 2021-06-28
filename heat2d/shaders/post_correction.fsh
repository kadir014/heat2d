#version 330

in vec2 UV;

uniform sampler2D Texture;
uniform vec2 SCREEN;

uniform float brightness = 1.0;
uniform float contrast = 1.0;

void main()
{
  vec3 color = texture(Texture, UV).rgb;
  vec3 colorContrasted = (color) * contrast;
  vec3 bright = colorContrasted + vec3(brightness);
  gl_FragColor.rgb = bright;
  gl_FragColor.a = 1.;
}
