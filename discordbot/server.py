import docker


class MinecraftServerContainer:

    def __init__(self):
        self.docker_client = docker.from_env()
        self.container = find_container_by_name(self.docker_client, 'mc')

    def say(self, text):
        self.command(f'say {text}')

    def command(self, cmd):
        sock = self.container.attach_socket(params={"stdin": 1, "stdout": 1, "stderr": 1, "stream": 1})

        sock._writing = True

        def write(sock, str):
            while len(str) > 0:
                written = sock.write(str)
                str = str[written:]

        cmd = cmd + '\n'
        write(sock, bytes(cmd, encoding='utf-8'))
        # TODO: Read from the socket and return the command output
        sock.close()


def find_container_by_name(docker_client, name):
    containers = docker_client.containers.list()
    return next(filter(lambda container: container.name == name, containers))
