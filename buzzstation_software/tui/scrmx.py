from txtcolor import TextColor
import os

'''
This class is responsible for creating a character matrix, 17 lines * 64 characters, 
as the basis for creating the Text User Interface.
'''
class ScreenMatrix():
    def __init__(self, iskmscon=True):
        self._TUI_HEIGHT = 17
        self._TUI_WIDTH = 64
        self._screen_matrix = self.create()
        self._screen_matrix = self.fill_nones()
        self._screen_matrix = self.bg_color()
        self.iskmscon = iskmscon

    # append with 17 lists corresponding to 17 rows
    def create(self):
        self._screen_matrix = []
        for i in range(self._TUI_HEIGHT):
            self._screen_matrix.append([])
        return self._screen_matrix

    # append each column with 64 Nones corresponding to 64 characters per row
    def fill_nones(self):
        for i in range(self._TUI_HEIGHT):
            for j in range(self._TUI_WIDTH):
                self._screen_matrix[i].append(None)
        return self._screen_matrix

    # Fill screen matrix with color
    def bg_color(self):
        for y in range(len(self._screen_matrix)):
            for x in range(len(self._screen_matrix[y])):
                self._screen_matrix[y][x] = TextColor.color_bg('blue', ' ')
        return self._screen_matrix

    def draw_box(self):
        # Draw box with space on top for text:
        for y in range(len(self._screen_matrix)):
            for x in range(len(self._screen_matrix[y])):
                if x == 0 or x == len(self._screen_matrix[y]) - 1:
                    self._screen_matrix[y][x] = TextColor.color_bg('blue', '┃')
                    if y == 0 or y == len(self._screen_matrix) - 1:
                        self._screen_matrix[y][x] = TextColor.color_bg('blue', ' ')
                    if x == 0 and y == 1:
                        self._screen_matrix[y][x] = TextColor.color_bg('blue', '┏')
                    if x == len(self._screen_matrix[y]) - 1 and y == 1:
                        self._screen_matrix[y][x] = TextColor.color_bg('blue', '┓')
                    if x == 0 and y == len(self._screen_matrix) - 2:
                        self._screen_matrix[y][x] = TextColor.color_bg('blue', '┗')
                    if x == len(self._screen_matrix[y]) - 1 and y == len(self._screen_matrix) - 2:
                        self._screen_matrix[y][x] = TextColor.color_bg('blue', '┛')
                elif y == 1 or y == len(self._screen_matrix) - 2:
                    self._screen_matrix[y][x] = TextColor.color_bg('blue', '━')
                else:
                    self._screen_matrix[y][x] = TextColor.color_bg('blue', ' ')

    # Draw centered text at the bottom of the screen:
    def draw_title(self, text):
        width = len(self._screen_matrix[0])
        start_print = (width - len(text)) / 2
        start_print = int(start_print)
        for i in range(len(text)):
            self._screen_matrix[0][start_print+i] = self._screen_matrix[0][start_print+i].replace(' ', text[i])

    #draw text on the bottom alligned to the left:
    def draw_instr(self, info_text):
        for i in range(len(info_text)):
            self._screen_matrix[len(self._screen_matrix)-1][i+1] = self._screen_matrix[len(self._screen_matrix)-1][i+1].replace(' ', info_text[i])

    # create string from chars matrix (self._screen_matrix) and print it out
    def print(self):
        if self.iskmscon:
            frame = ''
            print('\033[H', end='')
            for i in range(len(self._screen_matrix)):
                for j in range(len(self._screen_matrix[0])):
                    frame += self._screen_matrix[i][j]
                frame = (15-i)*'\033[F' + '\033[K' + frame
                print(frame, flush=True)
                frame = ''
        else:
            frame = ''
            for i in range(len(self._screen_matrix)):
                for j in range(len(self._screen_matrix[0])):
                    frame += self._screen_matrix[i][j]
                print(frame)
                frame = ''

    def alter_con_out(self, y, x, string):
        y = self._TUI_HEIGHT - y + 1
        print('\033[A'*y, end='')
        print('\033[C'*x, end='')
        print(string, end='')
        if self.iskmscon:
            print('\033[H', end='', flush=True)
            print('\033[999B', end='', flush=True)
        else:
            print('\033[E'*y, end='', flush=True)

    def clear_screen(self):
        print('\033[H', end='')


if __name__ == '__main__':
    screen_matrix = ScreenMatrix(iskmscon=False)
    screen_matrix.print()
    screen_matrix.alter_con_out(0, 60, 'text')
    import time
    time.sleep(10)