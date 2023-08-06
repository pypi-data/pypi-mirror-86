"""Console script for yaml_patcher."""
import argparse
import sys

from yaml_patcher.yaml_patcher import patch_yaml

def main():
    """Console script for yaml_patcher."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filepath")
    parser.add_argument("patch_filepath")
    parser.add_argument("output_filepath")
    args = parser.parse_args()

    patch_yaml(args.input_filepath, args.patch_filepath, args.output_filepath)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
