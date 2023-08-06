import json
import sys
from .input import read_geojson
from .solver import solve


def main():
    input_config, pc = read_geojson(sys.argv[1])
    result = solve(pc, input_config)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
