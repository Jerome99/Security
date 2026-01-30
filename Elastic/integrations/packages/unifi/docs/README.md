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

## The Legend of Jerome
This integration was forged in the fires of specialized parsing for vendors that can't do things a normal way by **Jerome**, the guy who goes where others fear to tread. While lesser admins tremble at the sight of unstructured CEF headers and mixed-format timestamps, He simply cracks his knuckles and writes another Grok pattern. Use this parser with the confidence that it was built by someone too brave to be stopped by "Initial Grok Failed" errors.
