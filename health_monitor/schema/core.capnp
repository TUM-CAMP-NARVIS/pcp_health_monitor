@0xb125264a01df1134;

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("artekmed::schema");

struct Map(Key, Value) {
  entries @0 :List(Entry);
  struct Entry {
    key @0 :Key;
    value @1 :Value;
  }
}

struct Scalar {
    value : union {
          boolValue @0 :Bool;
          int8Value @1 :Int8;
          int16Value @2 :Int16;
          int32Value @3 :Int32;
          int64Value @4 :Int64;
          uint8Value @5 :UInt8;
          uint16Value @6 :UInt16;
          uint32Value @7 :UInt32;
          uint64Value @8 :UInt64;
          floatValue @9 :Float32;
          doubleValue @10 :Float64;
      }
}

enum DataType {
    scalar     @0;
    vec2f      @1;
    vec3f      @2;
    vec4f      @3;
    matrix3x3f @4;
    matrix3x4f @5;
    matrix4x4f @6;
    quaternion @7;
    pose       @8;
    humanPoseList  @9;
    image  @10;
    pointCloud @11;
    mesh @12;
    buffer @13;
}

enum BitstreamEncoding {
    h264 @0;
    h265 @1;
}

enum PixelFormat {
    unknown @0;
    luminance @1;
    rgb @2;
    bgr @3;
    rgba @4;
    bgra @5;
    yuv422 @6;
    yuv411 @7;
    raw @8;
    depth @9;
    float @10;
    mjpeg @11;
    zdepth @12;
}


enum PointCloudFormat {
    positionNormalRadius @0;
    positionTextureCoordinate @1;
}

struct Image2D {
    pixelFormat @0 :PixelFormat;
    cvType @1 :Int32;
    width @2 :UInt32;
    height @3 :UInt32;
    stride @4 :UInt32;
    data @5 :Data;
}

struct BufferRef {
    size @0 :UInt64 = 0;
    data @1 :Data;
}

struct BufferInfo {
    frameSize @0 :UInt64 = 0;
    width      @1 :UInt32 = 0;
    height     @2 :UInt32 = 0;
    bitsPerElement @3 :UInt32 = 0;
    stride     @4 :UInt32 = 0;
    properties @5 :List(Entry);

    struct Entry {
        name @0 :Text;
        value @1 :Int32;
    }
}

struct PointNormal {
 x @0 :Float32;
 y @1 :Float32;
 z @2 :Float32;
 normalX @3 :Float32;
 normalY @4 :Float32;
 normalZ @5 :Float32;
 radius @6 :Float32;
}

struct PointCloudNormal {
 points @0 :List(PointNormal);
 width @1 :UInt32;
 height @2 :UInt32;
 isDense @3 :Bool;
}

struct CvMat {
 # @todo: implement this, placeholder
 data @0 :UInt32;
}
