import os
import sys
import zipfile
import yaml  # Requires: pip install pyyaml

def build_package(package_name):
    """
    Builds an Elastic Integration package into a zip file.
    Expects to be run from the 'packages/' directory.
    """
    
    # 1. Setup Paths
    current_dir = os.getcwd()
    package_dir = os.path.join(current_dir, package_name)
    manifest_path = os.path.join(package_dir, 'manifest.yml')

    # 2. Validation
    if not os.path.isdir(package_dir):
        print(f"Error: Directory '{package_name}' not found in {current_dir}")
        sys.exit(1)

    if not os.path.isfile(manifest_path):
        print(f"Error: 'manifest.yml' not found in {package_dir}")
        print("Please ensure the integration has a valid manifest file.")
        sys.exit(1)

    # 3. Read Version from Manifest
    print(f"Reading configuration for: {package_name}")
    try:
        with open(manifest_path, 'r') as f:
            manifest_data = yaml.safe_load(f)
            version = manifest_data.get('version')
            
            if not version:
                print("Error: 'version' field is missing from manifest.yml")
                sys.exit(1)
    except Exception as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)

    # 4. Create Zip File
    output_filename = f"{package_name}-{version}.zip"
    output_path = os.path.join(current_dir, output_filename)

    print(f"Building package version: {version}")
    print(f"Target file: {output_filename}")

    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the package directory and add files to the zip
            for root, dirs, files in os.walk(package_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Calculate the relative path inside the zip file
                    # This ensures 'manifest.yml' is at the root of the zip, 
                    # not inside a folder named 'unifi/'
                    archive_name = os.path.relpath(file_path, package_dir)
                    
                    print(f"  Adding: {archive_name}")
                    zipf.write(file_path, archive_name)

        print("-" * 30)
        print(f"Success! Package created at: {output_path}")
        print("-" * 30)

    except Exception as e:
        print(f"Error creating zip archive: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_package.py <package_name>")
        print("Example: python build_package.py unifi")
        sys.exit(1)

    target_package = sys.argv[1]
    build_package(target_package)
