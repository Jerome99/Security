# Integration Packages Source

This directory contains the source code for individual Elastic Integrations and the build tools required to package them for deployment.

## Directory Contents

* **`build_package.py`**: A Python utility to package integration source folders into installable `.zip` files.
* **Integration Folders**: Individual directories (e.g., `unifi/`) containing the source assets for specific integrations.

## Creating a New Integration

To add a new integration, create a new folder in this directory with the following minimum structure:

```text
packages/
└── <integration_name>/
    ├── manifest.yml        # Required: Metadata (name, version, title)
    ├── data_stream/        # Required: Data collection definitions
    │   └── <stream_name>/
    │       ├── manifest.yml
    │       └── elasticsearch/
    │           └── ingest_pipeline/
    └── docs/               # Optional: Documentation assets
        └── README.md
```

### `manifest.yml` Requirements
The `manifest.yml` at the root of your integration folder must contain at least a `version` field, as the build script uses this to name the output file.

```yaml
format_version: 1.0.0
version: 0.0.1
name: my-integration
title: My Custom Integration
description: Collects logs from my custom application
```

## Building a Package

Use the `build_package.py` script to create a deployable zip file.

1.  **Install Requirements:**
    ```bash
    pip install pyyaml
    ```

2.  **Run Build Command:**
    ```bash
    # Usage: python build_package.py <folder_name>
    python build_package.py unifi
    ```

3.  **Output:**
    The script will generate a zip file in this directory (e.g., `unifi-0.0.1.zip`). This file is ready to be uploaded to Kibana.
