// shader for making a pill shape on a button


uniform vec2 uRes;
uniform float uWidth;
uniform float uSoftness;
uniform float uScale;

// uniform float exampleUniform;
const float PI = 3.14159265;

float udRoundBox( vec2 p, vec2 b, float r )
{
    return length(max(abs(p)-b+r,0.0))-r;
}


out vec4 fragColor;
void main()
{
	vec2 iResolution = uRes;

	float t = .4;//PI/8.0;
	float iRadius = min(iResolution.x, iResolution.y) * (0.05 + t);
    vec2 halfRes = 0.5 * iResolution.xy;

	float b = udRoundBox( vUV.st * iResolution - halfRes, halfRes * uScale, iRadius );

	float strokeWidth = uWidth/2.0;
	float stroke = 1.0 - smoothstep(0, uSoftness, abs(b) - uWidth) ; 

	vec4 color = vec4(abs(stroke));
	fragColor = TDOutputSwizzle(color);
}
