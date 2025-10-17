import podman

import containers


def start() -> None:
    pass

def clean() -> None:
    pass

def main():
    podman_client =  podman.PodmanClient()
    manager = containers.ContainerManager(podman_client)
    manager.ensure_node_image("k8s-thw-node")

    for i in range(1):
        pass

    podman_client.close()


if __name__ == "__main__":
    main()
