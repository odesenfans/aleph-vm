import shutil
from subprocess import run


class Bridge:
    def __init__(self, device_name: str):
        self.device_name = device_name

    @property
    def dummy_nic(self):
        return f"{self.device_name}-nic"

    def create(self):
        ip_command = shutil.which("ip")

        run([ip_command, "link", "add", self.device_name, "type", "bridge"])

        # Add a dummy device to ensure the bridge stays up and keeps its MAC address
        dummy_nic = self.dummy_nic
        run(
            [
                ip_command,
                "link",
                "add",
                dummy_nic,
                "type",
                "dummy",
            ]
        )
        run([ip_command, "link", "set", dummy_nic, "master", self.device_name])

        # Enable the bridge
        run([ip_command, "link", "set", dummy_nic, "up"])
        run([ip_command, "link", "set", self.device_name, "up"])

    def attach(self, device_name: str):
        ip_command = shutil.which("ip")

        run([ip_command, "link", "set", device_name, "down"])
        run([ip_command, "link", "set", device_name, "master", self.device_name])
        run([ip_command, "link", "set", device_name, "up"])

    def delete(self):
        ip_command = shutil.which("ip")

        def _set_down_and_delete(nic: str):
            run([ip_command, "link", "set", nic, "down"])
            run([ip_command, "link", "del", nic])

        _set_down_and_delete(self.dummy_nic)
        _set_down_and_delete(self.device_name)
