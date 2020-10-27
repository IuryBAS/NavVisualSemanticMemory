'''

from ai2thor.controller import Controller, distance
from .base_controller import BaseController
import random
import networkx as nx



class OnlineController(BaseController):

    def __init__(
        self, 
        grid_size=0.25,
        fov=100,
        debug_mode=True,
        actions=["MoveAhead", "RotateLeft", "RotateRight", "LookUp", "LookDown", "OpenObject"],
        visualize=True,
    ):

        super(OnlineController, self).__init__()
        self.grid_size = grid_size
        self.grid = None
        self.graph = None
        self.controller = None
        self.actions = actions
        self.rotation = [0, 45, 90, 135, 180, 225, 270, 315]
        self.horizons = [0, 30]
        self.debug_mode = debug_mode
        self.fov = fov

        self.y = None
        self.last_event = None
        #self.controller = Controller()

        self.visualize = visualize
        self.scene_name = None
        self.state = None
        self.last_action_success = True
        self.last_event = None

        #self.h5py = importlib.import_module("h5py")
        #self.nx = importlib.import_module("networkx")
        #self.json_graph_loader = importlib.import_module("networkx.readwrite")


    def start(self):
        if self.visualize:
            self.controller.start()
            event = self.controller.step(
                dict(action="Initialize", gridSize=self.grid_size, fieldOfView=self.fov)
            )
        self.last_event = self.controller.last_event
        return event
        
    def step(self, action):
        print(action)
        event = self.controller.step(action)
        self.last_event = self.controller.last_event
        return event

    def reset(self, scene_name):
        self.controller.reset(scene_name)
        self.last_event = self.controller.last_event

    def all_objects(self):
        objects = self.controller.last_event.metadata['objects']
        self.last_event = self.controller.last_event
        return [o['objectId'] for o in objects]

    def randomize_state(self):
        reachable_points = self.controller.step(dict(action='GetReachablePositions'))
        point = random.choice(reachable_points.metadata['reachablePositions'])
        print(point)
        rotation = random.choice([0, 90, 180, 270])
        horizon = random.choice([0, 30, 330])
        self.controller.step(dict(action='TeleportFull', x=point['x'], y=point['y'], z=point['z'], rotation=rotation, horizon=horizon))
        self.last_event = self.controller.last_event

'''