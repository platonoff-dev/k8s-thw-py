import sys
from pathlib import Path

import libvirt

from infra.vm import VirtManager
from utils import download_file


def start() -> None:
    distro_image_url = "https://cloud-images.ubuntu.com/plucky/current/plucky-server-cloudimg-arm64.img"
    distro_image_path = Path("runtime/downloads/os.qcow2")

    if not distro_image_path.exists():
        download_file(distro_image_url, distro_image_path)
    else:
        print(f"{distro_image_path} already exists, skipping download.")


    virt_conn = libvirt.open()
    virt_manager = VirtManager(virt_conn)

    network = virt_manager.ensure_network("k8s-thw")

    # Create vms for master nodes
    for i in range(1):
        virt_manager.create_vm(
            name=f"master-{i+1}",
            cpu=2,
            memory=2048,
            disk_size=20,
            network=network.name(),
        )

    # Create vms for worker nodes
    for i in range(2):
        virt_manager.create_vm(
            name=f"worker-{i+1}",
            cpu=2,
            memory=2048,
            disk_size=20,
            network=network.name(),
        )


def clean() -> None:
    pass


def main():
    operation = sys.argv[1]
    match operation:
        case "start":
            start()
        case "clean":
            clean()
        case _:
            print(f"Unknown operation: {operation}")


if __name__ == "__main__":
    main()
