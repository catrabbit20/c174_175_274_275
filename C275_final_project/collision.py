import pygame, math, random
import objects
from objects import *

'''
File includes momentum exchange function, collision handling and particle generation.
'''

def momentum(obj1, obj2):
    '''
    Given two sprite objects with direction, speed and mass
    who've collided, computes the new speed and 
    direction of the object after colliding.

    Momentum equations obtained from wikipedia: 2D Elastic Collision
    '''

    x_dif = obj1.position[0]-obj2.position[0]
    y_dif = -(obj1.position[1]-obj2.position[1]) #(-) for  y+ dwn axis

    phi = math.atan2(y_dif,x_dif)
    theta1 = obj1.direction * math.pi / 180
    theta2 = obj2.direction * math.pi / 180

    v1 = obj1.speed
    v2 = obj2.speed
    m1 = obj1.mass
    m2 = obj2.mass

    # Do the component math
    v1x = ((v1*math.cos(theta1-phi)*(m1-m2)+2*m2*v2*math.cos(theta2-phi))*\
               math.cos(phi))/(m1+m2) \
               + v1*math.sin(theta1-phi)*math.cos(phi+math.pi/2)

    v1y = ((v1*math.cos(theta1-phi)*(m1-m2)+2*m2*v2*math.cos(theta2-phi))*\
               math.sin(phi))/(m1+m2) \
               + v1*math.sin(theta1-phi)*math.sin(phi+math.pi/2)

    v2x = ((v2*math.cos(theta2-phi)*(m2-m1)+2*m1*v1*math.cos(theta1-phi))*\
               math.cos(phi))/(m1+m2) \
               + v2*math.sin(theta2-phi)*math.cos(phi+math.pi/2)

    v2y = ((v2*math.cos(theta2-phi)*(m2-m1)+2*m1*v1*math.cos(theta1-phi))*\
               math.sin(phi))/(m1+m2) \
               + v2*math.sin(theta2-phi)*math.sin(phi+math.pi/2)

    # Put it back into magnitude/direction
    obj1.direction = (math.atan2(v1y,v1x)/math.pi * 180)%360
    obj2.direction = (math.atan2(v2y,v2x)/math.pi * 180)%360
    obj1.speed = math.sqrt(v1x**2+v1y**2)
    obj2.speed = math.sqrt(v2x**2+v2y**2)

    # Add a pixel to prevent sticking
    x, y = obj1.position
    obj1.position = (x+math.cos(phi),y-math.sin(phi))
    x, y = obj2.position
    obj2.position = (x-math.cos(phi),y+math.sin(phi))

def ast_mis(surface):
    '''
    Detects collisions between asteroid and missile groups.
    
    Deals damage to colliding objects, calculates the
    object's new momentum and generates particles for both 
    missile deactivation and asteroid deactivation.
    
    '''
    ### Asteroid / missile collision ###
    col = None
    # Obtain colliding objects
    col = pygame.sprite.groupcollide(
        missile.Missile.missileGroup,
        asteroid.Asteroid.asteroidGroup,
        False, # Do not kill() object
        False) # Do not kill() object

    # obj is missile
    for obj in col:
        # i is asteroid
        for i in col[obj]:
            # momentum exchange
            momentum(obj,i)
            i.hurt(obj.damage) # Deal damage
            # if an alien occupies this asteroid
            if not i.alien is None:
                # deal damage
                i.alien.hurt(obj.damage)
                # since we're one hitting the alien, update score
                score.Score.scoreGroup.sprites()[0].increaseScore(1)
            if i.alive() == False: # If we just destroyed an asteroid
                generate_particles(surface,obj,10,3, (141,125,114))
        # Missiles always generate particles and die
        generate_particles(surface,obj,8,2,(82,57,48))
        obj.hurt(1)

def ship_ast(surface):
    '''
    Detects collisions between ship and asteroid groups.

    Exchanges momentums. Ship maintains its direction post
    momentum exchange, otherwise piloting is a mess. This creates a 
    bug however, as the ships velocity increases due to momentum exchange.
    '''
    col = None
    # Obtain colliding objects
    col = pygame.sprite.groupcollide(
        ship.Ship.shipGroup,
        asteroid.Asteroid.asteroidGroup,
        False,
        False)

    # obj is ship
    for obj in col:
        # i is asteroid
        for i in col[obj]:
            # store pre collision ship direction
            dir_buf = obj.direction
            # momentum exchange
            momentum(obj,i)
            # reset ship direction
            obj.direction = dir_buf
 
def ast_ast():
    '''
    Detects collisions between asteroids

    Exchanges momentum when a collision occurs.
    '''
    col = None
    obj1 = None

    # For all the asteroids
    for i in range(len(asteroid.Asteroid.asteroidGroup)-1):
        # Check if i-th asteroid collides with any in i+1 suffix
        obj1 = asteroid.Asteroid.asteroidGroup.sprites()[i]
        col = pygame.sprite.spritecollide(
            obj1,
            asteroid.Asteroid.asteroidGroup.sprites()[i+1:],
            False)
        # For anything obj1 collided with, exchange momentum
        for obj2 in col:
            momentum(obj1, obj2)

def generate_particles(surface, source, number, radius, color, health=50):
    '''
    For effects, generates a number of circles of radius, color;
    Obtains speed and position information from source object.

    Args:
    surface: pygame surface to draw particles to
    source: object from which particles originate
            requires position, speed, direction attributes
    number: how many particles to generate
    radius: size of particles (circles)
    color: color of particles
    health: particles lose 1 health per frame, thus health is a crude timer

    Returns:
    rep_particle: last particle generated during this group. Only used in this
                  project for the endgame token
    '''
    for p in range(number):
        rep_particle = objects.object_types["particle"](
            health = health,
            position = source.position,
            # Randomize speed for effect
            speed = random.triangular(0,source.speed,source.speed*0.7),
            direction = \
                # Randomize direction for effect
                source.direction+random.triangular(
                    0,
                    360,
                    source.direction),
            radius=radius, color=color,
            surface = surface)
        particle.Particle.particleGroup.add(rep_particle)

    return rep_particle
