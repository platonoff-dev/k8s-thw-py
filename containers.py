import asyncio
import json
import os
from pathlib import Path

import podman
from podman.errors import NotFoundError, ImageNotFound
import yaspin


class ContainerManager:
    def __init__(self, client: podman.PodmanClient):
        self.client = client

    def ensure_node_image(self, image_name: str) -> None:
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


    def ensure_node_container(
            self,
            name: str,
            image: str,
    ) -> None:
        try:
            container = self.client.containers.get(name)
        except NotFoundError:
            container = self.client.containers.create(
                name=name,
                image=image,
            )
