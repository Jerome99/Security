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
