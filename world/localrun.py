# coding=utf-8
import json
import os
from coreRunner import settings

class WorldHandler(object):

    def __init__(self):
        from coreRunner.api import API
        self.api = API()
        self.ticks_count = int(os.environ.get('TICKS_COUNT', 7200))
        self.result = []
        self.client_player = {}
        from core.api import API
        self.red_client = API()
        from core.api2 import API
        self.blue_client = API()

    @staticmethod
    def write_result(data):
        f = open(
            '{}/../visualizer/game.js'.format(os.path.dirname(os.path.realpath(__file__))), 'w')
        f.write("var data = ")
        f.write(json.dumps(data))
        f.write(";")
        f.close()

    def start(self):
        self.api.create_players(self.red_client, self.blue_client)
        for _ in range(0, self.ticks_count):
            if _ % 1000 == 0:
                print(_)
            blue_message = self.blue_client.generate_actions(
                self.api.get_world_state_for(self.blue_client))
            red_message = self.red_client.generate_actions(
                self.api.get_world_state_for(self.red_client))
            self.api.apply_commands(blue_message, self.blue_client)
            self.api.apply_commands(red_message, self.red_client)
            self.api.tick()
            self.result.append(self.api.get_visio_state())
        try:
            json_str=str(self.result[-1]).split("scores': {")[1].split("}, 'waiting_passengers")[0]
            print (json_str)
            self.write_result({
                'config': settings.BUILDING_VISIO,
                'game_data': self.result,
                'players': {
                    "FIRST_PLAYER": "1",
                    "SECOND_PLAYER": "2",
                }
            })
        except Exception as e:
            print(e)


world_handler = WorldHandler()
world_handler.start()
print("end")
