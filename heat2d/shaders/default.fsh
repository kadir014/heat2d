#version 330

in vec2 UV;

uniform sampler2D Texture;

void main()
{
  vec3 texc = texture(Texture, UV).rgb;

  gl_FragColor = vec4(texc, 1.0);
}
