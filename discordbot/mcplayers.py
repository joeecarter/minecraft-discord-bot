import time
from threading import Thread, Lock
from mcstatus import MinecraftServer


class MinecraftServerPlayers(Thread):

    def __init__(self, hostname):
        super(MinecraftServerPlayers, self).__init__(daemon=True)
        self.server = MinecraftServer(hostname)
        self.players = self.__fetch_online_players()
        self.callback_join = None
        self.callback_leave = None
        self.__lock = Lock()

    def run(self):
        print('[MinecraftServerPlayers] Starting player leave/join loop')

        while True:
            time.sleep(60)

            with self.__lock:
                new_players = self.__fetch_online_players()
                left = diff(self.players, new_players)
                joined = diff(new_players, self.players)

                self.players = new_players

            for player in joined:
                print(f'{player} joined the server')
                if self.callback_join:
                    self.callback_join(player)

            for player in left:
                print(f'{player} left the server')
                if self.callback_leave:
                    self.callback_leave(player)

    def get(self):
        with self.__lock:
            players = self.players
        return players

    def on_player_join(self, callback):
        self.callback_join = callback

    def on_player_leave(self, callback):
        self.callback_leave = callback

    def __fetch_online_players(self):
        status = self.server.status()
        players = status.players.sample

        if players is None:
            return []

        return list(map(lambda player: player.name, players))


def diff(original, changed):
    d = []
    for x in original:
        if x not in changed:
            d.append(x)
    return d
