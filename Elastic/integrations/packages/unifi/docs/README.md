# UniFi Custom Integration

This integration parses logs from Ubiquiti UniFi Controllers (UDM/USG).

## Setup
1. **Install Integration**: Upload this package to Kibana.
2. **Add to Policy**: Add the "UniFi Networks" integration to your Elastic Agent policy.
3. **Configure**: 
    * Choose **UDP** or **TCP**.
    * Set your **Timezone** (e.g., `America/New_York`) to ensure accurate timestamps.
    * Point your UniFi Controller's Remote Syslog to the Elastic Agent IP on port **5614**.

## Features
- **Configurable**: Supports UDP/TCP, custom ports, and timezones.
- **Firewall Parsing**: Maps Allow/Deny/Reject to ECS `event.action` and `event.outcome`.
- **Enrichment**: Adds GeoIP and Community ID.
- **SSL**: Supports TCP with SSL.


