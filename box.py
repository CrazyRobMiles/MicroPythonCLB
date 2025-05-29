from device_configurator import DeviceConfigurator
import sys
from clb import CLB

clb = CLB()

config = DeviceConfigurator(
    clb.settings,
    on_settings_loaded=lambda s: print("Settings loaded"),
    on_file_error=lambda e: print(f"File Error:{e}"),
    on_waiting_for_host=lambda: print("Waiting for serial connection"),
    on_settings_received=lambda s: print("Settings received from serial connection"),
    on_get_request_received=lambda : print("Get request received from serial connection")
)
 
# Force online if required for initial setup
#result = config.setup(force_online=True)
result = config.setup()

print(clb.settings)

clb.setup()

clb.describe()

try:
    while True:
        clb.update()
        clb.update_console()
except Exception as e:
    print(e)
    sys.print_exception(e)
    clb.teardown()
