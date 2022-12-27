// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  CONSTANTS 

const float ROOT_2 = sqrt( 2.0 );
const float P_NORM_EPSILON = 0.000001;
const float P_NORM = P_NORM_EPSILON;
const float PI = 3.14159265359;
const float QUARTER_PI = ( PI * .25 );


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  GENERIC HELPERS

// RANDOM helpers
float get_random ( float x ) { return fract(sin(x)*1e4); }
float get_random ( vec2 st )
{ 
	return fract(sin(dot(st.xy, vec2(12.9898,78.233)))* 43758.5453123);
}

// REMAP helper
float remap(
	in float value, in float low1, in float high1, in float low2, in float high2
) {
	return float(low2 + (value - low1) * (high2 - low2) / (high1 - low1));
}

vec2 remap(
	in vec2 value, in vec2 low1, in vec2 high1, in vec2 low2, in vec2 high2
) {
	return vec2(low2 + (value - low1) * (high2 - low2) / (high1 - low1));
}

vec3 remap(
	in vec3 value, in float low1, in float high1, in float low2, in float high2
) {
	return low2 + (value - low1) * (high2 - low2) / (high1 - low1);
}
vec4 remap(
	in vec4 value, in float low1, in float high1, in float low2, in float high2
) {
	return low2 + (value - low1) * (high2 - low2) / (high1 - low1);
}

float get_theta( vec2 uuvv, vec2 point )
{
  vec2 uv = uuvv - point;
  float is_left = step( 0.0, uv.x );
  float a = 0.5*acos(dot(normalize(uv),normalize(vec2(0.0,1.0))))/PI;
  a = (is_left*a+(1.0-is_left)*(1.0-a));
  return a;
}

float get_normalized_angle_from_point( vec2 uuvv, vec2 point )
{
  vec2 uv = uuvv - point;
  float is_left = step( 0.0, uv.x );
  float a = 0.5*acos(dot(normalize(uv),normalize(vec2(0.0,1.0))))/PI;
  a = (is_left*a+(1.0-is_left)*(1.0-a));
  return a;
}

float get_normalized_angle_from_center( vec2 uv )
{
	float is_left = step( 0.0, uv.x );
	float a = 0.5*acos(dot(normalize(uv),normalize(vec2(0.0,1.0))))/PI;
	a = (is_left*a+(1.0-is_left)*(1.0-a));
	return a;
}

mat4 look_at_matrix( vec3 eye, vec3 at, vec3 up )
{
	
	vec3 zaxis = normalize(eye - at);    
	zaxis =  -zaxis;

	vec3 xaxis = normalize(cross(zaxis, up));
	vec3 yaxis = cross(xaxis, zaxis);


	mat4 m;
	m[ 0 ] = vec4(xaxis.x, xaxis.y, xaxis.z, -dot(xaxis, eye));
	m[ 1 ] = vec4(yaxis.x, yaxis.y, yaxis.z, -dot(yaxis, eye));
	m[ 2 ] = vec4(zaxis.x, zaxis.y, zaxis.z, -dot(zaxis, eye));
	m[ 3 ] = vec4(0, 0, 0, 1);

	// m = -transpose( m );
	// m = -m;

	return m;

}


// ROTATION helper
mat2 rotate2d(float _angle)
{
    return mat2(cos(_angle),-sin(_angle),sin(_angle),cos(_angle));
}

// Rotate Vec2 Directly Helper
vec2 rotate(vec2 v, float a) {
	float s = sin(a);
	float c = cos(a);
	mat2 m = mat2(c, -s, s, c);
	v -= .5;
	v = m * v;
	v += .5;
	return v;
}

mat4 rotationMatrix(vec3 axis, float angle) {
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;
    
    return mat4(oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0,
                oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0,
                oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0,
                0.0,                                0.0,                                0.0,                                1.0);
}

mat3 rotation_matrix( vec3 axis, float angle ) {
	mat3 m = mat3(
		axis.x*axis.x * (1.0f - cos(angle)) + cos(angle),       // column 1 of row 1
		axis.x*axis.y * (1.0f - cos(angle)) + axis.z * sin(angle), // column 2 of row 1
		axis.x*axis.z * (1.0f - cos(angle)) - axis.y * sin(angle), // column 3 of row 1

		axis.y*axis.x * (1.0f - cos(angle)) - axis.z * sin(angle), // column 1 of row 2
		axis.y*axis.y * (1.0f - cos(angle)) + cos(angle),       // ...
		axis.y*axis.z * (1.0f - cos(angle)) + axis.x * sin(angle), // ...

		axis.z*axis.x * (1.0f - cos(angle)) + axis.y * sin(angle), // column 1 of row 3
		axis.z*axis.y * (1.0f - cos(angle)) - axis.x * sin(angle), // ...
		axis.z*axis.z * (1.0f - cos(angle)) + cos(angle)        // ...
	);
	return m;
}

vec3 rotate(vec3 v, vec3 axis, float angle) {
	mat4 m = rotationMatrix(axis, angle);
	return (m * vec4(v, 1.0)).xyz;
}

mat3 rotation3dX(float angle) {
  float s = sin(angle);
  float c = cos(angle);

  return mat3(
    1.0, 0.0, 0.0,
    0.0, c, s,
    0.0, -s, c
  );
}

mat3 rotation3dY(float angle) {
  float s = sin(angle);
  float c = cos(angle);

  return mat3(
    c, 0.0, -s,
    0.0, 1.0, 0.0,
    s, 0.0, c
  );
}

mat3 rotation3dZ(float angle) {
  float s = sin(angle);
  float c = cos(angle);

  return mat3(
    c, s, 0.0,
    -s, c, 0.0,
    0.0, 0.0, 1.0
  );
}

mat4 rotation3d(vec3 axis, float angle) {
  axis = normalize(axis);
  float s = sin(angle);
  float c = cos(angle);
  float oc = 1.0 - c;

  return mat4(
    oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0,
    oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0,
    oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0,
    0.0,                                0.0,                                0.0,                                1.0
  );
}

vec3 rotateX(vec3 v, float angle) {
  return rotation3dX(angle) * v;
}

vec3 rotateY(vec3 v, float angle) {
  return rotation3dY(angle) * v;
}

vec3 rotateZ(vec3 v, float angle) {
  return rotation3dZ(angle) * v;
}


// Scale Vec2 Directly Helper
vec2 scale( vec2 _st, vec2 _scale ){
	_st -= .5;
    _st = mat2(_scale.x,0.0,
                0.0,_scale.y) * _st;
    _st += .5;
    return _st;
}

// Integer Equality Helper
float eq( int i, int j )
{
	return
		step( float( j ) - P_NORM_EPSILON, float( i ) ) *
		step( float( i ), float( j ) + P_NORM_EPSILON );
}

float floatEq(float i, float j){
  return float(abs(i-j) < P_NORM_EPSILON);
}

// SCALED sin
float ssin( float val, float min, float max )
{
	return ( max - min ) * ( sin( val ) * 0.5 + 0.5 ) + min;
}

// SCALED cos
float scos( float val, float min, float max )
{
	return ( max - min ) * ( cos( val ) * 0.5 + 0.5 ) + min;
}


vec3 hsv_to_rgb( float h, float s, float v )
{

	vec3 rgb = vec3( 0.0 );
	
	float i = int( h * 6.0 );
	float f = ( h * 6.0 ) - i;
	float p = float( ( v * ( 1.0 - s ) ) );
	float q = float( ( v * ( 1.0 - s * f ) ) );
	float t = float( ( v * ( 1.0 - s * ( 1.0 - f ) ) ) );

	i = mod( i, 6.0 );

	rgb = 
		eq( int( s ), 0 ) * vec3( v ) +
		eq( int( i ), 0 ) * vec3( v, t, p ) +
		eq( int( i ), 1 ) * vec3( q, v, p ) +
		eq( int( i ), 2 ) * vec3( p, v, t ) +
		eq( int( i ), 3 ) * vec3( p, q, v ) +
		eq( int( i ), 4 ) * vec3( t, p, v ) +
		eq( int( i ), 5 ) * vec3( v, p, q );

	return rgb;

}

vec3 hsv_to_rgb( vec3 hsv )
{

	float h = hsv.x;
	float s = hsv.y;
	float v = hsv.z;

	vec3 rgb = hsv_to_rgb( h, s, v );
	
	return rgb;

}


vec3 rgb_to_hsv(vec3 color)
{
  vec3 hsl; // init to 0 to avoid warnings ? (and reverse if + remove first part)

  float fmin = min(min(color.r, color.g), color.b);    //Min. value of RGB
  float fmax = max(max(color.r, color.g), color.b);    //Max. value of RGB
  float delta = fmax - fmin;             //Delta RGB value

  hsl.z = (fmax + fmin) / 2.0; // Luminance

  if (delta == 0.0)   //This is a gray, no chroma...
  {
    hsl.x = 0.0;  // Hue
    hsl.y = 0.0;  // Saturation
  }
  else                                    //Chromatic data...
  {
    if (hsl.z < 0.5)
      hsl.y = delta / (fmax + fmin); // Saturation
    else
      hsl.y = delta / (2.0 - fmax - fmin); // Saturation

    float deltaR = (((fmax - color.r) / 6.0) + (delta / 2.0)) / delta;
    float deltaG = (((fmax - color.g) / 6.0) + (delta / 2.0)) / delta;
    float deltaB = (((fmax - color.b) / 6.0) + (delta / 2.0)) / delta;

    if (color.r == fmax )
      hsl.x = deltaB - deltaG; // Hue
    else if (color.g == fmax)
      hsl.x = (1.0 / 3.0) + deltaR - deltaB; // Hue
    else if (color.b == fmax)
      hsl.x = (2.0 / 3.0) + deltaG - deltaR; // Hue

    if (hsl.x < 0.0)
      hsl.x += 1.0; // Hue
    else if (hsl.x > 1.0)
      hsl.x -= 1.0; // Hue
  }

  return hsl;
}




// ANTI-ALIAS STEP helper
float aastep_thick(float threshold, float value, float afwidth) {
    return smoothstep(threshold-afwidth, threshold+afwidth, value);
}

vec2 aastep_thick(vec2 threshold, vec2 value, float afwidth) {
    return smoothstep(threshold-afwidth, threshold+afwidth, value);
}


// - - - EASES

float cubicInOut(float t) {
  return t < 0.5
    ? 4.0 * t * t * t
    : 0.5 * pow(2.0 * t - 2.0, 3.0) + 1.0;
}

float cubicIn(float t) {
  return t * t * t;
}

float cubicOut(float t) {
  float f = t - 1.0;
  return f * f * f + 1.0;
}

float exponentialInOut(float t) {
  return t == 0.0 || t == 1.0
    ? t
    : t < 0.5
      ? +0.5 * pow(2.0, (20.0 * t) - 10.0)
      : -0.5 * pow(2.0, 10.0 - (t * 20.0)) + 1.0;
}

float exponentialIn(float t) {
  return t == 0.0 ? t : pow(2.0, 10.0 * (t - 1.0));
}

float exponentialOut(float t) {
  return t == 1.0 ? t : 1.0 - pow(2.0, -10.0 * t);
}

float quadraticInOut(float t) {
  float p = 2.0 * t * t;
  return t < 0.5 ? p : -p + (4.0 * t) - 1.0;
}

float quadraticIn(float t) {
  return t * t;
}

float quadraticOut(float t) {
  return -t * (t - 2.0);
}

float circularInOut(float t) {
  return t < 0.5
    ? 0.5 * (1.0 - sqrt(1.0 - 4.0 * t * t))
    : 0.5 * (sqrt((3.0 - 2.0 * t) * (2.0 * t - 1.0)) + 1.0);
}

float circularIn(float t) {
  return 1.0 - sqrt(1.0 - t * t);
}

float circularOut(float t) {
  return sqrt((2.0 - t) * t);
}

float parabolic(float t) {
  return (sin(2.0 * PI * (t - 1/4)) + 1) / 2;
}

float blend_screen( float base, float blend ) {
  return 1.0 - ( ( 1.0 - base ) * ( 1.0 - blend ) );
}

vec3 blend_screen( vec3 base, vec3 blend ) {
  return vec3( 
    blend_screen( base.r, blend.r ),
    blend_screen( base.g, blend.g ),
    blend_screen( base.b, blend.b )
  );
}

vec3 blend_screen( vec3 base, vec3 blend, float opacity ) {
  return ( blend_screen( base, blend ) * opacity + base * ( 1.0 - opacity ) );
}








// - - - CUSTOMIZEABLE EASES

float quadraticBezier (float x, float a, float b){
	// adapted from BEZMATH.PS (1993)
	// by Don Lancaster, SYNERGETICS Inc. 
	// http://www.tinaja.com/text/bezmath.html

	float epsilon = 0.00001;
	a = max(0, min(1, a)); 
	b = max(0, min(1, b)); 
	if (a == 0.5){
	a += epsilon;
	}

	// solve t from x (an inverse operation)
	float om2a = 1 - 2*a;
	float t = (sqrt(a*a + om2a*x) - a)/om2a;
	float y = (1-2*b)*(t*t) + (2*b)*t;
	return y;
}


// - - - CUBIC Bezier

float slopeFromT (float t, float A, float B, float C){
  float dtdx = 1.0/(3.0*A*t*t + 2.0*B*t + C); 
  return dtdx;
}

float xFromT (float t, float A, float B, float C, float D){
  float x = A*(t*t*t) + B*(t*t) + C*t + D;
  return x;
}

float yFromT (float t, float E, float F, float G, float H){
  float y = E*(t*t*t) + F*(t*t) + G*t + H;
  return y;
}

float cubicBezier (float x, float a, float b, float c, float d){

  float y0a = 0.00; // initial y
  float x0a = 0.00; // initial x 
  float y1a = b;    // 1st influence y   
  float x1a = a;    // 1st influence x 
  float y2a = d;    // 2nd influence y
  float x2a = c;    // 2nd influence x
  float y3a = 1.00; // final y 
  float x3a = 1.00; // final x 

  float A =   x3a - 3.0*x2a + 3.0*x1a - x0a;
  float B = 3.0*x2a - 6.0*x1a + 3.0*x0a;
  float C = 3.0*x1a - 3.0*x0a;   
  float D =   x0a;

  float E =   y3a - 3.0*y2a + 3.0*y1a - y0a;    
  float F = 3.0*y2a - 6.0*y1a + 3.0*y0a;             
  float G = 3.0*y1a - 3.0*y0a;             
  float H =   y0a;

  // Solve for t given x (using Newton-Raphelson), then solve for y given t.
  // Assume for the first guess that t = x.
  float currentt = x;
  int nRefinementIterations = 5;
  for (int i=0; i < nRefinementIterations; i++){
    float currentx = xFromT (currentt, A,B,C,D); 
    float currentslope = slopeFromT (currentt, A,B,C);
    currentt -= (currentx - x)*(currentslope);
    currentt = clamp(currentt, 0.0,1.0);
  } 

  float y = yFromT (currentt,  E,F,G,H);
  return y;
}




// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - BLEND MODES


float blend_darken( float base, float blend ) {
  return min( blend, base );
}

vec3 blend_darken( vec3 base, vec3 blend ) {
  return vec3( 
    blend_darken( base.r, blend.r ),
    blend_darken(base.g,blend.g),
    blend_darken(base.b,blend.b)
  );
}

vec3 blend_darken( vec3 base, vec3 blend, float opacity ) {
  return ( blend_darken( base, blend ) * opacity + base * ( 1.0 - opacity ) );
}

float blend_lighten( float base, float blend ) {
  return max( blend, base );
}

vec3 blend_lighten( vec3 base, vec3 blend ) {
  return vec3( 
    blend_lighten( base.r, blend.r ), 
    blend_lighten( base.g, blend.g ), 
    blend_lighten( base.b, blend.b )
  );
}

float blend_pin_light( float base, float blend ) {
  return ( blend < 0.5 ) 
    ? blend_darken( base, ( 2.0 * blend ) )
    : blend_lighten( base, ( 2.0 * ( blend - 0.5 ) ) );
}

vec3 blend_pin_light( vec3 base, vec3 blend ) {
  return vec3(blend_pin_light(base.r,blend.r),blend_pin_light(base.g,blend.g),blend_pin_light(base.b,blend.b));
}

vec3 blend_pin_light( vec3 base, vec3 blend, float opacity ) {
  return ( 
    blend_pin_light( base, blend ) * opacity + 
    base * ( 1.0 - opacity ) 
  );
}

vec3 blend_difference( vec3 base, vec3 blend ) {
  return abs( base - blend );
}

vec3 blend_difference( vec3 base, vec3 blend, float opacity ) {
  return (
    blend_difference( base, blend ) * opacity + 
    base * ( 1.0 - opacity )
  );
}

vec3 blend_exclusion( vec3 base, vec3 blend ) {
  return base + blend - 2.0 * base * blend;
}

vec3 blend_exclusion( vec3 base, vec3 blend, float opacity ) {
  return blend_exclusion( base, blend ) * opacity + base * ( 1.0 - opacity );
}




// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - NOISE

//
// Description : Array and textureless GLSL 2D/3D/4D simplex
//               noise functions.
//      Author : Ian McEwan, Ashima Arts.
//  Maintainer : ijm
//     Lastmod : 20110822 (ijm)
//     License : Copyright (C) 2011 Ashima Arts. All rights reserved.
//               Distributed under the MIT License. See LICENSE file.
//               https://github.com/ashima/webgl-noise
//

vec3 mod289(vec3 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 mod289(vec4 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 permute(vec4 x) {
     return mod289(((x*34.0)+1.0)*x);
}

vec4 taylorInvSqrt(vec4 r)
{
  return 1.79284291400159 - 0.85373472095314 * r;
}

float snoise(vec3 v)
  {
  const vec2  C = vec2(1.0/6.0, 1.0/3.0) ;
  const vec4  D = vec4(0.0, 0.5, 1.0, 2.0);

// First corner
  vec3 i  = floor(v + dot(v, C.yyy) );
  vec3 x0 =   v - i + dot(i, C.xxx) ;

// Other corners
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min( g.xyz, l.zxy );
  vec3 i2 = max( g.xyz, l.zxy );

  //   x0 = x0 - 0.0 + 0.0 * C.xxx;
  //   x1 = x0 - i1  + 1.0 * C.xxx;
  //   x2 = x0 - i2  + 2.0 * C.xxx;
  //   x3 = x0 - 1.0 + 3.0 * C.xxx;
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy; // 2.0*C.x = 1/3 = C.y
  vec3 x3 = x0 - D.yyy;      // -1.0+3.0*C.x = -0.5 = -D.y

// Permutations
  i = mod289(i);
  vec4 p = permute( permute( permute(
             i.z + vec4(0.0, i1.z, i2.z, 1.0 ))
           + i.y + vec4(0.0, i1.y, i2.y, 1.0 ))
           + i.x + vec4(0.0, i1.x, i2.x, 1.0 ));

// Gradients: 7x7 points over a square, mapped onto an octahedron.
// The ring size 17*17 = 289 is close to a multiple of 49 (49*6 = 294)
  float n_ = 0.142857142857; // 1.0/7.0
  vec3  ns = n_ * D.wyz - D.xzx;

  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);  //  mod(p,7*7)

  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_ );    // mod(j,N)

  vec4 x = x_ *ns.x + ns.yyyy;
  vec4 y = y_ *ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);

  vec4 b0 = vec4( x.xy, y.xy );
  vec4 b1 = vec4( x.zw, y.zw );

  //vec4 s0 = vec4(lessThan(b0,0.0))*2.0 - 1.0;
  //vec4 s1 = vec4(lessThan(b1,0.0))*2.0 - 1.0;
  vec4 s0 = floor(b0)*2.0 + 1.0;
  vec4 s1 = floor(b1)*2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));

  vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy ;
  vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww ;

  vec3 p0 = vec3(a0.xy,h.x);
  vec3 p1 = vec3(a0.zw,h.y);
  vec3 p2 = vec3(a1.xy,h.z);
  vec3 p3 = vec3(a1.zw,h.w);

//Normalise gradients
  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2, p2), dot(p3,p3)));
  p0 *= norm.x;
  p1 *= norm.y;
  p2 *= norm.z;
  p3 *= norm.w;

// Mix final noise value
  vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot( m*m, vec4( dot(p0,x0), dot(p1,x1),
                                dot(p2,x2), dot(p3,x3) ) );
  }














// - - - - - - - - - - - - - - - - - - - - - - - - - - - - APPLICATION SPECIFIC

float blendOverlay(float base, float blend) {
  return base<0.5?(2.0*base*blend):(1.0-2.0*(1.0-base)*(1.0-blend));
}

vec3 blendOverlay(vec3 base, vec3 blend) {
  return vec3(blendOverlay(base.r,blend.r),blendOverlay(base.g,blend.g),blendOverlay(base.b,blend.b));
}

vec3 blendOverlay(vec3 base, vec3 blend, float opacity) {
  return (blendOverlay(base, blend) * opacity + base * (1.0 - opacity));
}

vec4 blendOverlay(vec4 base, vec4 blend) {
  return vec4(blendOverlay(base.rgb, blend.rgb), 1.0) * blend.a + base * (1.0 - blend.a);
}

float offsetTween(float tween, float min1, float max1){
  return clamp(remap(tween, min1, max1, 0.0, 1.0), 0.0, 1.0);
}

vec4 tripleMix(float t, vec4 low, vec4 mid, vec4 high){
  return mix(
      mix(low, mid, remap(t, 0.0, .5, 0.0, 1.0)),
      mix(mid, high, remap(t, .5, 1.0, 0.0, 1.0)),
      step(.5, t)
    );
}

float distSquared( vec3 A, vec3 B )
{
    vec3 C = A - B;
    return dot( C, C );
}

float distSquared( vec2 A, vec2 B )
{
    vec2 C = A - B;
    return dot( C, C );
}

// float aastep(float threshold, float value) {
//   #ifdef GL_OES_standard_derivatives
//     float afwidth = length(vec2(dFdx(value),dFdy(value)))*0.707106781186547;
//     return smoothstep(threshold-afwidth, threshold+afwidth, value);
//   #else
//     return step(threshold, value);
//   #endif  
// }
