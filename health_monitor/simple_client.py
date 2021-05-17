import sys
import os
sys.path.append(os.path.join("..", "schema"))

import time
import argparse
import capnp

import schemata as S


def parse_args():
    parser = argparse.ArgumentParser(usage='Connects to the capture server.')
    parser.add_argument("host", help="HOST:PORT")

    return parser.parse_args()


def show_parameters(entity):
    param_names = entity.getParameterNames().wait().value
    for name in param_names:
        param = entity.getParameter(name).wait().value
        param_value = param.getValue().wait().value
        print("attribute: {0}={1}".format(name, getattr(param_value.value, param_value.value.which(), None)))


def main(host):
    client = capnp.TwoPartyClient(host)

    # Bootstrap the server capability and cast it to the PcpdServer interface
    server = client.bootstrap().cast_as(S.server.PcpdServer)

    promise = server.hasFacade()
    result = promise.wait()
    facade = None
    if not result.value:
        print('server has no facade')
        exit(1)

    print("get facade")
    facade = server.getFacade().wait().value

    should_stop = False
    if not facade.isNetworkRunning().wait().value:
        print("load network")
        if facade.loadNetwork().wait().value:
            print("start network")
            if not facade.startNetwork().wait().value:
                print("error starting facade")
                exit(1)
            should_stop = True

    # fetch device calibration from sensors
    sis = facade.getSensorInputService("device_context").wait().value
    sensor_names = sis.getSensorNames().wait().value
    for name in sensor_names:
        ctx = sis.getDeviceContext(name).wait().value
        calib = ctx.getDeviceCalibration().wait().value
        print("Device: ", name, calib)

    # fetch stream endpoint descriptions
    stream_names = facade.getStreamingEndpointNames().wait().value
    for name in stream_names:
        stream = facade.getStreamingEndpoint(name).wait().value
        if not stream.isActive().wait().value:
            print("inactive stream: ", name)
            continue

        try:
            config = stream.getConfig().wait().value
            tstyp = config.which()
            if tstyp == "zmqPublisher":
                print("zmq_publisher: ", name, config.dataType, config.zmqPublisher.endpointUrl)
            else:
                print("unknown endpoint: ", name, tstyp)
        except capnp.lib.capnp.KjException as e:
            print("Error while getting stream config: ", name, e)

    component_names = facade.getComponentNames().wait().value
    for name in component_names:
        component = facade.getComponent(name).wait().value
        print("found component: ", name)
        show_parameters(component)

    service_names = facade.getServiceNames().wait().value
    for name in service_names:
        service = facade.getService(name).wait().value
        print("found service: ", name)
        show_parameters(service)

    if should_stop:
        time.sleep(10)
        print("stop network")
        facade.stopNetwork().then(lambda ret: facade.teardown()).wait()


if __name__ == '__main__':
    main(parse_args().host)

