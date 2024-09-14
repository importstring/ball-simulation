from browser import document, window, timer
import random
import math
import time

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
    balls_to_remove = []

    for ball in balls:
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']
        if ball['superpower'] != 'gravity_immunity' or (ball['superpower'] == 'gravity_immunity' and ball.get('end_time') and time.time() > ball['end_time']):
            ball['dy'] += gravity

        # Handle timed effects
        apply_superpower(ball)

        # Bounce off circular boundary
        if not within_circle(ball['x'], ball['y'], circle_center, circle_radius - ball['radius']):
            angle = math.atan2(ball['y'] - circle_center[1], ball['x'] - circle_center[0])
            ball['dx'] = -ball['dx'] + random.uniform(-0.5, 0.5)  # Add some randomness to the bounce
            ball['dy'] = -ball['dy'] + random.uniform(-0.5, 0.5)
            ball['x'] = circle_center[0] + (circle_radius - ball['radius']) * math.cos(angle)
            ball['y'] = circle_center[1] + (circle_radius - ball['radius']) * math.sin(angle)

            # Create a new ball at the center
            new_ball_color = random.choice(list(colors.values()))
            new_ball_superpower = assign_random_superpower()

            new_ball = create_ball()
            new_ball['color'] = new_ball_color
            new_ball['superpower'] = new_ball_superpower
            new_balls.append(new_ball)

        # Draw the ball
        context.fillStyle = ball['color']
        context.beginPath()
        context.arc(ball['x'], ball['y'], ball['radius'], 0, 2 * window.Math.PI)
        context.fill()

    balls.extend(new_balls)

    # Check for collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if distance(balls[i], balls[j]) < balls[i]['radius'] + balls[j]['radius']:
                if speed(balls[i]) > speed(balls[j]):
                    balls_to_remove.append(balls[j])
                    if balls[i]['color'] == colors['white']:  # White ball wins
                        next_ball_white = True
                    if balls[i]['superpower'] == 'duplicate':
                        new_ball1 = create_ball()
                        new_ball1['color'] = balls[i]['color']
                        new_ball1['superpower'] = assign_random_superpower()
                        new_ball2 = create_ball()
                        new_ball2['color'] = balls[i]['color']
                        new_ball2['superpower'] = assign_random_superpower()
                        new_balls.extend([new_ball1, new_ball2])
                    if balls[i]['superpower'] == 'split':
                        new_ball1 = create_ball()
                        new_ball1['color'] = balls[i]['color']
                        new_ball1['radius'] = ball_radius // 2
                        new_ball1['superpower'] = assign_random_superpower()
                        new_ball2 = create_ball()
                        new_ball2['color'] = balls[i]['color']
                        new_ball2['radius'] = ball_radius // 2
                        new_ball2['superpower'] = assign_random_superpower()
                        new_balls.extend([new_ball1, new_ball2])
                else:
                    balls_to_remove.append(balls[i])
                    if balls[j]['color'] == colors['white']:  # White ball wins
                        next_ball_white = True
                    if balls[j]['superpower'] == 'duplicate':
                        new_ball1 = create_ball()
                        new_ball1['color'] = balls[j]['color']
                        new_ball1['superpower'] = assign_random_superpower()
                        new_ball2 = create_ball()
                        new_ball2['color'] = balls[j]['color']
                        new_ball2['superpower'] = assign_random_superpower()
                        new_balls.extend([new_ball1, new_ball2])
                    if balls[j]['superpower'] == 'split':
                        new_ball1 = create_ball()
                        new_ball1['color'] = balls[j]['color']
                        new_ball1['radius'] = ball_radius // 2
                        new_ball1['superpower'] = assign_random_superpower()
                        new_ball2 = create_ball()
                        new_ball2['color'] = balls[j]['color']
                        new_ball2['radius'] = ball_radius // 2
                        new_ball2['superpower'] = assign_random_superpower()
                        new_balls.extend([new_ball1, new_ball2])

    balls = [ball for ball in balls if ball not in balls_to_remove]

    draw()
    timer.set_timeout(update, 30)  # Update the simulation every 30 milliseconds

update()
