from atom.api import Atom, Int, Float, Str, Value, Enum, IntEnum, Bool, Dict, List, Typed, Event, Coerced, observe
from functools import partial
import capnp
import asyncio
import schemata as S
import logging

log = logging.getLogger(__name__)


class ParameterProxyBase(Atom):
    _params = Dict()

    def __str__(self):
        return "ParameterProxy[" + ",".join("{0}={1}".format(k, getattr(self, k)) for k in self._params.keys()) + "]"


class Parameter(Atom):
    name = Str()
    type = Int()
    value = Value()

    server = Typed(capnp.lib.capnp._DynamicCapabilityClient)
    updating = Bool(False)
    dirty = Bool(False)

    async def update(self):
        self.updating = True
        self.name = (await self.server.getName().a_wait()).value
        t_result = (await self.server.getType().a_wait()).value
        self.type = t_result.raw
        v_result = (await self.server.getValue().a_wait()).value
        self.value = getattr(v_result.value, v_result.value.which(), None)
        log.info("Found parameter {0} = {1}".format(self.name, self.value))
        self.updating = False

    @observe('value')
    def _watch_value(self, change):
        if not self.updating and change.get('type') == 'update':
            log.info("Parameter {0} got value change {1}".format(self.name, change.get('value')))
            self.dirty = True

    def send_update_to_server(self):
            loop = asyncio.get_running_loop()
            loop.call_later(0, lambda: asyncio.get_running_loop().create_task(self.push_value()))

    async def push_value(self):
        log.info("Send update for parameter {0} to server, value: {1}".format(self.name, self.value))

        try:
            pv = S.server.PcpdServer.ParameterValue()
            pv.type = self.type
            if self.type == S.server.ParameterType.bool:
                pv.value.boolValue = self.value
            elif self.type == S.server.ParameterType.char:
                pv.value.charValue = self.value
            elif self.type == S.server.ParameterType.int8:
                pv.value.int8Value = self.value
            elif self.type == S.server.ParameterType.int16:
                pv.value.int16Value = self.value
            elif self.type == S.server.ParameterType.int32:
                pv.value.int32Value = self.value
            elif self.type == S.server.ParameterType.int64:
                pv.value.int64Value = self.value
            elif self.type == S.server.ParameterType.uint8:
                pv.value.uint8Value = self.value
            elif self.type == S.server.ParameterType.uint16:
                pv.value.uint16Value = self.value
            elif self.type == S.server.ParameterType.uint32:
                pv.value.uint32Value = self.value
            elif self.type == S.server.ParameterType.uint64:
                pv.value.uint64Value = self.value
            elif self.type == S.server.ParameterType.float:
                pv.value.floatValue = self.value
            elif self.type == S.server.ParameterType.double:
                pv.value.doubleValue = self.value
            elif self.type == S.server.ParameterType.enumeration:
                pv.value.enumerationValue = self.value
            elif self.type == S.server.ParameterType.string:
                pv.value.stringValue = self.value
            elif self.type == S.server.ParameterType.any:
                pv.value.anyValue = self.value

            result = (await self.server.setValue(pv).a_wait()).value
            self.dirty = False
        except capnp.lib.capnp.KjException as e:
            log.error("Error occurred while sending parameter change to server: {0}".format(e))


PARAMETER_TYPE_MAP = {
    S.server.ParameterType.bool: (Bool, lambda s: ([], {})),
    S.server.ParameterType.char: (Str, lambda s: ([], {})),
    S.server.ParameterType.int8: (Int, lambda s: ([], {})),
    S.server.ParameterType.int16: (Int, lambda s: ([], {})),
    S.server.ParameterType.int32: (Int, lambda s: ([], {})),
    S.server.ParameterType.int64: (Int, lambda s: ([], {})),
    S.server.ParameterType.uint8: (Int, lambda s: ([], {})),
    S.server.ParameterType.uint16: (Int, lambda s: ([], {})),
    S.server.ParameterType.uint32: (Int, lambda s: ([], {})),
    S.server.ParameterType.uint64: (Int, lambda s: ([], {})),
    S.server.ParameterType.float: (Float, lambda s: ([], {})),
    S.server.ParameterType.double: (Float, lambda s: ([], {})),
    S.server.ParameterType.enumeration: (IntEnum, lambda s: ([], {})),
    S.server.ParameterType.string: (Str, lambda s: ([], {})),
    S.server.ParameterType.any: (Value, lambda s: ([], {})),
}


def make_parameter_proxy(component):
    cls_body = {}
    params = {}
    kw = {}
    for p in component.parameters:
        if p.type == S.server.ParameterType.enumeration:
            log.info("enum parameter {0} is not yet handled".format(p.name))
            continue
        params[p.name] = p
        atom_typ, param_func = PARAMETER_TYPE_MAP.get(p.type)
        pargs, pkw = param_func(p)
        cls_body[p.name] = atom_typ(*pargs, **pkw)
        kw[p.name] = p.value

    cls_body['_params'] = params
    cls = type('ParameterProxy', (ParameterProxyBase,), cls_body)
    obj = cls(**kw)

    # XXX add handlers to propagate changes back and forth
    for name, param in params.items():
        def _o(pv, change):
            if change.get('type') == 'update':
                pv.value = change.get("value")
                log.info("propagate change for {0} from proxy to parameter: {1}".format(pv.name, pv.value))
        obj.observe(name, partial(_o, param))

    print(component.name, obj)
    return obj


class Component(Atom):
    name = Str()
    type = Str()
    is_active = Bool()
    is_running = Bool()

    parameter_proxy = Typed(ParameterProxyBase)
    parameters = List(Parameter)

    server = Typed(capnp.lib.capnp._DynamicCapabilityClient)

    async def update_parameter(self, name):
        p_result = await self.server.getParameter(name).a_wait()
        prm_type = (await p_result.value.getType().a_wait()).value
        prm = Parameter(server=p_result.value)
        self.parameters.append(prm)
        await prm.update()

    async def update(self):
        self.name = (await self.server.getName().a_wait()).value
        self.type = (await self.server.getType().a_wait()).value
        self.is_active = (await self.server.getIsActive().a_wait()).value
        self.is_running = (await self.server.isRunning().a_wait()).value

        pn_result = await self.server.getParameterNames().a_wait()
        tasks = []
        for name in pn_result.value:
            tasks.append(self.update_parameter(name))
        await asyncio.gather(*tasks)
        self.parameter_proxy = make_parameter_proxy(self)


class Service(Atom):
    name = Str()
    type = Str()
    service_type = Int()

    parameter_proxy = Typed(ParameterProxyBase)
    parameters = List(Parameter)

    server = Typed(capnp.lib.capnp._DynamicCapabilityClient)

    async def update_parameter(self, name):
        p_result = await self.server.getParameter(name).a_wait()
        prm_type = (await p_result.value.getType().a_wait()).value
        prm = Parameter(server=p_result.value)
        self.parameters.append(prm)
        await prm.update()

    async def update(self):
        self.name = (await self.server.getName().a_wait()).value
        self.type = (await self.server.getType().a_wait()).value
        # self.service_type = (await self.server.getServiceType().a_wait()).value

        pn_result = await self.server.getParameterNames().a_wait()
        tasks = []
        for name in pn_result.value:
            tasks.append(self.update_parameter(name))
        await asyncio.gather(*tasks)
        self.parameter_proxy = make_parameter_proxy(self)


class Sensor(Atom):
    device_name = Str()
    depth_units_per_meter = Float()
    is_valid = Bool()
    device_calibration = Value()


class StreamEndpoint(Atom):
    is_active = Bool()
    config = Value()


class Facade(Atom):
    is_running = Bool()

    components = List(Component)
    services = List(Service)
    sensors = Dict(str, Sensor)
    stream_endpoints = Dict(str, StreamEndpoint)

    server = Typed(capnp.lib.capnp._DynamicCapabilityClient)

    def clear(self):
        # clear all (for now)
        self.components.clear()
        self.sensors.clear()
        self.stream_endpoints.clear()

    async def update_sensor(self, name, sis):
        result = await sis.getDeviceContext(name).a_wait()
        log.info("Found sensor {0}".format(name))

        ctx = result.value
        device_name = (await ctx.getDeviceName().a_wait()).value
        depth_units_per_meter = (await ctx.getDepthUnitsPerMeter().a_wait()).value
        is_valid = (await ctx.isValid().a_wait()).value
        device_calibration = (await ctx.getDeviceCalibration().a_wait()).value
        self.sensors[name] = Sensor(device_name=device_name,
                                    depth_units_per_meter=depth_units_per_meter,
                                    is_valid=is_valid,
                                    device_calibration=device_calibration)

    async def update_stream_endpoint(self, name):
        result = await self.server.getStreamingEndpoint(name).a_wait()
        log.info("Found stream_endpoint: {0}".format(name))

        try:
            endpoint = result.value
            is_active = (await endpoint.isActive().a_wait()).value
            config = (await endpoint.getConfig().a_wait()).value
            self.stream_endpoints[name] = StreamEndpoint(is_active=is_active, config=config)
        except Exception as e:
            log.error("error while updating stream_endpoint")
            log.error(e)

    async def update_component(self, name):
        result = await self.server.getComponent(name).a_wait()

        component = Component(server=result.value)
        self.components.append(component)
        await component.update()
        log.info("Found component: {0} - {1}".format(name, component.type))

    async def update_service(self, name):
        result = await self.server.getService(name).a_wait()

        service = Service(server=result.value)
        self.services.append(service)
        await service.update()
        log.info("Found service: {0} - {1} - {2}".format(name, service.type, service.service_type))

    async def update_sensors(self):
        sis_result = await self.server.getSensorInputService("device_context").a_wait()
        sis = sis_result.value
        sn_result = await sis.getSensorNames().a_wait()

        tasks = []
        for name in sn_result.value:
            tasks.append(self.update_sensor(name, sis))
        await asyncio.gather(*tasks)

    async def update_stream_endpoints(self):
        sen_result = await self.server.getStreamingEndpointNames().a_wait()
        tasks = []
        for name in sen_result.value:
            tasks.append(self.update_stream_endpoint(name))
        await asyncio.gather(*tasks)

    async def update_components(self):
        c_result = await self.server.getComponentNames().a_wait()
        tasks = []
        for name in c_result.value:
            tasks.append(self.update_component(name))
        await asyncio.gather(*tasks)

    async def update_services(self):
        c_result = await self.server.getServiceNames().a_wait()
        tasks = []
        for name in c_result.value:
            tasks.append(self.update_service(name))
        await asyncio.gather(*tasks)

    async def update(self):
        self.clear()

        result = await self.server.isNetworkRunning().a_wait()
        self.is_running = result.value

        if self.is_running:
            tasks = [
                self.update_sensors(),
                self.update_stream_endpoints(),
                self.update_components(),
                self.update_services(),
            ]
            await asyncio.gather(*tasks)

    async def start(self):
        log.info("Starting Facade")
        is_running = (await self.server.isNetworkRunning().a_wait()).value
        if not is_running:
            await self.server.loadNetwork().a_wait()
            await self.server.startNetwork().a_wait()
            await self.update()
        log.info("Starting Facade complete")

    async def stop(self):
        log.info("Stopping Facade")
        is_running = (await self.server.isNetworkRunning().a_wait()).value
        if is_running:
            self.clear()
            await self.server.stopNetwork().a_wait()
            await self.server.teardown().a_wait()
        log.info("Stopping Facade complete")

    async def connect(self):
        result = await self.server.isNetworkRunning().a_wait()
        self.is_running = result.value
        if self.is_running:
            await self.update()


class Host(Atom):
    class HostType(IntEnum):
        CaptureNode = 0
        ProcessorNode = 1
        VisualizationNode = 2

    name = Str()
    hostname = Str()
    port = Int()
    type = Typed(HostType)

    facade = Typed(Facade)

    client = Typed(capnp.TwoPartyClient)
    server = Typed(capnp.lib.capnp._DynamicCapabilityClient)

    async def connect(self):
        log.info("Connect to host: {0} at {1}:{2}".format(self.name, self.hostname, self.port))
        self.client = capnp.TwoPartyClient("{0}:{1}".format(self.hostname, self.port))
        self.server = self.client.bootstrap().cast_as(S.server.PcpdServer)

        has_facade = await self.server.hasFacade().a_wait()
        if has_facade:
            result = await self.server.getFacade().a_wait()
            self.facade = Facade(server=result.value)
            log.info("{0} attached to Facade".format(self.name))
            await self.facade.connect()


class Site(Atom):
    name = Str()

    hosts = List(Host)

    async def connect_hosts(self):
        log.info("Connect to all hosts for site: {0}".format(self.name))
        tasks = []
        for host in self.hosts:
            tasks.append(host.connect())
        return asyncio.gather(*tasks)
