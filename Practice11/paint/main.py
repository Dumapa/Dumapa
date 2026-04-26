import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    canvas = pygame.Surface((800, 600))
    canvas.fill((0, 0, 0))
    clock = pygame.time.Clock()
    
    radius = 5
    color = (0, 0, 255) 
    mode = 'pen' 
    last_pos, start_pos = None, None
    drawing = False

    print("Colors: R(Red), G(Green), B(Blue), Y(Yellow), W(White)")
    print("Tools: P(Pen), S(Rect), C(Circle), E(Eraser)")
    print("NEW SHAPES: 1(Square), 2(Right Tri), 3(Eq Tri), 4(Rhombus)")
    print("Radius: Mouse wheel or Left/Right click")

    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 255, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_y: color = (255, 255, 0)
                elif event.key == pygame.K_w: color = (255, 255, 255)
                
                elif event.key == pygame.K_p: mode = 'pen'
                elif event.key == pygame.K_s: mode = 'rect'
                elif event.key == pygame.K_c: mode = 'circle'
                elif event.key == pygame.K_e: mode = 'eraser'
                
                # New shape triggers
                elif event.key == pygame.K_1: mode = 'square'
                elif event.key == pygame.K_2: mode = 'right_tri'
                elif event.key == pygame.K_3: mode = 'eq_tri'
                elif event.key == pygame.K_4: mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    drawing = True
                    start_pos = event.pos 
                elif event.button == 3: radius = min(100, radius + 2)
                elif event.button == 2: radius = max(1, radius - 2)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    # Finalize shape onto persistent canvas
                    if mode == 'rect': draw_rect(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'circle': draw_circle(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'square': draw_square(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'right_tri': draw_right_triangle(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'eq_tri': draw_equilateral_triangle(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'rhombus': draw_rhombus(canvas, start_pos, event.pos, radius, color)
                    start_pos = None
                last_pos = None

        if drawing:
            if mode == 'pen' and last_pos is not None:
                draw_line(canvas, last_pos, pos, radius, color)
            elif mode == 'eraser' and last_pos is not None:
                draw_line(canvas, last_pos, pos, radius, (0, 0, 0)) 
            last_pos = pos

        screen.blit(canvas, (0, 0))
        
        # Temporary preview layer
        if drawing and start_pos is not None:
            if mode == 'rect': draw_rect(screen, start_pos, pos, radius, color)
            elif mode == 'circle': draw_circle(screen, start_pos, pos, radius, color)
            elif mode == 'square': draw_square(screen, start_pos, pos, radius, color)
            elif mode == 'right_tri': draw_right_triangle(screen, start_pos, pos, radius, color)
            elif mode == 'eq_tri': draw_equilateral_triangle(screen, start_pos, pos, radius, color)
            elif mode == 'rhombus': draw_rhombus(screen, start_pos, pos, radius, color)

        pygame.draw.circle(screen, color if mode != 'eraser' else (255, 255, 255), pos, radius, 1)

        pygame.display.flip()
        clock.tick(120)

def draw_line(surf, start, end, width, color):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    
    # CRITICAL FIX: Prevent division by zero if user clicks without dragging
    if distance == 0:
        pygame.draw.circle(surf, color, start, width)
        return
        
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surf, color, (x, y), width)

def draw_rect(surf, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)), width)

def draw_circle(surf, start, end, width, color):
    r = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
    if r > width: pygame.draw.circle(surf, color, start, r, width)

# --- 1. Draw Square ---
def draw_square(surf, start, end, width, color):
    side_length = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
    rect_x = start[0] if end[0] > start[0] else start[0] - side_length
    rect_y = start[1] if end[1] > start[1] else start[1] - side_length
    if side_length > 0:
        pygame.draw.rect(surf, color, (rect_x, rect_y, side_length, side_length), width)

# --- 2. Draw Right Triangle ---
def draw_right_triangle(surf, start, end, width, color):
    points = [(start[0], start[1]), (start[0], end[1]), (end[0], end[1])]
    if len(set(points)) > 2: # Prevent drawing invalid 1D polygons
        pygame.draw.polygon(surf, color, points, width)

# --- 3. Draw Equilateral (Isosceles) Triangle ---
def draw_equilateral_triangle(surf, start, end, width, color):
    mid_x = (start[0] + end[0]) // 2
    points = [(mid_x, start[1]), (start[0], end[1]), (end[0], end[1])]
    if len(set(points)) > 2:
        pygame.draw.polygon(surf, color, points, width)

# --- 4. Draw Rhombus ---
def draw_rhombus(surf, start, end, width, color):
    mid_x = (start[0] + end[0]) // 2
    mid_y = (start[1] + end[1]) // 2
    points = [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)]
    if len(set(points)) > 2:
        pygame.draw.polygon(surf, color, points, width)

if __name__ == "__main__":
    main()