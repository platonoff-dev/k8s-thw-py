import libvirt

class VirtManager:
    conn: libvirt.virConnect

    def __init__(self, conn: libvirt.virConnect) -> None:
        pass

    def create_vm(self, name: str, cpu: int, memory: int, disk_size: int) -> None:
        pass

    def delete_vm(self, name: str) -> None:
        pass

    def create_netowrk(self, name: str) -> None:
        pass

    def delete_network(self, name: str) -> None:
        pass

    def list_vms(self) -> list:
        return []
