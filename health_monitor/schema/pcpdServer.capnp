@0xa2eed44608e649c8;

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("artekmed::server");


enum ParameterType {
  bool @0;
  char @1;
  int8 @2;
  int16 @3;
  int32 @4;
  int64 @5;
  uint8 @6;
  uint16 @7;
  uint32 @8;
  uint64 @9;
  float @10;
  double @11;
  enumeration @12;
  string @13;
  any @14;
}

enum ServiceType {
  core @0;
  producer @1;
  consumer @2;
}

enum RecorderStatus {
  invalid @0;
  idle @1;
  recording @2;
  paused @3;
  error @4;
}

interface PcpdServer {

    hasFacade @0 () -> (value :Bool);
    getFacade @1 () -> (value :Facade);
    createFacade @2 (configFiles :List(Text)) -> (value :Bool);
    destroyFacade @3 () -> (value :Bool);

    interface Facade {
        loadNetwork @0 () -> (value :Bool);
        startNetwork @1 () -> (value :Bool);
        stopNetwork @2 () -> (value :Bool);
        teardown @3 () -> (value :Bool);
        isNetworkRunning @4 () -> (value :Bool);

        getComponentNames @5 () -> (value :List(Text));
        getComponent @6 (name :Text) -> (value :Component);

        getServiceNames @7 () -> (value :List(Text));
        getService @8 (name :Text) -> (value :Service);

        getSensorInputService @9 (name :Text) -> (value :SensorInputService);

        getStreamingEndpointNames @10 () -> (value :List(Text));
        getStreamingEndpoint @11 (name :Text) -> (value :StreamEndpoint);
    }


    interface Component {
        getName @0 () -> (value :Text);
        getType @1 () -> (value :Text);

        getIsActive @2 () -> (value :Bool);
        setIsActive @3 (value :Bool);
        isRunning @4 () -> (value :Bool);

        getParameterNames @5 () -> (value :List(Text));
        getParameter @6 (name :Text) -> (value :Parameter);
    }

    interface Service {
        getName @0 () -> (value :Text);
        getType @1 () -> (value :Text);
        getServiceType @2 () -> (value :ServiceType);

        getParameterNames @3 () -> (value :List(Text));
        getParameter @4 (name :Text) -> (value :Parameter);
    }

    interface Parameter {
        getName @0 () -> (value :Text);
        getType @1 () -> (value :ParameterType);
        getValue @2 () -> (value :ParameterValue);
        setValue @3 (value :ParameterValue) -> (value :Bool);
    }

    struct ParameterValue {
        type @0 :ParameterType;
        value : union {
              boolValue @1 :Bool;
              charValue @2 :UInt8;
              int8Value @3 :Int8;
              int16Value @4 :Int16;
              int32Value @5 :Int32;
              int64Value @6 :Int64;
              uint8Value @7 :UInt8;
              uint16Value @8 :UInt16;
              uint32Value @9 :UInt32;
              uint64Value @10 :UInt64;
              floatValue @11 :Float32;
              doubleValue @12 :Float64;
              enumerationValue @13 :Text;
              stringValue @14 :Text;
          }
    }

    interface SensorInputService {
        getSensorCount @0 () -> (value :Int32);
        getSensorNames @1 () -> (value :List(Text));
        getDeviceContext @2 (name :Text) -> (value :DeviceContext);
    }

    interface RecorderService {
        getRecorderStatus @0 () -> (value :RecorderStatus);
        startRecording @1 () -> (value :Bool);
        stopRecording @2 () -> (value :Bool);
    }

    interface DeviceContext {
        getDeviceName @0 () -> (value :Text);
        getDepthUnitsPerMeter @1 () -> (value :Float32);
        isValid @2 () -> (value :Bool);
        getDeviceCalibration @3 () -> (value :import "deviceCalibration.capnp".DeviceCalibration);
        getTimestampOffset @4 () -> (value :UInt64);
    }

    interface StreamEndpoint {
        isActive @0 () -> (value :Bool);
        getConfig @1 () -> (value :import "network.capnp".NetworkSenderConfig);
    }

}