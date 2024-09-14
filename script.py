from browser import document, window, timer
import random
import math
import time

# Initialize canvas and context
canvas = document["canvas"]
context = canvas.getContext("2d")

# Canvas dimensions
width, height = canvas.width, canvas.height

def draw_white_canvas():
    context.fillStyle = 'white'
    context.fillRect(0, 0, width, height)

def draw_black_canvas():
    context.fillStyle = 'black'
    context.fillRect(0, 0, width, height)

# Draw white canvas initially
draw_white_canvas()

# Change to black canvas after 2 seconds
timer.set_timeout(draw_black_canvas, 2000)

# Initialize variables
circle_center = (width // 2, height // 2)
circle_radius = 250
ball_radius = 10
gravity = 0.1
balls = []
colors = {
    'red': 'red',
    'orange': 'orange',
    'yellow': 'yellow',
    'green': 'green',
    'blue': 'blue',
    'purple': 'purple',
    'pink': 'pink',
    'white': 'white'
}

# Create a ball
def create_ball():
    return {
        'x': circle_center[0],
        'y': circle_center[1],
        'dx': random.uniform(-2, 2),
        'dy': random.uniform(-2, 2),
        'color': colors['white'],
        'radius': ball_radius,
        'superpower': None
    }

balls.append(create_ball())

# Possible superpowers
superpowers = ['size_increase', 'speed_boost', 'duplicate', 'gravity_immunity', 'slow_others', 'random_direction', 'split']

def distance(ball1, ball2):
    return math.sqrt((ball1['x'] - ball2['x']) ** 2 + (ball1['y'] - ball2['y']) ** 2)

def within_circle(x, y, center, radius):
    return (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2

def apply_superpower(ball):
    if ball['superpower'] == 'speed_boost':
        if ball.get('end_time') is None:  # Apply speed boost
            ball['dx'] *= 1.5
            ball['dy'] *= 1.5
            ball['end_time'] = time.time() + 2  # Speed boost lasts for 2 seconds
        elif time.time() > ball['end_time']:  # Reset speed boost
            ball['dx'] /= 1.5
            ball['dy'] /= 1.5
            ball['end_time'] = None
    elif ball['superpower'] == 'size_increase':
        ball['radius'] = ball_radius * 2
    elif ball['superpower'] == 'gravity_immunity':
        if ball.get('end_time') is None:
            ball['original_dy'] = ball['dy']
            ball['dy'] = 0
            ball['end_time'] = time.time() + 5  # Immunity lasts for 5 seconds
        elif time.time() > ball['end_time']:
            ball['dy'] = ball['original_dy']
            ball['end_time'] = None
    elif ball['superpower'] == 'random_direction':
        if ball.get('end_time') is None or time.time() > ball['end_time']:
            ball['dx'] = random.uniform(-2, 2)
            ball['dy'] = random.uniform(-2, 2)
            ball['end_time'] = time.time() + 5  # Change direction every 5 seconds

def assign_random_superpower():
    return random.choice(superpowers)

def draw():
    context.clearRect(0, 0, width, height)  # Clear the canvas
    
    # Draw the circular boundary
