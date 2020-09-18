# Custom profile for SPHERES augur builds

## Auspice configuration

Update the following fields in the auspice configuration file, `spheres_profile/auspice_config.json`, to reflect the current repository and maintainers.

  - `build_url`
  - `maintainers`

## Snakemake configuration

The original profile was tested on a SLURM cluster.
Modify how Snakemake is executed by editing the `spheres_profile/config.yaml` file.
Update the `cluster` directive to work with the style of cluster where this workflow will be run.
See [Snakemake's profile examples about different cluster types](https://github.com/Snakemake-Profiles/doc) and [documentation about configuring cluster execution](https://snakemake.readthedocs.io/en/stable/executing/cluster.html), for more details.

By default, this profile uses conda and [Snakemake's integrated package management](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#integrated-package-management) to ensure each rule is executed in the correct environment.
To enable this feature, [install miniconda](https://docs.conda.io/en/latest/miniconda.html) prior to running the workflow.
To disable this feature, remove the `use-conda` directive from `spheres_profile/config.yaml`.
To update Nextstrain dependencies or add your own custom dependencies, modify `spheres_profile/conda.yaml`.
The next time you run the workflow, Snakemake will detect these modifications and rebuild your conda environment automatically.
For more details, see [the Nextstrain team's description of how to manage software in Snakemake workflows](https://discussion.nextstrain.org/t/make-reproducible-workflows-with-conda-environments-and-pinned-augur-versions/107).

## State- and territory-level colors and descriptions

Each state- and territory-level build has its own custom color profile and descriptions for display in auspice.
Color profiles use a base color scheme based on [Emma Hodcroft's colors for her Southern USA builds](https://raw.githubusercontent.com/emmahodcroft/south-usa-sarscov2/master/profiles/south-central/colors.tsv).
For each build, the given build's state or territory is given a red color to clearly distinguish that division from other divisions in the auspice view.
To build these custom build-level color schemes, run the following command from the top-level of the repository.

```python
python3 spheres_profile/build_state_colors.py \
    --colors spheres_profile/colors.tsv \
    --builds spheres_profile/builds.yaml \
    --colors-directory spheres_profile/state_colors/ \
    --revised-builds spheres_profile/revised_builds.yaml
```

Then modify the revised builds, as needed, for readability and replace the original builds YAML with this new file.

To build the custom build-level description Markdown files, run the following command from the top-level of the repository.

```python
python3 spheres_profile/build_state_descriptions.py \
    --builds spheres_profile/builds.yaml \
    --descriptions-directory spheres_profile/state_descriptions/ \
    --revised-builds spheres_profile/revised_builds.yaml
```

As with the revised builds for colors, copy the updated `builds` section of the revised builds YAML produced by the command above into the main `builds.yaml` file.
Modify the contents of files in `spheres_profile/state_descriptions/` to customize the description for each state or territory.
