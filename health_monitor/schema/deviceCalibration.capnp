@0xfc92d8f6c8da99c0;

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("artekmed::schema");

struct DistortionParameters {
	k1 @0 :Float32;
	k2 @1 :Float32;
	k3 @2 :Float32;
	k4 @3 :Float32;
	k5 @4 :Float32;
	k6 @5 :Float32;
	tx @6 :Float32;
	ty @7 :Float32;
}

struct CameraIntrinsicParameters {
	fovX @0 :Float32;
	fovY @1 :Float32;
	cX   @2 :Float32;
	cY   @3 :Float32;

    # should the intrinsics matrix also be part of the serialization ?
    # basically it is redundant with intrinsic parameters

	width  @4 :Int32;
	height @5 :Int32;

	distortionParams @6 :DistortionParameters;
}


struct DeviceCalibration {
	depthCameraParameters @0 :CameraIntrinsicParameters;
	colorCameraParameters @1 :CameraIntrinsicParameters;
	color2depthTransform  @2 :import "math.capnp".Pose;
	cameraPose            @3 :import "math.capnp".Pose;
	isValid               @4 :Bool;
}