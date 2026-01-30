# Custom Elastic Integrations

This repository contains source code for custom Elastic Integrations. It is structured to allow multiple integrations to coexist and be built individually using a shared build system.

## Repository Structure

```text
Elastic/integrations/
├── README.md                  <-- This file (General documentation)
└── packages/
    ├── build_package.py       <-- Generic build script
    │
    ├── unifi/                 <-- Source code for UniFi integration
    │   ├── manifest.yml
    │   ├── data_stream/
    │   └── ...
    │
    └── [new_integration]/     <-- Future integrations go here
        ├── manifest.yml
        └── ...
```

## How to Build an Integration

To upload an integration to Kibana, it must be packaged into a `.zip` file. We use a helper script to bundle the source directory into this format.

### Prerequisites

* Python 3
* pyyaml (`pip install pyyaml`)

### Build Instructions

1. Navigate to the packages directory:
   ```bash
   cd packages
   ```

2. Run the build script with the name of the folder you want to package:
   ```bash
   python build_package.py <package_name>
   ```

#### Examples:

Build the UniFi integration:
```bash
python build_package.py unifi
```

Build a future integration:
```bash
python build_package.py my-custom-app
```

> **Note:** The script will read the version from `manifest.yml` inside the target folder and generate a zip file (e.g., `unifi-0.0.14.zip`) inside the `packages/` directory.

## Installation

1. Log in to Kibana.
2. Navigate to **Management -> Integrations**.
3. Click **Upload integration**.
4. Select the generated `.zip` file.
5. Go to **Settings -> Install** to enable the integration.

## Developing a New Integration

1. Create a new folder inside `packages/` (e.g., `packages/my-app/`).
2. Ensure you have the required structure:
   * `manifest.yml` (Must contain name and version)
   * `data_stream/` directory
   * `docs/README.md` (The content displayed in the Kibana UI)
3. Run the build command above to package and test it.
