import os
import yaml # Requires: pip install pyyaml
import shutil
import sys

def build_integration(package_name):
    # Ensure we are in the packages directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = os.path.join(base_dir, package_name)
    
    manifest_path = os.path.join(package_dir, "manifest.yml")

    if not os.path.exists(manifest_path):
        print(f"Error: Could not find manifest at {manifest_path}")
        return

    # 1. Read Version and Name from manifest
    with open(manifest_path, "r") as f:
        manifest = yaml.safe_load(f)
    
    name = manifest['name']
    version = manifest['version']
    folder_name = f"{name}-{version}"
    zip_name = f"{folder_name}.zip"
    build_temp_path = os.path.join(base_dir, "build_temp")
    output_zip_path = os.path.join(base_dir, zip_name)

    print(f"Building {zip_name} from {package_dir}...")

    # 2. Create a temporary build folder structure {name}-{version}/
    if os.path.exists(build_temp_path):
        shutil.rmtree(build_temp_path)
    
    dest_folder = os.path.join(build_temp_path, folder_name)
    os.makedirs(dest_folder)

    # 3. Copy files (excluding hidden files and the build script itself)
    for item in os.listdir(package_dir):
        if item.startswith(".") or item == "__pycache__":
            continue
        
        src = os.path.join(package_dir, item)
        dst = os.path.join(dest_folder, item)
        
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # 4. Zip it up
    # make_archive expects the base_name (filename w/o extension), format, and root_dir
    shutil.make_archive(os.path.join(base_dir, folder_name), 'zip', build_temp_path)
    
    # 5. Cleanup
    shutil.rmtree(build_temp_path)
    print(f"Success! Created: {output_zip_path}")

if __name__ == "__main__":
    # Default to 'unifi' if no argument provided
    target = sys.argv[1] if len(sys.argv) > 1 else "unifi"
    build_integration(target)
