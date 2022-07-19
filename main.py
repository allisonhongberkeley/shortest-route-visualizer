from math import sqrt
import pygame
from pygame.locals import *
from queue import PriorityQueue
import sys
import config
import time
import a_node

class Button():
    button_width = 200
    button_height = 100

    def __init__ (self, x, y, color, text):
        self.color = color
        self.x = x
        self.y = y
        self.text = text
    
    def draw(self, screen):
        rect = pygame.Rect((self.x, self.y), (Button.button_width, Button.button_height))
        pygame.draw.rect(config.screen, self.color, rect, 0, 2)

        font = pygame.font.SysFont('Calibri', 60)
        text= font.render(self.text, False, (0, 0, 0))
        config.screen.blit(text, (self.x + Button.button_width // 2 - text.get_width() // 2, self.y + Button.button_height // 2 - text.get_height() // 2))


def main():
    global clock, start_key, end, set_started, set_ended
    pygame.init() 
    config.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_WIDTH))
    clock = pygame.time.Clock()
    config.screen.fill(config.BACKGROUND_COLOR)
    pygame.display.set_caption("Shortest Path Finding: Visualization")
    pygame.display.flip() 
    config.game_grid = drawAGrid(); 
    reset_button = Button(10, 10, config.TAN, 'reset')
    reset_button.draw(config.screen)

    playing = True
    start_key, end_key = None, None
    set_started, set_ended = False, False
    while playing: 

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                print(key)
                pos = pygame.mouse.get_pos() 
                clicked_node = click(pos)
                if key == 'r':
                    clicked_node.draw_and_act(clicked_node.reset, config.screen)
                elif not set_started and key == 's': 
                    start_key = clicked_node
                    clicked_node.draw_and_act(clicked_node.start, config.screen)
                    set_started = True
                elif set_started and clicked_node != start_key and not set_ended and key == 'e':
                    end = clicked_node 
                    clicked_node.draw_and_act(clicked_node.end, config.screen)
                    set_ended = True
                elif set_started and set_ended and key == 'b':
                    clicked_node.draw_and_act(clicked_node.obstacle, config.screen)
                elif key == 'a':
                    [y.draw_and_act(y.reset, config.screen) for x in config.game_grid for y in x]  
                    set_started, set_ended = False, False       
                if key == 'p':
                    a_star_search()
            if event.type == pygame.QUIT:
                playing = False
            
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

def drawAGrid():
    # here, initiate all the nodes and draw Nodes 
    # create 2D array grid of nodes
    grid = [[None] * config.TOTAL_COLS for i in range(config.TOTAL_ROWS)]
    for x in range(config.TOTAL_ROWS):
        for y in range(config.TOTAL_COLS):
            node = a_node.Node(x, y, config.width)
            grid[x][y] = node
            node.draw(config.screen)        
    return grid

def heuristic(node_one, node_two):
    x_1, y_1 = node_one.position()
    x_2, y_2 = node_two.position()
    return abs(x_2-x_1) + abs(y_2-y_1)

def euclidean(node_one, node_two):
    x_1, y_1 = node_one.position()
    x_2, y_2 = node_two.position()
    return sqrt(abs(x_1-x_2)**2 + abs(y_1-y_2)**2)

def click(pos): 
    row, col = tuple(coord // config.width for coord in pos)
    clicked = config.game_grid[row][col]
    return clicked

def print_path(node):
    node.path()
    node.draw(config.screen)
    while node.parent is not None:
        node = node.parent
        node.path()
        node.draw(config.screen)

def a_star_search():
    queue = PriorityQueue()
    start_key.f, start_key.g, start_key.h = 0, 0, 0
    queue.put((start_key.f, start_key))
    scores_tracker = {}
    scores_tracker[start_key] = [start_key.f, start_key.g, start_key.h]
    visited = []

    while not queue.empty(): #while destination not reached
        node = queue.get()[1]
        node.close()
        #node.draw(screen)
        visited.append(node)
        if (node == end):
            print_path(node)
            return
        else:
            neighbors = node.find_neighbors()
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                #create f, g, h values
                neighbor.h = heuristic(neighbor, end)
                neighbor.g = node.g + euclidean(neighbor, node)
                neighbor.f = neighbor.g + neighbor.h
                # if neighbor is already in the queue and its g score is > than its current g score, don't update
                if neighbor in scores_tracker and neighbor.g > scores_tracker[neighbor][1]:
                    #figure out how to not update f, g, h here
                    #neighbor.f, neighbor.g, neighbor.h = scores_tracker[neighbor][0], scores_tracker[neighbor][1], scores_tracker[neighbor][2]
                    continue
                neighbor.parent = node            
                scores_tracker[neighbor] = [neighbor.f, neighbor.g, neighbor.h]
                queue.put((neighbor.f, neighbor))
        
    print('destination not found')

if __name__ == "__main__":
    main()