import sys
import podman

import containers


def start() -> None:
    podman_client =  podman.PodmanClient()
    manager = containers.ContainerManager(podman_client)
    
    image = manager.ensure_node_image("k8s-thw-node")
    network = manager.ensure_network("k8s-thw-net")

    for i in range(1):
        container = manager.ensure_node_container(
            name=f"k8s-thw-master-node-{i+1}",
            image=image.tags[0],
            network=network.name,
        )
    
    for i in range(3):
        container = manager.ensure_node_container(
            name=f"k8s-thw-worker-node-{i+1}",
            image=image.tags[0],
            network=network.name,
        )

    podman_client.close()

def clean() -> None:
    podman_client =  podman.PodmanClient()
    manager = containers.ContainerManager(podman_client)

    for i in range(1):
        manager.remove_container(f"k8s-thw-master-node-{i+1}")
    
    for i in range(3):
        manager.remove_container(f"k8s-thw-worker-node-{i+1}")
    
    manager.remove_network("k8s-thw-net")

    podman_client.close()

def main():
    op = sys.argv[1] if len(sys.argv) > 1 else "start"
    if op == "start":
        start()
    elif op == "clean":
        clean()
    else:
        print(f"Unknown operation: {op}")
        sys.exit(1)

if __name__ == "__main__":
    main()
