from txtcolor import TextColor
import os
from threading import Lock

'''
This class is responsible for creating a character matrix, 17 lines * 64 characters, 
as the basis for creating the Text User Interface.
'''
class ScreenMatrix():
    def __init__(self, iskmscon=True):
        self.bg_clr = 'sel blue' ##main TUI background color
        self._TUI_HEIGHT = 17
        self._TUI_WIDTH = 64
        self._screen_matrix = self.create()
        self._screen_matrix = self.bg_color()
        self.iskmscon = iskmscon
        self.lock = Lock()

    # append with 17 lists corresponding to 17 rows
    def create(self):
        self._screen_matrix = []
        for i in range(self._TUI_HEIGHT):
            self._screen_matrix.append([])
        return self._screen_matrix

    # Fill screen matrix with color
    # append each column with 64 Nones corresponding to 64 characters per row
    def bg_color(self):
        char = TextColor.color_bg(self.bg_clr, ' ')
        for i in range(self._TUI_HEIGHT):
            for j in range(self._TUI_WIDTH):
                self._screen_matrix[i].append(char)
        return self._screen_matrix

    def draw_box(self, y=0, x=10, y_siz=10, x_siz=10, title=None, warning_box=False):
        box_parts = {}
        fill = lambda char: (char * (x_siz - 2))
        box_parts['body'] = '┃' + fill(' ') + '┃'
        box_parts['frame top'] = '┏' + fill('━') + '┓'
        box_parts['frame bottom'] = '┗' + fill('━') + '┛'
        box_parts['frame joints'] = '┣' + fill('━') + '┫'
        if title is not None:
            cent_l = cent_r = int(((x_siz - 2) - len(title)) / 2)
            if ((x_siz - 2) - (cent_l + cent_r + len(title)) == 1):
                cent_r += 1
            box_parts['title'] = '┃' + (' ' * cent_l) + title + (' ' * cent_r) + '┃'

        for i in range(y_siz):
            if (i == 0):
                cat = 'frame top'
            elif (i == y_siz-1):
                cat = 'frame bottom'
            elif (
                (title is not None)
                and (i == 1)
            ):
                cat = 'title'
            elif (
                (title is not None)
                and (i == 2)
            ):
                cat = 'frame joints'
            elif(
                (warning_box)
                and (i == y_siz-3)
                ):
                cat = 'frame joints'
            else:
                cat = 'body'
            string = TextColor.color_bg(self.bg_clr, box_parts[cat])
            self.alter_con_out(y=y+i, x=x, string=string)

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
        '''
        Lock beacuse multiple threads can use this function, 
        which can errors in cursor manipulation.
        '''
        with self.lock:
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