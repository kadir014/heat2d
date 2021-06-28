#version 330

in vec2 UV;

uniform sampler2D Texture;
uniform vec2 SCREEN;

const int kernelSize = 15;
uniform float resolution = 1.0;


float normpdf(in float x, in float sigma)
{
	return 0.39894*exp(-0.5*x*x/(sigma*sigma))/sigma;
}


void main()
{
  vec3 c = texture(Texture, UV).rgb;

	const int kSize = (kernelSize-1)/2;
	float kernel[kernelSize];
	vec3 final_colour = vec3(0.0);

	float sigma = 7.0;
	float Z = 0.0;
	for (int j = 0; j <= kSize; ++j)
	{
		kernel[kSize+j] = kernel[kSize-j] = normpdf(float(j), sigma);
	}

	for (int j = 0; j < kernelSize; ++j)
	{
		Z += kernel[j];
	}

	for (int i=-kSize; i <= kSize; ++i)
	{
		for (int j=-kSize; j <= kSize; ++j)
		{
			final_colour += kernel[kSize+j]*kernel[kSize+i]*texture(Texture, (UV+vec2(float(i/(SCREEN.x/resolution)),float(j/(SCREEN.y/resolution))))).rgb;

		}
	}


	gl_FragColor = vec4(final_colour/(Z*Z), 1.0);

}
