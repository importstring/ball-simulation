from browser import document, timer

# Initialize canvas and context
canvas = document["canvas"]
context = canvas.getContext("2d")

# Canvas dimensions
width, height = canvas.width, canvas.height

def draw_white_canvas():
    context.fillStyle = 'white'
    context.fillRect(0, 0, width, height)

# Draw white canvas initially
draw_white_canvas()
