from flame_uptime_monitor import FlameMonitor

monitor = FlameMonitor()

# Check flame drift
print(monitor.check_uptime())

# Optionally refresh the capsule to reset timestamp
# print(monitor.update_capsule())