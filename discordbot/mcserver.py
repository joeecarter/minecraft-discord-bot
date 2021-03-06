import docker


class MinecraftServerContainer:

    def __init__(self):
        self.docker_client = docker.from_env()
        self.container = find_container_by_name(self.docker_client, 'mc')

    def say(self, text):
        self.command(f'say {text}')

    def restart_server(self):
        self.container.restart()

    def start_backup(self):
        self.command('backup start')

    def whitelist_add(self, username):
        self.command(f'whitelist add {username}')

    def command(self, cmd):
        sock = self.container.attach_socket(params={"stdin": 1, "stdout": 1, "stderr": 1, "stream": 1})

        sock._writing = True

        def write(sock, str):
            while len(str) > 0:
                written = sock.write(str)
                str = str[written:]

        # Clean out any new lines to stop arbitrary command injection
        cmd = cmd.replace('\n', ' ')

        # Press enter at the end of the command
        cmd = cmd + '\n'

        write(sock, bytes(cmd, encoding='utf-8'))
        # TODO: Read from the socket and return the command output
        sock.close()


def find_container_by_name(docker_client, name):
    all_containers = docker_client.containers.list()
    filtered_containers = list(filter(lambda container: container.name == name, all_containers))

    if len(filtered_containers) == 0:
        return None
    else:
        return filtered_containers[0]
