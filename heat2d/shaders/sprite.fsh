#version 330

in vec2 UV;

uniform sampler2D Texture;

uniform float rotation = 0.0;
uniform vec2 position = vec2(0, 0);
uniform vec2 size = vec2(0, 0);

uniform bool has_palette = false;
uniform int palette_length = 0;
uniform vec4 palette[256];


vec2 rotateUV(vec2 uv, vec2 pivot, float rotation) {
    float cosa = cos(rotation);
    float sina = sin(rotation);
    uv -= pivot;
    return vec2(
        cosa * uv.x - sina * uv.y,
        cosa * uv.y + sina * uv.x
    ) + pivot;
}

vec2 scaleUV(vec2 uv, vec2 pos, vec2 scale){
   return vec2(
        ((uv.x - 0.5) / scale.x) - ((pos.x - 0.5) / scale.x) + 0.5,
        ((uv.y - 0.5) / scale.y) + ((pos.y - 0.5) / scale.y) + 0.5
     );
}


void main()
{
  vec4 texc = texture(Texture, rotateUV(scaleUV(UV, position, size), vec2(0.5), rotation));

  if (has_palette){
    float dist = 9999.0;
    vec4 finalc = vec4(0, 0, 0, 1);

    if (texc.a == 0.0){
      gl_FragColor = texc;
      return;
    }

    for (int i = 0; i < palette_length; i++)
    {
      vec4 c = palette[i];
      float distn = pow((texc.r-c.r), 2) + pow((texc.g-c.g), 2) + pow((texc.b-c.b), 2);
      if (distn < dist){
        dist = distn;
        finalc = vec4(c.r, c.g, c.b, texc.a);
      }
    }

    gl_FragColor = finalc;

  } else {
    gl_FragColor = texc;
  }
}
