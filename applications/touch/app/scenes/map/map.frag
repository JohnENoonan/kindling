/*
* This shader serves as the main map shader.
*/
#extension GL_OES_standard_derivatives: enable

uniform vec2 uRes;
uniform vec4 uZoomData;
uniform vec4 uMouseData;
uniform vec4 uArea;

// unpack data
float uZoom = 1.0 / max(.001, uZoomData.x); // amount to zoom in

vec2 uMousePan = uMouseData.xy; // values used to pan the map

vec2 uPinPos = uArea.xy;
float uAreaRad = uArea.z;

// aspect ratio
vec2 uOutAspect = uRes / uRes.y;
float frameAspect = uRes.x / uRes.y;
float texAspect = uTD2DInfos[0].res.z / uTD2DInfos[0].res.w; // aspect ratio of the map
float texFrameRatio = texAspect / frameAspect;

out vec4 fragColor;
void main()
{
	// vec4 color = texture(sTD2DInputs[0], vUV.st);

	vec2 uv = vUV.st;
	vec2 frameToMap = vec2(1.0, 1.0/texFrameRatio); // map screen space of the frame to map space
	vec2 texCorrect = vec2(texAspect, 1.0); // maps map to scren

	vec2 aspectSize = uRes / uTD2DInfos[0].res.zw;

	vec2 mapUV = uv * aspectSize;
	mapUV = (mapUV * uZoom) + (-uMousePan + vec2(.5) - vec2(uZoom/2.0) * aspectSize);

	vec2 pin = vec2( 40.68903,-73.96961);
	vec2 pinuv = remap(uPinPos, MIN_LAT_LON, MAX_LAT_LON, vec2(0.0), vec2(1.0));





	vec4 color = vec4(1.0);
	// color.rg = mapUV;
	// color = texture(sTD2DInputs[0], mapUV);
	color = textureBicubic(sTD2DInputs[0], mapUV);
	float width = .8;
	float softness = .05;
	color = vec4(smoothstep(width - softness, width + softness, color.a));
	color.rgb *= color.a;

	// draw pinned area
	float areaCircle = sdCircle(mapUV - pinuv.yx, uAreaRad / MAP_MAX_DIST);
	float circleAlpha = .7 * float(areaCircle < 0.0);
	vec3 circleColor = vec3(1.0, 0.0, 1.0);
	color.rgb = circleColor * circleAlpha + color.rgb * (1.0 - circleAlpha);

	fragColor = TDOutputSwizzle(color);
}
