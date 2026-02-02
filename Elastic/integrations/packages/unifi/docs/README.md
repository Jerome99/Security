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
   * **AP Tag Parsing**: Extracts MAC addresses and product versions from AP tags (e.g., `788a20dc0ace,UAP-AC-Pro-Gen2...`).

2. **Key-Value Extraction**:
   * Parses `key=value` pairs from the message body.
   * **Note**: Certain raw fields (`MAC`, `PREC`, `ID`, `TOS`, `TTL`, `LEN`, `URGP`, `WINDOW`, `RES`) are explicitly excluded during extraction to reduce noise, focusing on core network identity fields.

3. **ECS Mapping**: Renames vendor-specific fields (e.g., `SRC`, `DST`, `SPT`, `DPT`, `PROTO`) to standard ECS fields.

4. **Event Categorization & Enrichment**:
   * **Firewall Rules**:
     * **Allow/Success**: If the rule name contains `LAN_IN` or `WAN_IN`.
     * **Deny/Failure**: If the rule name contains `DROP`, `REJECT`, or `DENY`.
   * **Dynamic Categorization**: events are categorized based on `unifi.cat`:
     * **Security/Firewall**: Maps to `network` and `firewall` (or `security`).
     * **Intrusion Prevention**: Maps to `network` and `intrusion_detection` and sets `event.kind` to `alert`.
     * **System**: Maps to `configuration`.
     * **Internet**: Maps to `network` and `availability`.
   * **Admin Access**: Logins (Code 1000) are mapped to `authentication` events.
   * **Alert Promotion**: High severity events (Severity >= 7) are automatically promoted to `event.kind: alert`.
   * **WAN Failover**: Extracts ISP, IP, and interface details for WAN failover events.
   * **Wireless**: Extracts BSSID and Signal Strength (RSSI) for WiFi events.
   * **IP Conflicts**: Detects IP conflicts and sets `event.type` to `error` and `conflict`.

5. **Geographic & Network Enrichment**:
   * **GeoIP**: Adds `source.geo` and `destination.geo` location data.
   * **Community ID**: Generates a network flow hash for correlation.

## ECS Field Mappings

The following table lists the field mappings from the raw UniFi logs to the Elastic Common Schema (ECS).

| ECS Field | UniFi Raw Field | Description | 
| ----- | ----- | ----- | 
| `@timestamp` | `syslog_timestamp`, `iso_timestamp` | Derived from the syslog header. | 
| `host.hostname` | `SYSLOGHOST`, `UNIFIhost` | The hostname of the UniFi device. | 
| `process.name` | `process.name` | Name of the process generating the log (e.g., `sudo`, `kernel`). | 
| `process.pid` | `process.pid` | Process ID. | 
| `rule.name` | `rule.name` | The firewall rule triggered (e.g., `WAN_IN-default-D`). | 
| `source.ip` | `SRC`, `UNIFIclientIp`, `unifi.src` | Source IP address. | 
| `source.port` | `SPT` | Source port number. | 
| `source.mac` | `MAC`, `UNIFIclientMac` | Source MAC address. | 
| `source.hostname` | `UNIFIclientHostname` | Source Hostname. | 
| `source.geo.*` | - | Geolocation derived from Source IP. | 
| `destination.ip` | `DST`, `unifi.dst` | Destination IP address. | 
| `destination.port` | `DPT` | Destination port number. | 
| `destination.geo.*` | - | Geolocation derived from Destination IP. | 
| `network.transport` | `PROTO` | Protocol (e.g., TCP, UDP). | 
| `network.community_id` | - | Hash of the network flow tuple. | 
| `network.name` | `UNIFIwifiName` | Name of the WiFi network (SSID). | 
| `wireless.bssid` | `UNIFIbssid` | Wireless BSSID. | 
| `wireless.signal.strength` | `UNIFIWiFiRssi` | Wireless Signal Strength (RSSI). | 
| `user.name` | `UNIFIadmin`, `suser` | Administrative user associated with the event. | 
| `event.reason` | `msg`, `reason` | Text description of the event. | 
| `event.action` | - | Derived from rule name (e.g., `allow`, `deny`) or login events. | 
| `event.outcome` | - | Derived from rule name (e.g., `success`, `failure`). | 
| `observer.vendor` | `observer.vendor` | Vendor (from CEF headers). | 
| `observer.product` | `observer.product` | Product name (from CEF headers). | 
| `observer.version` | `observer.version` | Firmware version (from CEF headers). | 
| `observer.name` | `UNIFIdeviceName` | Name of the observing UniFi device. | 
| `observer.ip` | `UNIFIdeviceIp` | IP of the observing UniFi device. | 
| `observer.mac` | `UNIFIdeviceMac` | MAC of the observing UniFi device. | 
| `observer.ingress.interface.name` | `deviceInboundInterface` | Inbound interface for the event. | 
| `observer.egress.interface.name` | `deviceOutboundInterface`, `UNIFIfailoverWanName` | Outbound interface or WAN failover interface. | 
| `observer.egress.interface.alias` | `UNIFIfailoverWanIsp` | ISP Name during failover events. | 
| `observer.egress.ip` | `UNIFIfailoverWanIp` | WAN IP during failover events. | 
| `labels.device_model` | `UNIFIdeviceModel` | Model of the UniFi device. | 
| `labels.access_method` | `UNIFIaccessMethod` | Access method used (e.g., for logins). | 
| `error.message` | - | Set during parsing failures or IP conflicts. | 

## Example Log

**Raw Syslog:**
```log
'Oct 27 10:00:00 UDM-Pro kernel: [WAN_IN-default-D]IN=eth4 OUT=eth0 MAC=aa:bb:cc:dd:ee:ff:11:22:33:44:55:66:08:00 SRC=1.2.3.4 DST=192.168.1.100 LEN=60 TOS=0x00 PREC=0x00 TTL=52 ID=34324 DF PROTO=TCP SPT=443 DPT=56789 WINDOW=65535 RES=0x00 SYN URGP=0'
```

**Mapped Event (JSON):**

```json
{
  "@timestamp": "2023-10-27T10:00:00.000Z",
  "host": {
    "hostname": "UDM-Pro"
  },
  "rule": {
    "name": "WAN_IN-default-D"
  },
  "event": {
    "kind": "event",
    "category": "network",
    "action": "allow",
    "outcome": "success"
  },
  "source": {
    "ip": "1.2.3.4",
    "port": 443,
    "geo": {
      "country_iso_code": "US"
    }
  },
  "destination": {
    "ip": "192.168.1.100",
    "port": 56789
  },
  "network": {
    "transport": "tcp",
    "community_id": "1:hO+sN4H+MG5MY/8h4...="
  }
}
```
