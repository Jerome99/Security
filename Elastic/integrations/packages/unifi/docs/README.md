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
5. Enter the **Port** (default: `514` or typically `5614` for this custom integrations).
6. Set the **Logging Level** (recommended: `Debug` for firewall logs, `Auto` for general).
7. Click **Apply Changes**.

## Ingest Pipeline Processing

The integration uses an Elasticsearch Ingest Pipeline to parse raw Syslog messages. Key processing steps include:

1. **Grok Parsing**: Extracts timestamps, process names (e.g., `kernel`, `sudo`), and the raw message body.
2. **Firewall Pattern Matching**: specifically parses kernel logs for packet filtering events (e.g., `[WAN_IN-default-D]`) to extract:
   * Source/Destination IPs and Ports
   * MAC addresses
   * Interfaces (in/out)
   * Protocols (TCP/UDP/ICMP)
3. **ECS Mapping**: Renames vendor-specific fields to standard ECS fields (see table below).
4. **GeoIP Enrichment**: Adds `source.geo` and `destination.geo` location data based on IP addresses.
5. **Network Direction**: Infers `network.direction` (inbound, outbound, internal) based on the firewall rule name and interface.

## ECS Field Mappings

The following table lists the field mappings from the raw UniFi logs to the Elastic Common Schema (ECS).

| ECS Field | UniFi Raw / Description | Example | 
| ----- | ----- | ----- | 
| `@timestamp` | derived from syslog timestamp | `2023-10-27T10:00:00.000Z` | 
| `event.module` | `unifi` | `unifi` | 
| `event.dataset` | `unifi.log` | `unifi.log` | 
| `event.action` | Rule action (derived) | `allow`, `deny`, `drop` | 
| `event.category` | Fixed value | `network` | 
| `event.kind` | Fixed value | `event` | 
| `event.outcome` | Derived from action | `success` (allow), `failure` (drop) | 
| `source.ip` | `SRC` | `192.168.1.50` | 
| `source.port` | `SPT` | `54322` | 
| `source.mac` | `MAC` (parsed source) | `aa:bb:cc:dd:ee:ff` | 
| `destination.ip` | `DST` | `8.8.8.8` | 
| `destination.port` | `DPT` | `53` | 
| `destination.mac` | `MAC` (parsed dest) | `11:22:33:44:55:66` | 
| `network.transport` | `PROTO` | `UDP` | 
| `network.protocol` | `PROTO` (lowercase) | `udp` | 
| `observer.ingress.interface` | `IN` | `eth0` | 
| `observer.egress.interface` | `OUT` | `eth1` | 
| `rule.name` | Rule identifier from log prefix | `WAN_IN-default-D` | 
| `log.level` | Syslog severity | `warning`, `info` | 
| `host.hostname` | Syslog hostname | `UDM-Pro` | 

## Example Log

**Raw Syslog:**

```text
<4>Oct 27 10:00:00 UDM-Pro kernel: [WAN_IN-default-D]IN=eth4 OUT=eth0 MAC=aa:bb:cc:dd:ee:ff:11:22:33:44:55:66:08:00 SRC=1.2.3.4 DST=192.168.1.100 LEN=60 TOS=0x00 PREC=0x00 TTL=52 ID=34324 DF PROTO=TCP SPT=443 DPT=56789 WINDOW=65535 RES=0x00 SYN URGP=0
