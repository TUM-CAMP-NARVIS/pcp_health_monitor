@0xb341aaa9e4752b74;

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("artekmed::network");


enum StreamDataType {
    unknown @0;
    image @1;
    bitstream @2;
    bodytrackingPoses @3;
}

struct NetworkSenderConfig {
    dataType @0 :StreamDataType;
    bufferInfo @1 :import "core.capnp".BufferInfo;
    union {
        zmqPublisher :group {
            endpointUrl @2 :Text;
        }
        ddsPublisher :group {
            topicName @3 :Text;
        }
        udpSender :group {
            ipaddress @4 :Text;
            port @5 :Int32;
        }
        rtspSender :group {
            rtspUrl @6 :Text;
        }
        avbtSender :group {
            senderAddress @7 :Text;
        }
    }
}