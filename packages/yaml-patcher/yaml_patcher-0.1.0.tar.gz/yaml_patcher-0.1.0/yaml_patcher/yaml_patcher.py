"""Main module."""
import argparse

import yaml
from benedict import benedict

# same syntax as https://github.com/krishicks/yaml-patch

def patch_yaml(yml_path, patch_conf_ops_path, output_path):
    print(yml_path, patch_conf_ops_path, output_path)
    
    d = benedict.from_yaml(yml_path)
    patch_conf_ops = yaml.load(open(patch_conf_ops_path))

    for op_specs in patch_conf_ops:
        if op_specs["op"] == "replace":
            d[op_specs["path"]] = op_specs["value"]
        else:
            raise ValueError(f"Invalid operation type: {op_specs}")

    o = d.to_yaml()
    with open(output_path, "w") as outfile:
        outfile.write(o)

