class API:
    def __init__(self):
        try:
            from core.strategy2 import Strategy
            self.strategy = Strategy()
        except Exception as e:
            self.strategy = None
            self.instance_exception = e

    def generate_actions(self, state):
        from core.api import Elevator, Passenger, Debug
        actions = []
        add_action = lambda action, args: actions.append({'command': action, 'args': args})
        dummy_action = lambda action, args: action

        my_passengers = state['my_passengers']
        enemy_passengers = state['enemy_passengers']
        my_elevators = state['my_elevators']
        enemy_elevators = state['enemy_elevators']
        my_elevators = [Elevator(add_action, **e) for e in my_elevators]
        enemy_elevators = [Elevator(dummy_action, **e) for e in enemy_elevators]
        my_passengers = [Passenger(add_action, **p) for p in my_passengers]
        enemy_passengers = [Passenger(add_action, **p) for p in enemy_passengers]

        debug = Debug(add_action)
        try:
            if self.strategy:
                self.strategy.set_debug(debug)
                self.strategy.on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers)
            else:
                if self.instance_exception:
                    debug.exception(self.instance_exception)
                    self.instance_exception = None
        except Exception as e:
            debug.exception(e)
        return actions
