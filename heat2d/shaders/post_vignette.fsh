#version 330

in vec2 UV;

uniform sampler2D Texture;
uniform vec2 SCREEN;

uniform float strength = 0.35;
uniform float spread = 15.0;

void main()
{
  vec2 UVn = UV;

  UVn *= 1.0 - UVn.yx;

  float vig = UVn.x * UVn.y * spread;
  vig = pow(vig, strength);

  vec4 tex = texture(Texture, UV);

  gl_FragColor = vec4(tex.rgb * vig, tex.a);
}
