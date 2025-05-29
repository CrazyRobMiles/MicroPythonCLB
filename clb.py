import os
import json
import sys
import select

class CLB:
    def __init__(self, settings_file="/settings.txt"):
        self.settings_file = settings_file
        self.manager_entries = self._load_managers()
        self.settings = {
            name: mgr.get_defaults()
            for name, mgr in self.manager_entries
        }
        self.status = {}
        self.command_dict = {}
        self._input_buffer = ""

    def _load_managers(self):
        entries = []
        for file in os.listdir("/managers"):
            print(f"Found:{file}")
            if file.endswith("_manager.py") and not file.startswith("_"):
                module_name = file[:-3]
                full_name = f"managers.{module_name}"
                print(f"Loading: {full_name}")
                try:
                    module = __import__(full_name)
                    for part in full_name.split(".")[1:]:
                        module = getattr(module, part)
                    manager_class = getattr(module, "Manager")
                    manager_instance = manager_class()
                    manager_name = module_name[:-8]  # strip '_manager'
                    entries.append((manager_name, manager_instance))
                except Exception as e:
                    sys.print_exception(e)
                    print(f"Failed to load {module_name}: {e}")
        return entries

    def setup(self):
        if self.settings_file in os.listdir("/"):
            try:
                with open(self.settings_file, "r") as f:
                    saved = json.load(f)
                    for name, mgr in self.manager_entries:
                        if name in saved:
                            self.settings[name].update(saved[name])
                        else:
                            self.settings[name] = mgr.get_defaults()
            except Exception as e:
                print("Error loading settings file:", e)

        manager_lookup = {name: mgr for name, mgr in self.manager_entries}

        for name, mgr in self.manager_entries:
            deps = mgr.get_dependencies()
            if hasattr(mgr, "dependency_instances"):
                mgr.dependency_instances = [manager_lookup[d] for d in deps if d in manager_lookup]

        from managers.base import console_printer
        for name, mgr in self.manager_entries:
            mgr.add_message_handler(console_printer)
            mgr.setup(self.settings[name])
            self.status[name] = mgr.get_status()

        for name, mgr in self.manager_entries:
            if hasattr(mgr, "get_commands"):
                self.register_command_set(mgr.get_commands())

        self.register_command_set([
            ("status", self.describe, "Show manager status"),
            ("reset", self.reset, "Reset settings to defaults"),
            ("help", self.show_help, "List available commands"),
            ("set", self.set_setting, "Set a configuration value: set manager_setting=value"),
            ("settings", self.show_settings, "Display all current setting values"),
            ("teardown", self.teardown, "Tear down all managers and release resources")
        ])

    def register_command_set(self, command_list):
        for entry in command_list:
            if isinstance(entry, tuple) and len(entry) == 3:
                name, func, desc = entry
                self.command_dict[name] = {
                    "handler": func,
                    "description": desc
                }

    def update(self):
        for name, mgr in self.manager_entries:
            mgr.update()
            self.status[name] = mgr.get_status()

    def update_console(self):
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            char = sys.stdin.read(1)
            if char == '\n':
                self.handle_command(self._input_buffer.strip())
                self._input_buffer = ""
            else:
                self._input_buffer += char

    def reset(self):
        try:
            with open(self.settings_file, "w") as f:
                json.dump({name: mgr.get_defaults() for name, mgr in self.manager_entries}, f)
            print("Settings reset to defaults.")
        except Exception as e:
            print("Error resetting settings:", e)

    def teardown(self):
        for name, mgr in self.manager_entries:
            if hasattr(mgr, "teardown"):
                try:
                    mgr.teardown()
                    print(f"Torn down manager: {name}")
                except Exception as e:
                    print(f"Error tearing down manager {name}: {e}")

    def get_versions(self):
        return {
            name: {
                "version": mgr.get_version(),
                "dependencies": mgr.get_dependencies()
            }
            for name, mgr in self.manager_entries
        }

    def describe(self):
        print("\nConnected Little Box Status Report")
        print("----------------------------------")
        for name, mgr in self.manager_entries:
            print(f"{name:<10} v{mgr.get_version():<8} state: {mgr.state:<16} enabled: {mgr.enabled}  deps: {mgr.get_dependencies()}")

    def show_help(self):
        print("\nAvailable Commands:")
        for name in sorted(self.command_dict.keys()):
            desc = self.command_dict[name]["description"]
            print(f"  {name:<10} - {desc}")

    def handle_command(self, command_line):
        if not command_line:
            return
        parts = command_line.strip().split()
        cmd = parts[0]
        args = parts[1:]
        entry = self.command_dict.get(cmd)
        if entry:
            try:
                entry["handler"](*args)
            except Exception as e:
                print(f"Error executing command '{cmd}': {e}")
        else:
            print(f"Unknown command: {cmd}")

    def set_setting(self, *args):
        if len(args) != 1 or "=" not in args[0]:
            print("Usage: set manager_setting=value")
            return

        setting_expr = args[0]
        key_part, value_str = setting_expr.split("=", 1)
        if "_" not in key_part:
            print("Invalid format. Use manager_setting=value")
            return

        manager_name, setting_name = key_part.split("_", 1)

        if manager_name not in self.settings:
            print(f"Unknown manager: {manager_name}")
            return

        settings_dict = self.settings[manager_name]

        if setting_name not in settings_dict:
            print(f"Unknown setting: {setting_name} in manager {manager_name}")
            return

        original_value = settings_dict[setting_name]
        try:
            if isinstance(original_value, bool):
                settings_dict[setting_name] = value_str.lower() in ("true", "1", "yes", "on")
            elif isinstance(original_value, int):
                settings_dict[setting_name] = int(value_str)
            elif isinstance(original_value, float):
                settings_dict[setting_name] = float(value_str)
            else:
                settings_dict[setting_name] = value_str
            print(f"✅ {manager_name}.{setting_name} updated to {settings_dict[setting_name]} ({type(settings_dict[setting_name]).__name__})")
        except Exception as e:
            print(f"❌ Failed to convert value: {e}")

    def show_settings(self):
        print("\nCurrent Settings:")
        for manager_name, settings in self.settings.items():
            print(f"[{manager_name}]")
            for key, val in settings.items():
                print(f"  {key:<12}: {val} ({type(val).__name__})")
