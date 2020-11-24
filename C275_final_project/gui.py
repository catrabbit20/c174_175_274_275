import pygame, random, math, time
from pygame.locals import *
import objects, graph, collision
from utilities import Timer, euclidD
from objects import *

class GUI():
    def __init__(self, screen_rect, bg_img):

        # Setup Screen and background image
        self.screen = pygame.display.set_mode((screen_rect.w, screen_rect.h))
        self.screen_rect = screen_rect
        self.bg_img = bg_img.convert()

        # Init starfield (layer above background, slowly scrolls on loop)
        self.star_field = \
            objects.object_types["starField"](
            speed = -0.3,
            surface = self.screen)

        # Init player ship, add it to shipGroup
        self.player_ship = objects.object_types["ship"](
            position = (50,50),
            activate=True)
        ship.Ship.shipGroup.add(self.player_ship)

        # Init the alien infested asteroid, add to infestedGroup
        self.infested_asteroid = objects.object_types["infested"](
            position = (self.screen_rect.w-150,200))
        infested.Infested.infestedGroup.add(self.infested_asteroid)

        # Init space station, add to spaceStation group
        self.space_station = objects.object_types["spaceStation"](
            position = (75,self.screen_rect.h/2))
        spaceStation.SpaceStation.spaceStationGroup.add(self.space_station)

        # Init scorekeeping, add to score group
        self.score = objects.object_types["score"](
                position = (self.screen_rect.w,0),
                time = time.time(),
                spaceStation = self.space_station)
        score.Score.scoreGroup.add(self.score)

        # For the graph section
        self.paths = None
        self.graph_timer = Timer(150/1000, self.graph_update)

        # TODO: remove this demo feature
        self.OPTIONS = 0

    def p1_button(self, e, down):
        '''
        Handles user input, allowing player_ship to be piloted

        Args:
        event e, a pygame event
        down, a boolean representing key event type (down==True)
        '''
        if e == K_RIGHT: \
                self.player_ship.k_right = down*self.player_ship.turn_speed
        elif e == K_LEFT: \
                self.player_ship.k_left = down*self.player_ship.turn_speed
        elif e == K_UP: \
                self.player_ship.k_up = down*self.player_ship.acceleration
        elif e == K_DOWN: \
                self.player_ship.k_down = down*self.player_ship.acceleration
        elif e == K_SPACE and down: self.player_ship.fire_missile()
        elif e == K_TAB and down: 
            self.OPTIONS = (self.OPTIONS+1)%4
            print(self.OPTIONS)
            
    def asteroid_spawn(self):
        '''
        Generates an asteroid offscreen right which will travel towards
        spacestation.

        Consecutive asteroids will have semi-uniform motion, defined by
        the speed and direction. Asteroid spawn positions will be 
        divided into rough 'sections' to help create a uniform asteroid field.        
        '''
        # Divide the screen into rough sections (1.25 asteroid height)
        spacing_height = asteroid.Asteroid.sprite.get_rect().h * 1.25
        # Determine how many integer sections fit on screen
        spacing_number = int(self.screen_rect.h / spacing_height)

        # The second term positions the asteroid offscreen by some amount
        x = self.screen_rect.w + random.randrange(10, 50)
        # First term offsets the spacing so asteroids do not spawn
        # offscreen in the vertical axis. Second term determines 
        # which 'section' to spawn asteroid in.
        y = 0.5 * spacing_height + \
            spacing_height * random.randint(0,spacing_number)

        # Field movement properties
        speed = random.triangular(0.5, 3, 2)
        direction = random.uniform(170,190)
            
        # Init asteroid object, add it to asteroid group
        new_asteroid = objects.object_types["asteroid"](
            position = (x,y),
            speed=speed,
            direction = direction)
        asteroid.Asteroid.asteroidGroup.add(new_asteroid)
 
    def alien_spawn(self, QTY):
        '''
        Adds an integer QTY potential aliens to the infested
        asteroid 'aliens' attribute. This quantity will dictate
        the amount of aliens which can spawn from the alien_hop
        method. (I call it 'spawn pool')
        '''
        self.infested_asteroid.aliens += QTY

    def alien_hop(self):
        '''
        Handles creation of new aliens, movement of existing aliens,
        and drawing of teleport beams for successful hops.        
        '''
        # Only create aliens if there is a path
        if not self.paths is None:
            # Send an alien along each path
            for p in self.paths:
                if self.infested_asteroid.aliens != 0:
                    new_alien = objects.object_types["alien"](
                        asteroid = self.infested_asteroid, # Start at source
                        path = p[1:]) #No need to include source in path                   
                    alien.Alien.alienGroup.add(new_alien)
                    self.infested_asteroid.aliens -= 1 # Decrement 'spawn pool'
            self.paths = None

        # Only move if the spacestation is alive
        if self.space_station.alive():            
            target = self.space_station
            for al in alien.Alien.alienGroup:
                hop = None
                # Alien movement
                hop = al.path_hop(target)

                # Optional alien path drawing
                if self.OPTIONS==1 and not al.path is None:                   
                    self.alien_path_beams(al)

                # If hop successful, two nodes were returned, draw the beam
                if not hop is None:
                    beam.Beam.beamGroup.add(\
                        objects.object_types["beam"](\
                            obj1 = hop[0],
                            obj2 = hop[1],
                            color = (128,255,0),
                            surface = self.screen))
  
    def offscreen(self):
        '''
        Deactivates objects which go offscreen
        '''
        # Since we don't want asteroids deleting before offscreen, add padding
        padding = 50 
        # Asteroids
        for o in asteroid.Asteroid.asteroidGroup:
            if o.position[0] < -padding or o.position[0] \
                    > self.screen_rect.w + padding or \
                    o.position[1] < -10 or o.position[1] \
                    > self.screen_rect.h+10:
                o.deactivate()
        # Missiles
        for o in missile.Missile.missileGroup:
            if o.position[0] < -padding or o.position[0] \
                    > self.screen_rect.w + padding or \
                    o.position[1] < -padding or o.position[1] > \
                    self.screen_rect.h+padding:
                o.deactivate()
        # Aliens
        for o in alien.Alien.alienGroup:
            if o.position[0] < -padding or o.position[0] \
                    > self.screen_rect.w + padding or \
                    o.position[1] < -padding or o.position[1] > \
                    self.screen_rect.h+padding:
                o.deactivate()

                    
    def update(self):
        '''
        Called by game.py, calls the update methods of various groups/objects.
        Also handles object collisions.
        '''

        self.star_field.update()
        self.score.update(time.time())

        collision.ast_mis(self.screen)
        collision.ast_ast()

        # Optional ship collision with asteroids
        if self.OPTIONS == 2:
            collision.ship_ast(self.screen)

        asteroid.Asteroid.asteroidGroup.update()
        ship.Ship.shipGroup.update()
        missile.Missile.missileGroup.update()            

        self.graph_timer.update()

        alien.Alien.alienGroup.update()

    def draw(self):
        '''
        Draws the background elements and game objects.
        '''
        # Re-draw entire background
        self.screen.blit(self.bg_img,(0,0))
        self.star_field.draw(self.screen)
        self.score.draw(self.screen)

        # Draw the objects
        infested.Infested.infestedGroup.draw(self.screen)
        asteroid.Asteroid.asteroidGroup.draw(self.screen)
        ship.Ship.shipGroup.draw(self.screen)
        missile.Missile.missileGroup.draw(self.screen)
        spaceStation.SpaceStation.spaceStationGroup.draw(self.screen)
        alien.Alien.alienGroup.draw(self.screen)

        
        # Draw special effects
        # Particles draw simple circles on update
        particle.Particle.particleGroup.update()

        # Beams draw simple lines on update
        beam.Beam.beamGroup.update()

        # Update the screen
        pygame.display.flip()

    def graph_update(self):
        '''
        Updates the graph (flow network), modifies the GUI paths attribute
        to include any paths returned from the max flow algorithm.
        
        Everytime this function is called, the graph is created from scratch,
        and max flow called on this new flow network.        
        '''
        # Reset paths
        self.paths = None
        
        # Since the graph creates new source/sink nodes, store these along
        # with the graph object
        g,s,t = graph.gen_flow_network(
            asteroid.Asteroid.asteroidGroup.sprites(), # Nodes
            self.infested_asteroid, # Source s
            self.space_station, # Sink t
            alien.Alien.radius) # The max teleport radius

        # Optional graph edge drawing
        if self.OPTIONS == 3:
            self.graph_beams(g)
        
        # Run max flow on the newly created graph object
        flow = graph.max_flow(g,s,t)
        if flow > 0: # There is at least 1 valid flow path
            # Reconstruct flows to yield a list of path lists.
            self.paths = graph.reconstruct_flows(g,s,t)
            
    def graph_beams(self,g):
        '''
        Simply for demoing, draws a line for all edges in the graph object
        created in graph_update using the beam class.
        '''
        for e in g.edges():
            beam.Beam.beamGroup.add(\
                objects.object_types["beam"](\
                    health = 1,
                    obj1 = e[0],
                    obj2 = e[1],
                    color = (255,255,0),
                    surface = self.screen))
    
    def alien_path_beams(self, alien):
        '''
        Simply for demoing, draws a line for all edges in the alien's path.
        Green means still viable, red means out of range.
        '''
        curr = alien.asteroid
        
        for succ in alien.path[1:]:
            if euclidD(succ.position, curr.position) > alien.radius:
                color = (255,153,153)
            else:
                color = (102,155,102)
            beam.Beam.beamGroup.add(\
                objects.object_types["beam"](\
                    health = 40,
                    obj1 = curr,
                    obj2 = succ,
                    color = color,
                    surface = self.screen))
            curr = succ
