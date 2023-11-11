from direct.showbase.ShowBase import ShowBase
from math import tan, radians, cos, sin
from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionTube, BitMask32
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import WindowProperties, DepthOffsetAttrib
#from panda3d.core import *
import simplepbr
from game_object import *
import json
import mercator

#loadPrcFileData("", "load-file-type p3assimp")

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        #simplepbr.init()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.win.setClearColor(Vec4(0.8, 1, 1, 1))

        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        render.setShaderAuto()

        #self.roads = loader.loadModel("asset_pipeline/built/roads/models/highways/roads-asset.bam")
        #self.roads.reparentTo(render)
        self.buildings = loader.loadModel("asset_pipeline/built/buildings/models/buildings/palazzi.egg")
        self.buildings.reparentTo(render)
        #self.buildings.set_p(90);
        self.roads = loader.loadModel("asset_pipeline/built/roads/models/highways/streets.egg")
        self.roads.reparentTo(render)
        self.water = loader.loadModel("asset_pipeline/built/buildings/models/buildings/tiber.egg")
        self.water.reparentTo(render)
        #self.water.set_p(90);
        #self.roads=render.attachNewNode(loader.loadModel("asset_pipeline/input/roads-asset/sample_streets.obj"))
        #self.roads.setAttrib(DepthOffsetAttrib.make(1))
        #self.roads.set_p(90);
        # self.tiberriver.setCollideMask(BitMask32.bit(1))
        # print(self.tiberriver.node())

        #self.collision_node = self.buildings.find("**/collision")
        #self.setup_collision()

        self.setBackgroundColor(0.53, 0.80, 0.92, 1)

        self.camera.setPos(0, 0, 500)
        self.camera.setP(-90)

        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False,
            "rot-left" : False,
            "rot-right" : False,
            "increment" : False,
            "decrement" : False
        }

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])
        self.accept('q', self.updateKeyMap, ['rot-left', True])
        self.accept('q-up', self.updateKeyMap, ['rot-left', False])
        self.accept('e', self.updateKeyMap, ['rot-right', True])
        self.accept('e-up', self.updateKeyMap, ['rot-right', False])
        self.accept('z', self.updateKeyMap, ["increment", True])
        self.accept('z-up', self.updateKeyMap, ["increment", False])
        self.accept('x', self.updateKeyMap, ["decrement", True])
        self.accept('x-up', self.updateKeyMap, ["decrement", False])

        self.theta = 89  # Initial pitch angle

        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()
        # self.handler = CollisionHandlerPusher()

        self.pusher.setHorizontal(True)

        jsonpath = "../walkintiber/assets/json/sample.json"
        with open(jsonpath) as file:
            tubes = json.load(file)

        converter = mercator.Mercator()

        for way in tubes.values():
            for n in range(len(way["nodes"])):
                nodeStart = way["nodes"][n]
                nodeEnd = way["nodes"][(n+1)%len(way["nodes"])]
                wallSolid = CollisionTube(converter.get_x(nodeStart[0]), converter.get_y(nodeStart[1]), 0, 
                                          converter.get_x(nodeEnd[0]), converter.get_y(nodeEnd[1]), 0, 0.2)
                wallNode = CollisionNode("wall")
                wallNode.addSolid(wallSolid)
                wall = render.attachNewNode(wallNode)

        """ wallSolid = CollisionTube(-96.8479919433594, 92.4960021972656, 0, 
                                  -96.0609893798828, 113.390998840332, 0, 0.5)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)

        wallSolid = CollisionTube(-114.804992675781, 114.97200012207, 0,
                                  -117.738990783691, 93.7429962158203, 0, 0.5)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)

        wallSolid = CollisionTube(-114.804992675781, 114.97200012207, 0,
                                  -96.0609893798828, 113.390998840332, 0, 0.5)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)

        wallSolid = CollisionTube(-96.8479919433594, 92.4960021972656, 0, 
                                  -117.738990783691, 93.7429962158203, 0, 0.5)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode) """

        wall.show()

        self.updateTask = taskMgr.add(self.update, "update")
        #self.updateTask = taskMgr.add(self.updateCameraTask, "UpdateCameraTask")
        self.updateTask = taskMgr.add(self.updateCameraTaskBack2, "UpdateCameraTaskBack2")

        self.player = Player()

        #self.tempEnemy = WalkingEnemy(Vec3(-500, 0, 0))

        # Add the character's collision node to the traverser and the handler.
        #self.cTrav.addCollider(self.player.collider, self.pusher)
        #self.pusher.addCollider(self.player.collider, self.render)

        self.cTrav.showCollisions(render)

        # The environment's collision polygons should have been loaded as "into" objects,
        # so you don't need to add them to the traverser.
        # If you want to make them visible for debugging, you can loop through them like this:
        self.collision_nodes = self.buildings.findAllMatches('**/+CollisionNode')
        for collision_node in self.collision_nodes:
            collision_node.show()

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState


    def update(self, task):
        dt = globalClock.getDt()

        self.player.update(self.keyMap, dt)

        #self.tempEnemy.update(self.player, dt)

        if self.keyMap["increment"]:
            self.increment_theta()
        if self.keyMap["decrement"]:
            self.decrement_theta()

        return task.cont
    
    def updateCameraTaskBack(self, task):
        # Get the player's current position
        playerPos = self.player.actor.getPos()

        # Define the vertical offset and distance behind the player for the camera
        cameraZOffset = 2  # The height from the player position
        cameraDistance = 10  # How far behind the player the camera should be

        # Calculate the new camera position. We're positioning the camera directly above the player
        # and then moving it backward by cameraDistance amount, and up by cameraZOffset amount.
        newCameraPos = playerPos + Vec3(-cameraDistance, 0, cameraZOffset)

        # Set the camera's position to this new point
        self.camera.setPos(newCameraPos)

        # Now, we'll have the camera look at the player. It automatically adjusts the pitch to -45 degrees
        # because of how we positioned it above. It keeps the camera centered on the player's position.
        self.camera.lookAt(playerPos)

        # The task should continue running each frame; returning Task.cont will ensure this.
        return Task.cont
    
    def increment_theta(self):
        """Increment the angle theta."""
        if self.theta < 89:
            self.theta += 0.5 # Or any other value you consider appropriate for each key press

    def decrement_theta(self):
        """Decrement the angle theta."""
        if self.theta > 30:
            self.theta -= 0.5 # Or any other value you consider appropriate for each key press

    def updateCameraTaskBack2(self, task):
        # Get the player's current position
        playerPos = self.player.actor.getPos()
        playerH = radians(self.player.actor.getH())
        # print(playerH)

        # Convert theta to radians, then calculate the tangent of theta
        theta_radians = radians(self.theta)
        tangent_theta = tan(theta_radians)

        # Calculate camera parameters based on theta
        cameraZOffset = tangent_theta + 1.
        cameraDistance = (90 - self.theta)/5  # Or some function of theta, if it's not a 1:1 relationship

        # Calculate the new camera position based on player position and camera parameters
        newCameraPos = playerPos + Vec3(-cameraDistance*cos(playerH), -cameraDistance*sin(playerH), cameraZOffset)

        # Set the camera's position and have it look at the player
        self.camera.setPos(newCameraPos)
        self.camera.lookAt(playerPos)

        return task.cont  # Continue the task indefinitely

    def updateCameraTask(self, task):
        # Get the player's current position
        playerPos = self.player.actor.getPos()

        # Update the camera's position to match the player's X and Y coordinates, but keep its own Z coordinate.
        self.camera.setPos(playerPos.getX(), playerPos.getY(), self.camera.getZ())

        # The task should continue running each frame; returning Task.cont will ensure this.
        return Task.cont
    
    def setup_collision(self):
        # Initialize the collision traverser.
        self.cTrav = CollisionTraverser()

        # Initialize the collision handler.
        self.pusher = CollisionHandlerPusher()

        # Setup a collision node for the character, for example a sphere
        self.collide_node_path = self.render.attachNewNode(CollisionNode('charCollideNode'))
        self.collide_node_path.node().addSolid(CollisionSphere(0, 0, 0, 1))

        # Set the collision mask
        self.collide_node_path.node().setIntoCollideMask(BitMask32.allOff())
        self.collide_node_path.node().setFromCollideMask(BitMask32.bit(0))

        # Attach the collision node to the traverser and the handler
        self.cTrav.addCollider(self.collide_node_path, self.pusher)
        self.pusher.addCollider(self.collide_node_path, self.render)

        # Show the collision nodes for debugging purposes
        self.collision_node.show()



game = Game()
game.run()