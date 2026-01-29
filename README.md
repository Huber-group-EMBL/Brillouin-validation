# Brillouin file format (`.brim`) validation

This repository provides a tool to validate Brillouin file format (`.brim`) files, as defined in the [Brillouin specification](https://github.com/prevedel-lab/Brillouin-standard-file/tree/main).

## Design considerations

We want validation of `.brim` files to be:
- **Implementable in multiple programming languages**: The validation logic should be simple enough to be easily ported to different programming languages.
- **Performant**: Validating a `.brim` file should be efficient, even for large files.

## Approach

The validator focuses on the file structure (presence and location of certain key files), and the properties of individual zarr arrays.

Here is how we go about it:

- Consolidate the zarr metadata into a single JSON structure for easier validation.
- Validate the consolidated metadata against the Brillouin specification using the JSON schema provided in [`schemas/`](schemas/).

The validation is provided here in python as a proof of concept but should therefore be portable in any language that:

- Can read zarr files
- Implements the experimental zarr metadata consolidation feature
- Can validate JSON against a JSON schema

## Usage

### Installation

You can install the validator from this GitHub repository:

```bash
pip install git+https://github.com/Huber-group-EMBL/Brillouin-validation.git
```

### Running the validator

Once installed, you can run the validator using the `brim-validate` command:

```bash
brim-validate <data_path> <schema_path>
```

For example:

```bash
brim-validate example_data/zebrafish_eye_confocal.brim schemas/brim_v0.1_schema.json
```

Alternatively, you can run it as a Python module:

```bash
python -m brim_validator.validate_schema <data_path> <schema_path>
```

## Contribution

This proof of concept was initially developed during the 3C-CoDash EMBL Event 2026.