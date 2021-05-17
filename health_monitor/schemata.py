from pkg_resources import resource_filename
import os
import capnp

capnp.remove_import_hook()
schema_base_path = resource_filename("health_monitor", "schema")
import_base_path = os.path.dirname(resource_filename("capnp", ""))

__all__ = ['core', 'bodytracking', 'deviceCalibration', 'math', 'measurement', 'network', 'server', 'events']

core = capnp.load(os.path.join(schema_base_path, 'core.capnp'), imports=[import_base_path, ])
bodytracking = capnp.load(os.path.join(schema_base_path, 'bodytracking.capnp'), imports=[import_base_path, ])
deviceCalibration = capnp.load(os.path.join(schema_base_path, 'deviceCalibration.capnp'), imports=[import_base_path, ])
math = capnp.load(os.path.join(schema_base_path, 'math.capnp'), imports=[import_base_path, ])
measurement = capnp.load(os.path.join(schema_base_path, 'measurement.capnp'), imports=[import_base_path, ])
network = capnp.load(os.path.join(schema_base_path, 'network.capnp'), imports=[import_base_path, ])
server = capnp.load(os.path.join(schema_base_path, 'pcpdServer.capnp'), imports=[import_base_path, ])
events = capnp.load(os.path.join(schema_base_path, 'events.capnp'), imports=[import_base_path, ])
