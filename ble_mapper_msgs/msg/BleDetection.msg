# BLE detection
std_msgs/Header header

# BLE device info
string device_id        # MAC address or uuid
string device_name      # advertised name
int8 rssi               # signal strength [dBm]
float32 tx_power        # advertised TX power (0.0 if not available)
string[] service_uuids    # advertised service UUIDs

