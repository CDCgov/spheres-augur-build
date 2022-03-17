# SPHERES augur builds

## Overview

This repo contains build files for the [SPHERES builds](https://nextstrain.org/groups/spheres) hosted by the [Nextstrain](https://nextstrain.org/) and a description the upstream subsampling steps performed prior to the analysis pipeline.

## Usage

Clone this repository.

```bash
git clone https://github.com/CDCgov/spheres-augur-build.git
cd spheres-augur-build/
```

Select the appropriate build in the `spheres_profile` directory and copy it's contents to a directory named `build` in your [ncov](https://github.com/nextstrain/ncov) directory.
Modify build definitions, as needed, in `builds.yaml` and `config.yaml` files
By default, each build requires specificly named data files to be placed in the `ncov/data` directory
```
"references" data
Files: data/references_sequences.fasta and data/references_metadata.tsv
Description: Sequence and metadata for Wuhan reference sequences. Provided with Nextstrain ncov repository
```

```
"global_background" data
Files: data/global_background.fasta and data/global_background.tsv
Description: Sequence and metadata for non-USA background sequences.  User must provide these files.
```

```
"usa" data
Files: data/usa_background.fasta and data/usa_background.tsv
Description: Sequence and metadata for USA background sequences.  User must provide these files.
```

```
"focus" data
Files: data/<BUILD_NAME>.fasta and data/<BUILD NAME>.tsv
Description: Sequence and metadata for focus division.  User must provide these files.
```

Run the workflow.

```bash
snakemake --profile build/
```

View the resulting builds through [auspice.us](https://auspice.us/) or with [auspice](https://github.com/nextstrain/auspice) installed on your local machine.

```bash
auspice view
```


## Workflow Maintenance

The Nextstrain team constantly improvies the the Nextstrain workflow.  We recommend that you regularly update your ncov workflow to take advantage of new feature additions.
This repo is no longer dependent on a specific nextstrain ncov augur distribution, so these build files can are compatible with Docker based Nextstrain workflows and can be updated independently of the ncov workflow.

## CDC SPHERES build subsampling

The build files hosted in this repo are uses to generate the publicly hosted [SPHERES builds](https://nextstrain.org/groups/spheres), however most of the subsampling operations take place upstream of the Nextstrain ncov workflow. This allows for improved run-time performance and greater portability. This section describes the subsampling used to produce the [SPHERES builds](https://nextstrain.org/groups/spheres).  All input data files described here are oversampled relative to the requirements in the build file to provide some flexibility in downstream subsampling by the Nextstrain augur pipeline

#### Shared filters

All included data is prepared using these rules prior to any subsampling operations
- Sequence and metadata is derived from Sars-CoV-2 sequence data provided by [the GISAID Initiative](https://www.gisaid.org/)
- In the case of duplicated accession numbers (EPI_ISL_), only the most recently submitted version is retained
- Additional metadata is added from the [Nextstrain curation](https://raw.githubusercontent.com/nextstrain/ncov-ingest/master/source-data/gisaid_annotations.tsv)
- Sequence length must exceed 27000 base pairs
- Sequences are selected randomly from all sequences matching the sampling criteria
- If an insufficient number of sequences are available for a given subsampling target, that data partition will contain all available sequences meeting that criteria


#### Global background

This data provides global context to the USA sequences. The `global_background` files are shared between all builds on a given week, but is re-calculated each week.

- 25 sequences collected within the last two months from each global region ("Africa" "Asia" "Europe" "North America" "Oceania" "South America" )
- 25 sequences collected prior to last two months from each global region ("Africa" "Asia" "Europe" "North America" "Oceania" "South America" )

#### USA background

This data is provides USA context to the focal sequences. The `usa_background` files are shared between all builds on a given week, but is re-calculated each week

- 10 sequences collected within the last two months from each of the included states, unincorporated territory of the United States, and Palau
- 10 sequences collected prior to last two months from each of the included states, unincorporated territory of the United States, and Palau

#### Focal data

This data is densely sampled focal data of the build. These data files are specific to each build and are not shared with other builds.

- 1000 sequences collected within the last two months from the focal division
- 1000 sequences collected prior to last two months from the focal division

#### USA (whole country)

This data provides an overview of circulating and historical sequences in the United States, unincorporated territory of the United States, and Palau. These files are used for the "usa" build only

- 25 sequences collected within the last two months from each of the included states, unincorporated territory of the United States, and Palau
- 25 sequences collected prior to last two months from each of the included states, unincorporated territory of the United States, and Palau

#### NS3 (National Sars-Cov-2 Strain Surveillance)

This data provides an overview of circulating and historical sequences in the United States and unincorporated territory of the United States generated by the NS3 project. These files are used for the "ns3" build only

- 25 sequences collected as part of the NS3 project within the last two months from each of the included states, unincorporated territory of the United States, and Palau
- 25 sequences collected as part of the NS3 project prior to last two months from each of the included states, unincorporated territory of the United States, and Palau



## Public Domain Standard Notice
This repository constitutes a work of the United States Government and is not
subject to domestic copyright protection under 17 USC § 105. This repository is in
the public domain within the United States, and copyright and related rights in
the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this repository will be released under the CC0 dedication. By
submitting a pull request you are agreeing to comply with this waiver of
copyright interest.

## License Standard Notice
The repository utilizes code licensed under the terms of the Apache Software
License and therefore is licensed under ASL v2 or later.

This source code in this repository is free: you can redistribute it and/or modify it under
the terms of the Apache Software License version 2, or (at your option) any
later version.

This source code in this repository is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the Apache Software License for more details.

You should have received a copy of the Apache Software License along with this
program. If not, see http://www.apache.org/licenses/LICENSE-2.0.html

The source code forked from other open source projects will inherit its license.

## Privacy Standard Notice
This repository contains only non-sensitive, publicly available data and
information. All material and community participation is covered by the
[Disclaimer](https://github.com/CDCgov/template/blob/master/DISCLAIMER.md)
and [Code of Conduct](https://github.com/CDCgov/template/blob/master/code-of-conduct.md).
For more information about CDC's privacy policy, please visit [http://www.cdc.gov/other/privacy.html](https://www.cdc.gov/other/privacy.html).

## Contributing Standard Notice
Anyone is encouraged to contribute to the repository by [forking](https://help.github.com/articles/fork-a-repo)
and submitting a pull request. (If you are new to GitHub, you might start with a
[basic tutorial](https://help.github.com/articles/set-up-git).) By contributing
to this project, you grant a world-wide, royalty-free, perpetual, irrevocable,
non-exclusive, transferable license to all users under the terms of the
[Apache Software License v2](http://www.apache.org/licenses/LICENSE-2.0.html) or
later.

All comments, messages, pull requests, and other submissions received through
CDC including this GitHub page may be subject to applicable federal law, including but not limited to the Federal Records Act, and may be archived. Learn more at [http://www.cdc.gov/other/privacy.html](http://www.cdc.gov/other/privacy.html).

## Records Management Standard Notice
This repository is not a source of government records, but is a copy to increase
collaboration and collaborative potential. All government records will be
published through the [CDC web site](http://www.cdc.gov).

## Additional Standard Notices
Please refer to [CDC's Template Repository](https://github.com/CDCgov/template)
for more information about [contributing to this repository](https://github.com/CDCgov/template/blob/master/CONTRIBUTING.md),
[public domain notices and disclaimers](https://github.com/CDCgov/template/blob/master/DISCLAIMER.md),
and [code of conduct](https://github.com/CDCgov/template/blob/master/code-of-conduct.md).
