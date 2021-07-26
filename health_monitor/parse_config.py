import yaml

import model

def parse_config(path):
    with open(path, "r") as file:
        file_stream = file.read()
        config = yaml.safe_load(file_stream)
        config = config["site"]
        # parse hosts into a more easily
        # readable format
        hosts = dict()
        for host in config["hosts"]:
            host_id = [x for x in host.keys()][0]
            hosts[host_id] = host[host_id]

        config["hosts"] = hosts
        return config
