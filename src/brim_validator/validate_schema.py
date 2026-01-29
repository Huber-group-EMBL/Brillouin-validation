import json
import zarr
import jsonschema
from pathlib import Path
import pprint
import argparse
import sys


def validate_brim_data(data_path: Path, schema_path: Path):
    """
    Validates the metadata of a Zarr (.brim) file against a JSON schema.

    Args:
        data_path: Path to the .brim Zarr data store.
        schema_path: Path to the JSON schema file.

    Returns:
        True if validation is successful, False otherwise.
    """
    # Import the builtins module to ensure we use the original open function

    print(f"Loading data from: {data_path}")
    print(f"Loading schema from: {schema_path}")


    try:
        # Consolidate metadata
        zarr.consolidate_metadata(data_path)
        print("Metadata consolidated successfully.")

        # Load the metadata
        with open(f"{data_path}/zarr.json", 'r') as f:
            metadata = json.load(f)
        print("Data loaded successfully.")
        
        # Load the JSON schema
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        print("Schema loaded successfully.")
        
        # Validate json schema first
        jsonschema.Draft6Validator.check_schema(schema)
        print("JSON schema is valid.")

        # Validate the metadata against the schema
        jsonschema.validate(instance=metadata, schema=schema)
        print("\nValidation successful!")
        return True

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check your file paths.")
        return False
    except jsonschema.exceptions.ValidationError as e:
        print("\nValidation FAILED.")
        print(f"Details: {e.message}")
        print("\n--- Data that failed validation ---")
        pprint.pprint(e.instance)

        # Print the other parameters from the error:
        print(e.validator_value)    

        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def main():
    """
    Parses CLI arguments and runs validation.
    """
    parser = argparse.ArgumentParser(
        description='Validate Zarr (.brim) file metadata against a JSON schema.'
    )
    
    parser.add_argument(
        'data_path',
        type=Path,
        help='Path to the .brim Zarr data store'
    )
    
    parser.add_argument(
        'schema_path',
        type=Path,
        help='Path to the JSON schema file'
    )
    
    args = parser.parse_args()
    
    success = validate_brim_data(data_path=args.data_path, schema_path=args.schema_path)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':

    main()
