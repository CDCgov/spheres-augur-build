import argparse
import pandas as pd
import pathlib
import yaml
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--colors", required=True, help="name of the base colors file")
    parser.add_argument("--builds", required=True,  help="builds YAML with state names given by the 'division' attribute")
    parser.add_argument("--state-color", default="#DB2823", help="color to use to highlight a given build's state")
    parser.add_argument("--colors-directory", required=True, help="directory to store state-specific colors files")
    parser.add_argument("--revised-builds", required=True, help="builds YAML modified to include custom colors")

    args = parser.parse_args()

    # Load the base colors file.
    colors = pd.read_csv(args.colors, sep="\t", names=("field", "value", "color"))

    # Load builds YAML.
    with open(args.builds, "r") as fh:
        builds = yaml.load(fh, Loader=yaml.FullLoader)

    # Collect a list of states/territories.
    states_by_build = {build: attributes["division"] for build, attributes in builds["builds"].items()}

    # Create the directory for state-level color files.
    colors_directory = pathlib.Path(args.colors_directory)
    colors_directory.mkdir(exist_ok=True)

    # For each state/territory, make a copy of the base colors, update the
    # current state's color, save the colors to a new file, and update the YAML
    # data structure to include the path to the custom color file.
    for build, state in states_by_build.items():
        build_colors = colors.copy()

        current_state_index = ((build_colors["field"] == "division") & (build_colors["value"] == state))
        # The current state already has an entry in the base colors, so update it.
        if build_colors[current_state_index].shape[0] == 1:
            build_colors.loc[
                current_state_index,
                "color"
            ] = args.state_color
        # The current state does not exist in the base colors.
        elif build_colors[current_state_index].shape[0] == 0:
            print(f"The state '{state}' is missing an entry in the base colors file '{args.colors}'.", file=sys.stderr)
        # Something has gone wrong, because the current state has multiple entries in base colors.
        else:
            print(f"The state '{state}' has multiple entries in the base colors file '{args.colors}'.", file=sys.stderr)

        # Define path to state-level color file.
        build_colors_path = colors_directory / pathlib.Path(f"{build}_colors.tsv")

        # Create the state-level color file.
        build_colors.to_csv(
            build_colors_path,
            sep="\t",
            header=False,
            index=False
        )

        # Update the YAML to include the custom build colors.
        builds["builds"][build]["colors"] = str(build_colors_path)

    # Save revised builds YAML with custom color paths.
    with open(args.revised_builds, "w") as oh:
        yaml.dump(builds, oh, default_flow_style=False)
