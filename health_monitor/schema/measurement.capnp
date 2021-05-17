@0xbf84196599dec8ba; 

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("artekmed::schema");


struct StreamHeader {
    dimX @0 :Int32 = 1;
    dimY @1 :Int32 = 1;
    dimZ @2 :Int32 = 1;
    bitsPerElement @3 :Int32;

    union {
        scalar     @4 :Void;
        bitStream  @5 :import "core.capnp".BitstreamEncoding;
        image      @6 :import "core.capnp".PixelFormat;
        pointCloud @7 :import "core.capnp".PointCloudFormat;
        mesh       @8 :Void;
        humanPoseList  @9 :Void;
        buffer @10 :Void;
    }
}

struct Measurement {
    timestamp      @0 :UInt64;
    count          @1 :UInt32;
    entry          @2 :Entry;
    struct Entry {
        value : union {
            scalar         @0  :import "core.capnp".Scalar;
            scalarList     @1  :List(import "core.capnp".Scalar);
            vec2f          @2  :import "math.capnp".Vec2f;
            vec2fList      @3  :List(import "math.capnp".Vec2f);
            vec3f          @4  :import "math.capnp".Vec3f;
            vec3fList      @5  :List(import "math.capnp".Vec3f);
            vec4f          @6  :import "math.capnp".Vec4f;
            vec4fList      @7  :List(import "math.capnp".Vec4f);
            matrix3x3f     @8  :import "math.capnp".Matrix3x3f;
            matrix3x3fList @9  :List(import "math.capnp".Matrix3x3f);
            matrix3x4f     @10 :import "math.capnp".Matrix3x4f;
            matrix3x4fList @11 :List(import "math.capnp".Matrix3x4f);
            matrix4x4f     @12 :import "math.capnp".Matrix4x4f;
            matrix4x4fList @13 :List(import "math.capnp".Matrix4x4f);
            quaternion     @14 :import "math.capnp".Quaternion;
            quaternionList @15 :List(import "math.capnp".Quaternion);
            pose           @16 :import "math.capnp".Pose;
            poseList       @17 :List(import "math.capnp".Pose);
            humanPose      @18 :import "bodytracking.capnp".HumanPoseList;
            humanPoseList  @19 :List(import "bodytracking.capnp".HumanPoseList);
            image2D        @20 :import "core.capnp".Image2D;
            image2DList    @21 :List(import "core.capnp".Image2D);
            buffer         @22 :import "core.capnp".BufferRef;
            bufferList     @23 :List(import "core.capnp".BufferRef);
            pointCloudNormal @24 :import "core.capnp".PointCloudNormal;
            pointCloudNormalList @25 :List(import "core.capnp".PointCloudNormal);
            cvMat @26 :import "core.capnp".CvMat;
            cvMatList @27 :List(import "core.capnp".CvMat);
        }
    }
}


struct RecordingSchema {
    name @0 :Text;
    recorderType :union {
        file: group {
            frameTimeLogFileName @1 :Text;
            directory @2 :Text;
        }
        mkv: group {
            fileName @3 :Text;
        }
    }

    channels @4 :List(Channel);
    calibrations @5 :List(CalibrationEntry);

    struct CalibrationEntry {
        name @0: Text;
        calibration @1 :import "deviceCalibration.capnp".DeviceCalibration;
    }
    struct Channel {
        index @0 :Int32;
        name @1 :Text;
        type @2 :import "core.capnp".DataType;
        directory @3 :Text;
        storage :union {
            mkvVideo :group {
                width @4 :Int32;
                height @5 :Int32;
                pixelFormat @6 :import "core.capnp".PixelFormat;
                pixelFormatStorage @7 :import "core.capnp".PixelFormat;
            }
            mkvData :group {
                maxPacketLen @8 :Int32;
            }
            streamFile :group {
                fileName @9 :Text;
            }
            singleFile :group {
                directory @10 :Text;
                filePrefix @11 :Text;
                fileSuffix @12 :Text;
            }
        }
    }
}

struct EventTimeLogEntry {
        channel @0 :Int32;
        timestamp @1 :UInt64;
        frameIndex @2 :UInt32;
}


struct RecordingEventLog {
    entries @0 :EventTimeLogEntry;
}
