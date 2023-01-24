// Example Pixel Shader
#extension GL_OES_standard_derivatives: enable

// uniform float exampleUniform;
uniform vec2 uRes;
uniform vec4 uZoomData;
uniform vec4 uMouseData;
uniform vec4 uArea;

// unpack data
float uZoom = 1.0 / max(.001, uZoomData.x);

vec2 uMousePan = uMouseData.xy;

vec2 uPinPos = uArea.xy;
float uAreaRad = uArea.z;

// aspect ratio
vec2 uOutAspect = uRes / uRes.y;
float frameAspect = uRes.x / uRes.y;
float texAspect = uTD2DInfos[0].res.z / uTD2DInfos[0].res.w; // aspect ratio of the map
float texFrameRatio = texAspect / frameAspect;



vec4 cubic(float v){
    vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
    vec4 s = n * n * n;
    float x = s.x;
    float y = s.y - 4.0 * s.x;
    float z = s.z - 4.0 * s.y + 6.0 * s.x;
    float w = 6.0 - x - y - z;
    return vec4(x, y, z, w) * (1.0/6.0);
}

vec4 textureBicubic(sampler2D tex, vec2 texCoords){

   vec2 texSize = textureSize(tex, 0);
   vec2 invTexSize = 1.0 / texSize;
   
   texCoords = texCoords * texSize - 0.5;

   
    vec2 fxy = fract(texCoords);
    texCoords -= fxy;

    vec4 xcubic = cubic(fxy.x);
    vec4 ycubic = cubic(fxy.y);

    vec4 c = texCoords.xxyy + vec2 (-0.5, +1.5).xyxy;
    
    vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
    vec4 offset = c + vec4 (xcubic.yw, ycubic.yw) / s;
    
    offset *= invTexSize.xxyy;
    
    vec4 sample0 = texture(tex, offset.xz);
    vec4 sample1 = texture(tex, offset.yz);
    vec4 sample2 = texture(tex, offset.xw);
    vec4 sample3 = texture(tex, offset.yw);

    float sx = s.x / (s.x + s.y);
    float sy = s.z / (s.z + s.w);

    return mix(
       mix(sample3, sample2, sx), mix(sample1, sample0, sx)
    , sy);
}

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
	vec2 pinuv = remap(pin, MIN_LAT_LON, MAX_LAT_LON, vec2(0.0), vec2(1.0));





	vec4 color = vec4(1.0);
	// color.rg = mapUV;
	// color = texture(sTD2DInputs[0], mapUV);
	color = textureBicubic(sTD2DInputs[0], mapUV);
	float width = .8;
	float softness = .05;
	color = vec4(smoothstep(width - softness, width + softness, color.a));
	color.rgb *= color.a;

	color = mix(color, color * vec4(1.0, 0.0, 0.0, .5), step(distance(mapUV, pinuv.yx), 1.0 / MAP_MAX_DIST));
	// color.rg = pinuv;

	// color = vec4(onLand);
	fragColor = TDOutputSwizzle(color);
}
