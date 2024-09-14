import pygame
import sys
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Controlled Ball Bouncing Simulation')


# Colors
black = (0, 0, 0)
colors = {
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (148, 0, 211),
    'pink': (255, 105, 180),
    'white': (255, 255, 255)
}

# Circular boundary settings
circle_center = (width // 2, height // 2)
circle_radius = 250

# Ball settings
ball_radius = 10
gravity = 0.1
balls = []
initial_ball = [circle_center[0], circle_center[1], random.uniform(-2, 2), random.uniform(-2, 2), colors['white'], ball_radius, None, None, None]  # White ball initially
balls.append(initial_ball)

# Possible superpowers
superpowers = ['size_increase', 'speed_boost', 'duplicate', 'gravity_immunity', 'slow_others', 'random_direction', 'split']

def distance(ball1, ball2):
    return math.sqrt((ball1[0] - ball2[0]) ** 2 + (ball1[1] - ball2[1]) ** 2)

def within_circle(x, y, center, radius):
    return (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2

def speed(ball):
    return math.sqrt(ball[2] ** 2 + ball[3] ** 2)

def apply_superpower(ball):
    if ball[6] == 'speed_boost':
        if ball[8] is None:  # Apply speed boost
            ball[2] *= 1.5
            ball[3] *= 1.5
            ball[8] = time.time() + 2  # Speed boost lasts for 2 seconds
        elif time.time() > ball[8]:  # Reset speed boost
            ball[2] /= 1.5
            ball[3] /= 1.5
            ball[8] = None
    elif ball[6] == 'size_increase':
        ball[5] = ball_radius * 2
    elif ball[6] == 'gravity_immunity':
        if ball[8] is None:
            ball[7] = ball[3]
            ball[3] = 0
            ball[8] = time.time() + 5  # Immunity lasts for 5 seconds
        elif time.time() > ball[8]:
            ball[3] = ball[7]
            ball[8] = None
    elif ball[6] == 'random_direction':
        if ball[8] is None or time.time() > ball[8]:
            ball[2] = random.uniform(-2, 2)
            ball[3] = random.uniform(-2, 2)
            ball[8] = time.time() + 5  # Change direction every 5 seconds

def assign_random_superpower():
    return random.choice(superpowers)

# Main loop
running = True
next_ball_white = False

# Main loop
running = True
next_ball_white = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    # Randomly adjust the circle radius
    circle_radius += random.randint(-10, 10)
    circle_radius = max(50, min(circle_radius, min(width, height) // 2 - 10))

    # Draw the circular boundary
    pygame.draw.circle(screen, (255, 255, 255), circle_center, circle_radius, 2)

    new_balls = []
    balls_to_remove = []

    # Move balls and apply gravity
    for ball in balls:
        ball[0] += ball[2]
        ball[1] += ball[3]
        if ball[6] != 'gravity_immunity' or (ball[6] == 'gravity_immunity' and ball[8] and time.time() > ball[8]):
            ball[3] += gravity

        # Handle timed effects
        apply_superpower(ball)

        # Bounce off circular boundary
        if not within_circle(ball[0], ball[1], circle_center, circle_radius - ball[5]):
            angle = math.atan2(ball[1] - circle_center[1], ball[0] - circle_center[0])
            ball[2] = -ball[2] + random.uniform(-0.5, 0.5)  # Add some randomness to the bounce
            ball[3] = -ball[3] + random.uniform(-0.5, 0.5)
            ball[0] = circle_center[0] + (circle_radius - ball[5]) * math.cos(angle)
            ball[1] = circle_center[1] + (circle_radius - ball[5]) * math.sin(angle)

            # Create a new ball at the center
            if next_ball_white:
                new_ball_color = colors['white']
                next_ball_white = False
            else:
                new_ball_color = random.choice(list(set(colors.values()) - {colors['white']}))

            new_ball_superpower = assign_random_superpower()

            new_ball = [circle_center[0], circle_center[1], random.uniform(-2, 2), random.uniform(-2, 2), new_ball_color, ball_radius, new_ball_superpower, None, None]
            new_balls.append(new_ball)

        # Draw the ball
        pygame.draw.circle(screen, ball[4], (int(ball[0]), int(ball[1])), ball[5])

    balls.extend(new_balls)

    # Check for collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if distance(balls[i], balls[j]) < balls[i][5] + balls[j][5]:
                if speed(balls[i]) > speed(balls[j]):
                    balls_to_remove.append(balls[j])
                    if balls[i][4] == colors['white']:  # White ball wins
                        next_ball_white = True
                    if balls[i][6] == 'duplicate':
                        new_ball1 = [balls[i][0], balls[i][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[i][4], ball_radius, assign_random_superpower(), None, None]
                        new_ball2 = [balls[i][0], balls[i][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[i][4], ball_radius, assign_random_superpower(), None, None]
                        new_balls.extend([new_ball1, new_ball2])
                    if balls[i][6] == 'split':
                        new_ball1 = [balls[i][0], balls[i][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[i][4], ball_radius // 2, assign_random_superpower(), None, None]
                        new_ball2 = [balls[i][0], balls[i][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[i][4], ball_radius // 2, assign_random_superpower(), None, None]
                        new_balls.extend([new_ball1, new_ball2])
                else:
                    balls_to_remove.append(balls[i])
                    if balls[j][4] == colors['white']:  # White ball wins
                        next_ball_white = True
                    if balls[j][6] == 'duplicate':
                        new_ball1 = [balls[j][0], balls[j][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[j][4], ball_radius, assign_random_superpower(), None, None]
                        new_ball2 = [balls[j][0], balls[j][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[j][4], ball_radius, assign_random_superpower(), None, None]
                        new_balls.extend([new_ball1, new_ball2])
                    if balls[j][6] == 'split':
                        new_ball1 = [balls[j][0], balls[j][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[j][4], ball_radius // 2, assign_random_superpower(), None, None]
                        new_ball2 = [balls[j][0], balls[j][1], random.uniform(-2, 2), random.uniform(-2, 2), balls[j][4], ball_radius // 2, assign_random_superpower(), None, None]
                        new_balls.extend([new_ball1, new_ball2])

    for ball in balls_to_remove:
        if ball in balls:
            balls.remove(ball)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
