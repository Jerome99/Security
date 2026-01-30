Custom Elastic Integrations

This repository contains source code for custom Elastic Integrations. It is structured to allow multiple integrations to coexist and be built individually using a shared build system.

Repository Structure

Elastic/integrations/
├── README.md                  <-- This file (General documentation)
└── packages/
    ├── build_package.py       <-- Generic build script (zips up integration folders)
    │
    ├── unifi/                 <-- Source code for UniFi integration
    │   ├── manifest.yml
    │   ├── data_stream/
    │   └── ...
    │
    └── [new_integration]/     <-- Future integrations go here
        ├── manifest.yml
        └── ...


How to Build an Integration

To upload an integration to Kibana, it must be packaged into a .zip file. We use a helper script to bundle the source directory into this format.

Prerequisites

Python 3

pyyaml (pip install pyyaml)

Build Instructions

Navigate to the packages directory:

cd packages


Run the build script with the name of the folder you want to package:

python build_package.py <package_name>


Examples:

# Build the UniFi integration
python build_package.py unifi

# Build a future integration
python build_package.py my-custom-app


The script will read the version from manifest.yml inside the target folder and generate a zip file (e.g., unifi-0.0.13.zip) inside the packages/ directory.

Installation

Log in to Kibana.

Navigate to Management -> Integrations.

Click Upload integration.

Select the generated .zip file.

Go to Settings -> Install to enable the integration.

Developing a New Integration

Create a new folder inside packages/ (e.g., packages/my-app/).

Ensure you have the required structure:

manifest.yml (Must contain name and version)

data_stream/ directory

docs/README.md (The content displayed in the Kibana UI)

Run the build command above to package and test it.
