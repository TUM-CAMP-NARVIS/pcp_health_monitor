@0xbed941e077089f53; 

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("artekmed::schema");


enum BodyJointType {
    pelvis @0;
    spineNaval @1;
    spineChest @2;
    neck @3;
    clavicleLeft @4;
    shoulderLeft @5;
    elbowLeft @6;
    wristLeft @7;
    handLeft @8;
    handtipLeft @9;
    thumbLeft @10;
    clavicleRight @11;
    shoulderRight @12;
    elbowRight @13;
    wristRight @14;
    handRight @15;
    handtipRight @16;
    thumbRight @17;
    hipLeft @18;
    kneeLeft @19;
    ankleLeft @20;
    footLeft @21;
    hipRight @22;
    kneeRight @23;
    ankleRight @24;
    footRight @25;
    head @26;
    nose @27;
    eyeLeft @28;
    earLeft @29;
    eyeRight @30;
    earRight @31;
    count @32;
}

struct BodyJoint {
    bodyId @0 :UInt16;
    jointType @1 :BodyJointType;
    confidence @2 :UInt8;
    position @3 :import "math.capnp".Vec3f;
    rotation @4 :import "math.capnp".Quaternion;
}

struct HumanPoseList {
    joints @0 :List(BodyJoint);
}