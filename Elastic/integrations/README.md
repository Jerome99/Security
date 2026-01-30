# Elastic Integrations Repository

This repository contains custom Elastic Integrations.

## Repository Structure

```text
Elastic/integrations/
├── README.md                  <-- This file
└── packages/
    ├── build_package.py       <-- Script to bundle integrations
    └── unifi/                 <-- Source code for UniFi integration
        ├── manifest.yml
        ├── data_stream/
        └── ...

## How to Build an Integration
To upload an integration to Kibana, it must be packaged into a .zip file with a specific internal versioned folder structure. We use a helper script to generate this artifact.

Prerequisites
Python 3 installed.

PyYAML installed (pip install pyyaml).

Build Instructions
Open your terminal and navigate to the packages directory:

Bash
cd packages
Run the build script. By default, it builds the unifi package:

Bash
python build_package.py
To build a different package, pass the folder name as an argument:

Bash
python build_package.py my-other-package
The script will generate a zip file (e.g., unifi-0.0.13.zip) inside the packages/ directory.

How to Install
Log in to Kibana.

Navigate to Management -> Integrations.

Click the Upload integration button (top right).

Select the .zip file you just generated.

Once uploaded, go to Settings -> Install to enable it.
