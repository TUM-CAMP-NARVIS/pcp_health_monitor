import yaml

import model

HOST_TYPE_MAP = {
    "CaptureNode": model.Host.HostType.CaptureNode,
    "ProcessorNode": model.Host.HostType.ProcessorNode,
    "VisualisationNode": model.Host.HostType.VisualizationNode
}


def transform_enum(host):
    for key in host.keys():
        # host should only have one key.. return the parameters for simpler
        # access
        host[key]["type"] = HOST_TYPE_MAP[host[key]["type"]]
        return host[key]


def parse_config(path):
    with open(path, "r") as file:
        file_stream = file.read()
        config = yaml.safe_load(file_stream)
        hosts = config["site"]["hosts"]
        config['site']['hosts'] = map(transform_enum, hosts)
        return config
