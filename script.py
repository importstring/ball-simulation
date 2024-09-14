from browser import document, window, timer
import random
import math

# Initialize variables
width, height = 800, 600
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

def distance(ball1, ball2):
    return math.sqrt((ball1['x'] - ball2['x']) ** 2 + (ball1['y'] - ball2['y']) ** 2)

def within_circle(x, y, center, radius):
    return (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2

def draw():
    canvas = document["canvas"]
    context = canvas.getContext("2d")
    
    context.fillStyle = "black"
    context.fillRect(0, 0, width, height)

    context.strokeStyle = 'white'
    context.beginPath()
    context.arc(circle_center[0], circle_center[1], circle_radius, 0, 2 * window.Math.PI)
    context.stroke()

    for ball in balls:
        context.fillStyle = ball['color']
        context.beginPath()
        context.arc(ball['x'], ball['y'], ball['radius'], 0, 2 * window.Math.PI)
        context.fill()

def update():
    global circle_radius

    canvas = document["canvas"]
    context = canvas.getContext("2d")
    
    # Randomly adjust the circle radius
    circle_radius += random.randint(-10, 10)
    circle_radius = max(50, min(circle_radius, min(width, height) // 2 - 10))

    new_balls = []

    for ball in balls:
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']
        ball['dy'] += gravity

        if not within_circle(ball['x'], ball['y'], circle_center, circle_radius - ball['radius']):
            angle = math.atan2(ball['y'] - circle_center[1], ball['x'] - circle_center[0])
            ball['dx'] = -ball['dx'] + random.uniform(-0.5, 0.5)
            ball['dy'] = -ball['dy'] + random.uniform(-0.5, 0.5)
            ball['x'] = circle_center[0] + (circle_radius - ball['radius']) * math.cos(angle)
            ball['y'] = circle_center[1] + (circle_radius - ball['radius']) * math.sin(angle)

            new_ball = create_ball()
            new_ball['color'] = random.choice(list(colors.values()))
            new_balls.append(new_ball)

        context.fillStyle = ball['color']
        context.beginPath()
        context.arc(ball['x'], ball['y'], ball['radius'], 0, 2 * window.Math.PI)
        context.fill()

    balls.extend(new_balls)

    context.clearRect(0, 0, width, height)
    draw()

timer.set_interval(update, 1000 / 60)  # 60 FPS
