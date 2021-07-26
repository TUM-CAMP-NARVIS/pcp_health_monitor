@0x870412502809cf76;

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("artekmed::schema");

enum ApplicationLifeCycleEventDomain {
  application @0;
  coreService @1;
  consumerService @2;
  producerService @3;
  runtime @4;
  dataflow @5;
  component @6;
}

enum ApplicationLifeCycleStatus {
  initialized @0;
  started @1;
  stopped @2;
  uninitialized @3;
}

enum ApplicationLifeCycleRequest {
  requestShutdown @0;
  playbackStart @1;
  playbackPause @2;
  playbackStep @3;
  playbackStop @4;
  recordingStart @5;
  recordingPause @6;
  recordingStop @7;
}

enum HealthStatusUpdate {
  watchdogEvent @0;
  captureDeviceTimeout @1;
  diskSpaceWarning @2;
  lowLightWarning @3;
  lowFramerateWarning @4;
  writeQueueWarning @5;
  frameRateInfo @6;
  imuMovementWarning @7;
}

struct ApplicationStatusEvent {
  domain @0 :ApplicationLifeCycleEventDomain;
  name @1 :Text;
  status @2 :ApplicationLifeCycleStatus;
}

struct ApplicationRequestEvent {
  domain @0 :ApplicationLifeCycleEventDomain;
  name @1 :Text;
  request @2 :ApplicationLifeCycleRequest;
}

struct ApplicationHealthStatusEvent {
  domain @0 :ApplicationLifeCycleEventDomain;
  name @1 :Text;
  healthStatus @2 :HealthStatusUpdate;
  payload @3 :Data;
}

struct ApplicationEvent {
    timestamp      @0 :UInt64;
    nodeName       @1 :Text;
    event          @2 :Event;
    struct Event {
        value : union {
            status       @0  :ApplicationStatusEvent;
            request      @1  :ApplicationStatusEvent;
            healthStatus @2  :ApplicationHealthStatusEvent;
        }
    }
}
