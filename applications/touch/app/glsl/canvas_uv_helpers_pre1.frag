// ANTI-ALIAS STEP helper
float aastep(float threshold, float value) {
	#ifdef GL_OES_standard_derivatives
		float afwidth = length(vec2(dFdx(value),dFdy(value)))*0.707106781186547;
		return smoothstep(threshold-afwidth, threshold+afwidth, value);
	#else
		return step(threshold, value);
	#endif  
}