from pathlib import Path

import podman
from podman.errors import NotFound, ImageNotFound
from podman.domain.containers import Container
from podman.domain.images import Image
from podman.domain.networks import Network
import yaspin

from podman_client import PodmanClient


class ContainerManager:
    def __init__(self, client: podman.PodmanClient):
        self.client = client

    def ensure_node_image(self, image_name: str) -> Image:
        print("Ensuring node images are built")
        try:
            image = self.client.images.get(image_name)
            print("Node image already exists.")
        except ImageNotFound:
            print("Node image not found")
            with yaspin.yaspin(text="Building node image...", color="cyan"):
                image, logs = self.client.images.build(
                    path=str(Path.cwd()),
                    dockerfile=Path.cwd() / "Dockerfile.node",
                    tag=image_name,
                )

            print("Node image built successfully.")
        return image


    def ensure_node_container(
            self,
            name: str,
            image: str,
            network: str,
    ) -> Container:
        print(f"Ensuring container '{name}' exists")
        try:
            container = self.client.containers.get(name)
        except NotFound:
            print(f"Container '{name}' not found. Creating")
            container = self.client.containers.create(
                name=name,
                image=image,
                networks={network: {"aliases": [f"{name}.k8s-thw.local"]}},
                network_mode="bridge",
                hostname=name,
            )
        
        if container.status != "running":
            print(f"Starting container '{name}'")
            container.start()
        
        return container
    
    def ensure_network(self, name: str) -> Network:
        print(f"Ensuring network '{name}' exists")
        try:
            network = self.client.networks.get(name)
        except NotFound:
            print(f"Network '{name}' not found. Creating")
            network = self.client.networks.create(
                name=name,
                dns_enabled=True,
            )
        
        return network

    def remove_container(self, name: str) -> None:
        print(f"Removing container '{name}' if it exists")
        try:
            container = self.client.containers.get(name)
            container.kill()
            container.remove()
            print(f"Container '{name}' removed.")
        except NotFound:
            print(f"Container '{name}' does not exist. No action taken.")
    
    def remove_network(self, name: str) -> None:
        print(f"Removing network '{name}' if it exists")
        try:
            network = self.client.networks.get(name)
            network.remove()
            print(f"Network '{name}' removed.")
        except NotFound:
            print(f"Network '{name}' does not exist. No action taken.")