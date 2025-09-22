import os

import jinja2
import libvirt

class VirtManager:
    conn: libvirt.virConnect

    def __init__(self, conn: libvirt.virConnect) -> None:
        self.conn = conn

    def create_vm(self, name: str, cpu: int, memory: int, disk_size: int, network: str) -> libvirt.virDomain:
        domain_xml = jinja2.Environment(
            loader=jinja2.FileSystemLoader("infra/templates")
        ).get_template("domain.xml.j2").render(
            name=name,
            cpu=cpu,
            memory=memory,
            disk_image=f"{os.getcwd()}/runtime/downloads/os.qcow2",
            disk_size=disk_size,
            network_name=network,
        )

        return self.conn.createXML(domain_xml)

    def delete_vm(self, name: str) -> None:
        domain = self.conn.lookupByName(name)
        domain.destroy()
        domain.undefine()

    def create_network(self, name: str) -> libvirt.virNetwork:
        network_xml = jinja2.Environment(
            loader=jinja2.FileSystemLoader("infra/templates")
        ).get_template("network.xml.j2").render(
            name=name,
        )

        network = self.conn.networkCreateXML(network_xml)
        return network

    def delete_network(self, name: str) -> None:
        network = self.conn.networkLookupByName(name)
        network.destroy()
        network.undefine()

    def ensure_network(self, name: str) -> libvirt.virNetwork:
        try:
            network = self.conn.networkLookupByName(name)
        except libvirt.libvirtError:
            network = self.create_network(name)
        return network

    def list_vms(self) -> list:
        return []
