import pygame
from resources import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

bgcolor = pygame.Color(60, 60, 80)
playercolor = pygame.Color(60, 100, 180)
shieldcolor = pygame.Color(195, 230, 255)
wallcolor = (65, 80, 90)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
dt = 0
speed = 300

current_room = 'room1'
shield = False

player_radius = 40
door_radius = 45

northwallrect = pygame.Rect(0, 0, screen.get_width(), 100)
eastwallrect = pygame.Rect(screen.get_width() - 100, 0, 100, screen.get_height())
southwallrect = pygame.Rect(0, screen.get_height() - 100, screen.get_width(), 100)
westwallrect = pygame.Rect(0, 0, 100, screen.get_height())

northdoor_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 15)
southdoor_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() * 14 / 15)
westdoor_pos = pygame.Vector2(door_radius + 5, screen.get_height() / 2)
eastdoor_pos = pygame.Vector2(screen.get_width() - door_radius - 5, screen.get_height() / 2)

connections = {
        'room1' : ['room2', 'null', 'null', 'null'],
        'room2' : ['null', 'room3', 'room1', 'null'],
        'room3' : ['null', 'room6', 'room4', 'room2'],
        'room4' : ['room3', 'room5', 'null', 'null'],
        'room5' : ['null', 'null', 'null', 'room4'],
        'room6' : ['null', 'null', 'null', 'room3']
        }
contents = {
        'room1' : ['northdoor'],
        'room2' : ['southdoor', 'eastdoor'],
        'room3' : ['westdoor', 'southdoor', 'eastdoor'],
        'room4' : ['northdoor', 'eastdoor'],
        'room5' : ['westdoor'],
        'room6' : ['westdoor']
        }

def draw_doors(current_room):
    for room in contents[current_room]:
        if room == 'northdoor':
            pygame.draw.circle(screen, "black", northdoor_pos, door_radius)
        if room == 'eastdoor':
            pygame.draw.circle(screen, "black", eastdoor_pos, door_radius)
        if room == 'southdoor':
            pygame.draw.circle(screen, "black", southdoor_pos, door_radius)
        if room == 'westdoor':
            pygame.draw.circle(screen, "black", westdoor_pos, door_radius)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bgcolor)

    # poll key presses and update character
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos.y >= 80:
        player_pos.y -= speed * dt
    if keys[pygame.K_a] and player_pos.x >= 80:
        player_pos.x -= speed * dt
    if keys[pygame.K_s] and player_pos.y <= screen.get_height() - 80:
        player_pos.y += speed * dt
    if keys[pygame.K_d] and player_pos.x <= screen.get_width() - 80:
        player_pos.x += speed * dt

    # collisions
    # northdoor
    if abs(player_pos.x - northdoor_pos.x) < (player_radius + door_radius):
        if abs(player_pos.y - northdoor_pos.y) < (player_radius + door_radius):
            if connections[current_room][0] != 'null':
                current_room = connections[current_room][0]
                player_pos.y = screen.get_height() - 150
    # eastdoor
    if abs(player_pos.x - eastdoor_pos.x) < (player_radius + door_radius):
        if abs(player_pos.y - eastdoor_pos.y) < (player_radius + door_radius):
            if connections[current_room][1] != 'null':
                current_room = connections[current_room][1]
                player_pos.x = 150
    # southdoor
    if abs(player_pos.x - southdoor_pos.x) < (player_radius + door_radius):
        if abs(player_pos.y - southdoor_pos.y) < (player_radius + door_radius):
            if connections[current_room][2] != 'null':
                current_room = connections[current_room][2]
                player_pos.y = 150
    # westdoor
    if abs(player_pos.x - westdoor_pos.x) < (player_radius + door_radius):
        if abs(player_pos.y - westdoor_pos.y) < (player_radius + door_radius):
            if connections[current_room][3] != 'null':
                current_room = connections[current_room][3]
                player_pos.x = screen.get_width() - 150

    # draw walls
    pygame.draw.rect(screen, wallcolor, northwallrect)
    pygame.draw.rect(screen, wallcolor, westwallrect)
    pygame.draw.rect(screen, wallcolor, eastwallrect)
    pygame.draw.rect(screen, wallcolor, southwallrect)

    # draw room contents
    draw_doors(current_room)

    # check for shield
    if keys[pygame.K_LSHIFT]:
        pygame.draw.circle(screen, shieldcolor, player_pos, player_radius + 10)
        shield = True

    # draw player
    pygame.draw.circle(screen, playercolor, player_pos, player_radius)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
