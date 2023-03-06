/*
* This shader serves as the main map shader.
*/
#extension GL_OES_standard_derivatives: enable
#define NUM_SPECIES 132

uniform vec2 uRes;
uniform vec4 uZoomData;
uniform vec4 uMouseData;
uniform vec4 uArea;
uniform vec4 uConfig0;
uniform vec2 uPrimeProduce;
const int MAX_SELECTED = 512;
uniform vec4 uSelected[MAX_SELECTED];

// ======= DATA ======= //
// zooming data
float uStrokeWidth = uZoomData.y;
float uStrokeSoftness = uZoomData.z;
float uTime = uZoomData.w;
float uZoomT = uZoomData.x;//uConfig0.z;

// mouse data
vec2 uMousePan = uMouseData.xy; // values used to pan the map

// pinned area data
vec2 uPinPos = uArea.xy;
float uAreaRad = uArea.z;
float uAreaAlpha = uArea.w; // alpha value for rendering the area circle

// scene values
bool isConnected = bool(uConfig0.x);
int numSelected = int(uConfig0.y);


// ======= CONSTANTS ======= //
// aspect ratio
vec2 uOutAspect = uRes / uRes.y;
float frameAspect = uRes.x / uRes.y;
float texAspect = uTD2DInfos[0].res.z / uTD2DInfos[0].res.w; // aspect ratio of the map
float texFrameRatio = texAspect / frameAspect;

// ======= FUNCTIONS ======= //
float wave(vec2 uv, float speed, float scl, float waveWidthFact) {
	// create repeated waves. Takes uv. Tiling is controled by scl
	float curve = 0.4 * sin(9.25 * uv.x + (uTime * speed)) ;
	float waveWidth = waveWidthFact * remap(uZoomT,1.0, 0.0, 0.1, 1.0);
	float waveSoftness = waveWidth * .1;
	float lineAShape = clamp(distance(curve + scl * mod(uv.y, 1.0/scl), 0.5) * 1.0, 0.0, 1.0);
	return 1.0-smoothstep(waveWidth - waveSoftness, waveWidth + waveSoftness,abs(lineAShape));
}

float sdUnevenCapsule( vec2 p, float r1, float r2, float h )
{
	p.x = abs(p.x);
	float b = (r1-r2)/h;
	float a = sqrt(1.0-b*b);
	float k = dot(p,vec2(-b,a));
	if( k < 0.0 ) return length(p) - r1;
	if( k > a*h ) return length(p-vec2(0.0,h)) - r2;
	return dot(p, vec2(a,b) ) - r1;
}

float getMapData(float channel){
	return smoothstep(uStrokeWidth - uStrokeSoftness, uStrokeWidth + uStrokeSoftness, channel);
}


out vec4 fragColor;
void main()
{
	// create uv and mappers from space to space
	vec2 uv = vUV.st;
	vec2 frameToMap = vec2(1.0, 1.0/texFrameRatio); // map screen space of the frame to map space
	vec2 texCorrect = vec2(texAspect, 1.0); // maps map to scren
	vec2 aspectSize = uRes / uTD2DInfos[0].res.zw;

	vec2 mapUV = uv;
	
	// get the map space of the pinned location
	vec2 pinuv = mapLatLonToUV(uPinPos);
	// apply translation and zoom
	mapUV += uMousePan;
	mapUV -= pinuv.yx;
	// mapUV -= vec2(uAreaRad/2);	
	mapUV *= 1.0 - (.95 * uZoomT);
	// mapUV += vec2(.5) * uZoomT;
	mapUV += pinuv.yx;
	mapUV -= uMousePan;
	// mapUV += vec2(uAreaRad/2);	
	// mapUV += uMousePan;
	// mapUV = (mapUV * uZoom) + (-uMousePan + vec2(.5) - vec2(uZoom/2.0));
	
	




	// make ocean
	vec3 ocean = LIGHTBLUE.rgb;
	float isWave = wave(mapUV, .4, 40.0, .05);
	vec4 color = vec4(ocean * (1.0 - .1 * isWave), 1.0);
	
	
	vec4 mapTex = textureBicubic(sTD2DInputs[0], mapUV);
	// other land 
	float otherLand = getMapData(mapTex.b);
	color.rgb = blendNormal(color.rgb, OTHER_COLOR.rgb, step(0.0001, otherLand));
	// create city land
	float city = getMapData(mapTex.r);
	color.rgb = blendNormal(color.rgb, WHITE.rgb, step(.1, city));
	// create parks
	float parks = getMapData(textureBicubic(sTD2DInputs[1], mapUV).r);
	color.rgb = blendNormal(color.rgb, PARKS_COLOR.rgb, parks);

	// create roads
	float roads = getMapData(mapTex.g) * smoothstep(.1,.3, uZoomT);
	color.rgb = blendNormal(color.rgb, ROADS_COLOR.rgb, roads);
	// color.rgb = mix(color.rgb, BEIGE.rgb, roads);

	// draw pinned area
	float areaCircle = sdCircle(texCorrect * (mapUV - pinuv.yx), uAreaRad / MAP_MAX_DIST);
	float circleAlpha = float(areaCircle < 0.0) ; //float(areaCircle < 0.0)
	circleAlpha += 1.0-smoothstep(0.0,0.001,abs(areaCircle));
	circleAlpha = uAreaAlpha * .7 * clamp(circleAlpha, 0.0, 1.0);
	vec3 circleColor = RED.rgb;
	color.rgb = blendNormal(color.rgb, circleColor, circleAlpha);

	//draw prime produce
	vec2 primeProduceUV = mapLatLonToUV(uPrimeProduce);
	vec4 capsuleScale = vec4(.00001, .001, .002, 0.00015) * 16.0 * (1.0 - remap(uZoomT, 0.0, 1.0, 0.0, .9));
	float capsule = sdUnevenCapsule((mapUV - primeProduceUV.yx), capsuleScale.x, capsuleScale.y, capsuleScale.z);
	color.rgb = blendNormal(color.rgb, RED.rgb, 1.0 - smoothstep(0.0, .0001, capsule));
	color.rgb = mix( color.rgb, WHITE.rgb, 1.0-smoothstep(0.0, capsuleScale.w,abs(capsule)) );


	// draw selected
	// vec4 selected = drawSelected(mapUV, texCorrect);
	// color.rgb = selected.rgb * selected.a + color.rgb * (1.0 - selected.a);

	// color = selected;
	// color = vec4(mapUV, 0.0, 1.0);
	fragColor = TDOutputSwizzle(color);
}
