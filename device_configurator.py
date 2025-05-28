# device_configurator.py

import time
import json
import os
from machine import Pin
import sys

try:
    from machine import unique_id
    uid_bytes = unique_id()
    print("Machine Unique ID set")
except:
    print("Used default ID")
    uid_bytes = b'\x01\x02\x03\x04\x05\x06\x07\x08'

MAGIC = b'\xDE\xAD\xBE\xEF'

class DeviceConfigurator:
    def __init__(
        self,
        settings: dict,
        settings_file="/settings.txt",
        safe_pin=1,  # Use GPIO number (e.g., 1 for GP1)
        use_obfuscation=False,
        on_settings_loaded=None,
        on_file_error=None,
        on_waiting_for_host=None,
        on_settings_received=None,
        on_get_request_received=None
    ):
        self.settings = settings
        self.settings_file = settings_file
        self.safe_pin = safe_pin
        self.use_obfuscation = use_obfuscation

        self.on_settings_loaded = on_settings_loaded
        self.on_file_error = on_file_error
        self.on_waiting_for_host = on_waiting_for_host
        self.on_settings_received = on_settings_received
        self.on_get_request_received = on_get_request_received

    def file_exists(self):
        try:
            os.stat(self.settings_file)
            return True
        except OSError:
            return False

    def _prng(self, seed):
        state = seed
        while True:
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            yield state & 0xFF

    def _xor_data(self, data, seed):
        rng = self._prng(seed)
        return bytes([b ^ next(rng) for b in data])

    def load(self):
        try:
            with open(self.settings_file, "rb" if self.use_obfuscation else "r") as f:
                data = f.read()

            if self.use_obfuscation:
                if data[:4] != MAGIC:
                    raise ValueError("Invalid magic header")
                obfuscated = data[4:]
                seed = sum(uid_bytes)
                json_bytes = self._xor_data(obfuscated, seed)
                loaded = json.loads(json_bytes.decode("utf-8"))
            else:
                print("Loaded data:", data)
                loaded = json.loads(data)

            # Assume: self.settings = full default settings
            #         loaded = settings read from file
            
            for section in loaded:
                if section in self.settings:
                    self.settings[section].update(loaded[section])
                    
            # If we have added new sections - save everything
                    
            if len(loaded) != len(self.settings):
                self.save()

            return True
        except Exception as e:
            raise e

    def save(self):
        try:
            if self.use_obfuscation:
                json_bytes = json.dumps(self.settings).encode("utf-8")
                seed = sum(uid_bytes)
                obfuscated = self._xor_data(json_bytes, seed)
                with open(self.settings_file, "wb") as f:
                    f.write(MAGIC + obfuscated)
            else:
                with open(self.settings_file, "w") as f:
                    json.dump(self.settings, f)
            return True
        except Exception as e:
            raise e

    def wait_for_settings(self):
        while True:
            try:
                line = sys.stdin.readline().strip()
                print("got a line")
                if line == "GET":
                    if self.on_get_request_received():
                        self.on_get_request_received()
                    print((json.dumps(self.settings) + "\n").encode("utf-8"))
                    continue
                if line.startswith("{"):
                    self.settings.clear()
                    self.settings.update(json.loads(line))
                    self.save()
                    if self.on_settings_received:
                        self.on_settings_received(self.settings)
                    return self.settings
            except Exception as e:
                print("Serial error:", e)
            time.sleep(0.1)

    def setup(self,force_online=False):
        
        if(self.safe_pin):
            pin = Pin(self.safe_pin, Pin.IN, Pin.PULL_UP)
            safe_pin_value = pin.value
        else:
            safe_pin_value=True
        
        if self.file_exists():
            try:
                if self.load():
                    print("Settings loaded")
                    if self.on_settings_loaded:
                        self.on_settings_loaded(self.settings)
            except Exception as e:
                print("Error loading settings:", e)
                if self.on_file_error:
                    self.on_file_error(e)
                force_online = True
        else:
            force_online = True

        if not safe_pin_value or force_online:
            print("Entering setup mode")
            if self.on_waiting_for_host:
                self.on_waiting_for_host()
            return self.wait_for_settings()

        return self.settings


