
def console_printer(msg_id, msg_text):
    print(f"[{msg_id}] {msg_text}")

class CLBManager:
    version = "0.0.0"
    dependencies = []

    # Universal states (base definitions)
    STATE_OK = "OK"
    
    def __init__(self, defaults=None):
        self.defaults = defaults or {}
        self.state = "not connected"
        self.settings = {}
        self.enabled = True
        self._status_text = "Not initialized"
        self._status_id = 0
        self._message_receivers = []

    def get_defaults(self):
        d = self.defaults.copy()
        d["enabled"] = False
        return d

    def get_version(self):
        return self.__class__.version

    def get_dependencies(self):
        return self.__class__.dependencies

    def setup(self, settings_dict):
        merged = self.get_defaults()
        merged.update(settings_dict)
        self.settings = merged
        self.enabled = self.settings.get("enabled", False)

        if not self.enabled:
            self.state = "disabled"
            self.set_status(1000, "Disabled by config")
        else:
            self.state = "connecting"
            self.set_status(1001, "Setting up...")

    def update(self):
        pass

    def get_status(self):
        return self._status_text

    def set_status(self, msg_id, msg_text):
        self._status_id = msg_id
        self._status_text = msg_text
        for handler in self._message_receivers:
            handler(msg_id, msg_text)

    def add_message_handler(self, handler):
        if handler not in self._message_receivers:
            self._message_receivers.append(handler)

    def remove_message_handler(self, handler):
        if handler in self._message_receivers:
            self._message_receivers.remove(handler)

