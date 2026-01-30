# Ubiquiti UniFi Integration

The Ubiquiti UniFi integration collects and parses logs from UniFi Consoles (UDM, UDR, USG) and UniFi Network Controllers. It normalizes these logs into Elastic Common Schema (ECS) fields, allowing for unified analysis of network traffic, firewall events, and system alerts.

## Compatibility

This integration has been tested with:

* UniFi Network Application 7.x and 8.x
* UniFi Dream Machine (UDM) / Pro / SE
* UniFi Security Gateway (USG)

## Data Streams

The integration collects logs through the following data streams:

* **log**: Collects general system logs, firewall events, and intrusion detection alerts (IPS/IDS) sent via Syslog.

## Requirements

* **Elastic Agent**: Must be installed on a host capable of receiving Syslog traffic from your UniFi devices.
* **Syslog Configuration**: You must configure your UniFi Console to send remote logs to the Elastic Agent's IP address and port.

### UniFi Configuration

1. Log in to your UniFi Network Application.
2. Navigate to **Settings > System > Advanced**.
3. Enable **Remote Logging**.
4. Enter the **IP Address** of the Elastic Agent.
5. Enter the **Port** (default: `514` in the UI but if keeping the default config for this integration use `5614`).
6. Set the **Logging Level** (recommended: `Debug` for firewall logs, `Auto` for general).
7. Click **Apply Changes**.

## Ingest Pipeline Processing

The integration uses an Elasticsearch Ingest Pipeline to parse raw Syslog messages. Key processing steps include:

1. **Grok Parsing**: The pipeline handles multiple log formats:
   * Standard Syslog with CEF extensions (Common Event Format).
   * Standard Syslog with process names and PIDs.
   * Kernel-level firewall logs (e.g., `[WAN_IN-default-D]`).
   * UniFi device name events.

2. **Key-Value Extraction**:
   * Parses `key=value` pairs from the message body.
   * **Note**: Certain raw fields (`MAC`, `PREC`, `ID`, `TOS`, `TTL`, `LEN`, `URGP`, `WINDOW`, `RES`) are explicitly excluded during extraction to reduce noise, focusing on core network identity fields.

3. **ECS Mapping**: Renames vendor-specific fields (e.g., `SRC`, `DST`, `SPT`, `DPT`, `PROTO`) to standard ECS fields.

4. **Event Classification**: A painless script analyzes the `rule.name` to determine the event outcome:
   * **Allow/Success**: If the rule name contains `LAN_IN` or `WAN_IN`.
   * **Deny/Failure**: If the rule name contains `DROP`, `REJECT`, or `DENY`.
   * **Info**: All other events.

5. **Enrichment**:
   * **GeoIP**: Adds `source.geo` and `destination.geo` location data.
   * **Community ID**: Generates a network flow hash for correlation.

## ECS Field Mappings

The following table lists the field mappings from the raw UniFi logs to the Elastic Common Schema (ECS).

| ECS Field | UniFi Raw Field | Description | 
| ----- | ----- | ----- | 
| `@timestamp` | `syslog_timestamp` | Derived from the syslog header. | 
| `host.hostname` | `SYSLOGHOST` | The hostname of the UniFi device. | 
| `process.name` | `process.name` | Name of the process generating the log (e.g., `sudo`, `kernel`). | 
| `process.pid` | `process.pid` | Process ID. | 
| `rule.name` | `rule.name` | The firewall rule triggered (e.g., `WAN_IN-default-D`). | 
| `source.ip` | `SRC`, `UNIFIclientIp`, `unifi.src` | Source IP address. | 
| `source.port` | `SPT` | Source port number. | 
| `source.mac` | `MAC`, `UNIFIclientMac` | Source MAC address. | 
| `source.geo.*` | - | Geolocation derived from Source IP. | 
| `destination.ip` | `DST`, `unifi.dst` | Destination IP address. | 
| `destination.port` | `DPT` | Destination port number. | 
| `destination.geo.*` | - | Geolocation derived from Destination IP. | 
| `network.transport` | `PROTO` | Protocol (e.g., TCP, UDP). | 
| `network.community_id` | - | Hash of the network flow tuple. | 
| `network.name` | `UNIFIwifiName` | Name of the WiFi network (SSID). | 
| `user.name` | `UNIFIadmin` | Administrative user associated with the event. | 
| `event.reason` | `msg` | Text description of the event. | 
| `event.action` | - | Derived from rule name (e.g., `allow`, `deny`). | 
| `event.outcome` | - | Derived from rule name (e.g., `success`, `failure`). | 
| `observer.vendor` | `observer.vendor` | Vendor (from CEF headers). | 
| `observer.product` | `observer.product` | Product name (from CEF headers). | 
| `observer.version` | `observer.version` | Firmware version (from CEF headers). | 

## Example Log

**Raw Syslog:**
