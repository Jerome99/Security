# How to Build an Integration

To upload an integration to Kibana, it must be packaged into a `.zip` file with a specific internal versioned folder structure. We use a helper script to generate this artifact.

## Prerequisites

Before building, ensure you have the following installed:

* Python 3
* PyYAML (`pip install pyyaml`)

## Build Instructions

1.  Open your terminal and navigate to the `packages` directory:

    ```bash
    cd packages
    ```

2.  Run the build script. By default, this builds the **unifi** package:

    ```bash
    python build_package.py
    ```

    > **Note:** To build a different package, pass the folder name as an argument:
    >
    > ```bash
    > python build_package.py my-other-package
    > ```

3.  The script will generate a zip file (e.g., `unifi-0.0.13.zip`) inside the `packages/` directory.

## How to Install

1.  Log in to **Kibana**.
2.  Navigate to **Management** -> **Integrations**.
3.  Click the **Upload integration** button (located in the top right).
4.  Select the `.zip` file you just generated.
5.  Once uploaded, go to **Settings** -> **Install** to enable it.
