# BLE detection with robot position at the moment of detection
std_msgs/Header header

# BLE device info
string device_id        # MAC address or uuid
string device_name      # advertised name
int8 rssi               # signal strength [dBm]
float32 tx_power        # advertised TX power (0.0 if not available)
string[] service_uuids    # advertised service UUIDs

# Robot pose at detection time (map frame)
geometry_msgs/Point position
geometry_msgs/Quaternion orientation
