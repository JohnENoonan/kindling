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
const int MAX_SELECTED = 512;
uniform vec4 uSelected[MAX_SELECTED];

// ======= DATA ======= //
// zooming data
float uZoom = 1.0 / max(.0001, uZoomData.x); // amount to zoom in
float uStrokeWidth = uZoomData.y;
float uStrokeSoftness = uZoomData.z;
float uTime = uZoomData.w;
float uZoomT = uConfig0.z;

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
	float waveWidth = waveWidthFact * clamp(uZoom, 0.0, 1.0);
	float waveSoftness = waveWidth * .1;
	float lineAShape = clamp(distance(curve + scl * mod(uv.y, 1.0/scl), 0.5) * 1.0, 0.0, 1.0);
	return 1.0-smoothstep(waveWidth - waveSoftness, waveWidth + waveSoftness,abs(lineAShape));
}

vec2 mapLatLonToUV(vec2 latlon){
	return remap(latlon, MIN_LAT_LON, MAX_LAT_LON, vec2(0.0), vec2(1.0));
}



vec4 drawSelected(vec2 mapUV, vec2 mapToScreen){
	/*
	* Draw the circles for the selected trees
	*/
	vec4 color = vec4(0.0);

	for (int i = 0; i < numSelected; i++){
		vec4 tree = uSelected[i];
		vec2 treeUV = mapLatLonToUV(tree.zw);
		float circle = sdCircle(mapToScreen * (mapUV - treeUV.yx), .005);
		float alpha = float(circle < 0.0);
		color += vec4(alpha, 0.0, 0.0, alpha);
	}

	return clamp(color, vec4(0.0), vec4(1.0));
}



out vec4 fragColor;
layout(location = 1) out vec4 uvSpace;
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
	vec4 color = vec4(ocean * (1.0 - .1 * wave(uv, .4, 40.0, .1)), 1.0); // use mapUV to move the waves as well with mouse
	
	// create roads
	vec4 mapTex = textureBicubic(sTD2DInputs[0], mapUV);
	// mapTex.a = .;
	float roads = smoothstep(uStrokeWidth - uStrokeSoftness, uStrokeWidth + uStrokeSoftness, mapTex.a);
	color = mix(color, vec4(roads), float(roads > 0.1));
	color.rgb *= color.a;

	// draw pinned area
	float areaCircle = sdCircle(texCorrect * (mapUV - pinuv.yx), uAreaRad / MAP_MAX_DIST);
	float circleAlpha = .7 * float(areaCircle < 0.0) * uAreaAlpha;
	vec3 circleColor = vec3(1.0, 0.0, 1.0);
	color.rgb = circleColor * circleAlpha + color.rgb * (1.0 - circleAlpha);


	// draw selected
	vec4 selected = drawSelected(mapUV, texCorrect);
	color.rgb = selected.rgb * selected.a + color.rgb * (1.0 - selected.a);

	// color = selected;
	// color = vec4(mapUV, 0.0, 1.0);
	uvSpace = vec4(mapUV, 0.0, 1.0);

	fragColor = TDOutputSwizzle(color);
}
