from scrmx import ScreenMatrix
from txtcolor import TextColor


class TrackerLike(ScreenMatrix):
    def __init__(self, iskmscon=True):
        super().__init__(iskmscon)
        self._played_number = None
        self._first_number = 1

    '''
    Create rows in different color than background, divided eachother
    by line width column of background color.
    This rows will be fields for tracker notes/pattern data.
    Each second line is colored in differend shade of grey,
    therefore the rows will not be confused with each other.
    Rows are printed from 1 to 17, to leave screen row 0 for rows
    titles.
    '''
    def draw_tracks(self):
        clrd_empty_chr1 = TextColor.color_bg('black grey', ' ')
        clrd_empty_chr2 = TextColor.color_bg('dark grey', ' ')
        ## 16 visible quarternotes/levels/rows:
        for y in range(1, 17):
            track_position = 3 #from each screen matrix column track printing will start
            ## 8 tracks:
            for i in range(8):
                # 5 characters ength for track:
                for j in range(5):
                    # each second i
                    if y % 2 == 1:
                        self._screen_matrix[y][track_position+j] = clrd_empty_chr1
                    else:
                        self._screen_matrix[y][track_position+j] = clrd_empty_chr2
                track_position += 6
        return self._screen_matrix

    '''
    Convert quarter level number to 3 length string,
    change it color background and, if needed, font color,
    so for example number 1 can hide previous displayed
    number 100.
    '''
    def adjust_qnumber_str(self, nbr):
        nbr_str = str(nbr)
        for i in range(3-len(nbr_str)):
            nbr_str = ' ' + nbr_str
        nbr_str = TextColor.color_bg('blue', nbr_str)
        ## accent each four beat:
        if (nbr % 4 == 0):
            nbr_str = TextColor.color_font('black', nbr_str)
        return nbr_str

    '''
    This numbers will mark, with quarternote/track/row number 
    is each row. 1, 5, 9 and 13 numbers font is black, to 
    highligt them from rest.
    '''    
    def alter_numbers(self, first_number=1):
        self._first_number = first_number
        for i in range(16):
            nbr = self.adjust_qnumber_str(first_number+i)
            self.alter_con_out(y=2+i, x=0, string=nbr)

    def display_played_quarter(self, played_number):
        ## alter lvl number with > sign, to show, which lvl is curenntly played:
        if (self._first_number <= played_number <= self._first_number+16):
            play_char = TextColor.color_bg('blue', '  >')
            self.alter_con_out(y=1+played_number, x=0, string=play_char)
            prev_played_nbr = self._played_number
            ## alter previous > sign with quarter note number if needed:
            if (
                (prev_played_nbr is not None)
                and (self._first_number <= prev_played_nbr <= self._first_number+16)
                ):
                nbr_str = self.adjust_qnumber_str(prev_played_nbr)
                self.alter_con_out(y=1+prev_played_nbr, x=0, string=nbr_str)
            self._played_number = played_number

    def alter_track_names(self, track_names={}, page=1):
        '''
        8 tracks visible on screen, but more are available.
        User by toggling pages, change displayed tracks on which he operates.
        '''
        for i in range(8):
            track = i + (8 * (page-1))
            if track in track_names:
                name = columns[track]
                for j in range(5 - len(name)):
                    name + ' '
            else:
                name = 'Empty' 
            name = TextColor.color_bg('blue', name)
            self.alter_con_out(y=0, x=3+i*6, string=name)

    def draw_pots_values(self, bpm, swing, vol):
        # x is char on x axis, where the tracks ends, and the song info starts:
        x = 3 + 6*8
        info_text = 'BPM:    Swing:  bVOL:   '
        for i in range(3):
            value_to_print = 0
            match i:
                case 0: 
                    value_to_print = bpm
                case 1: 
                    value_to_print = swing
                case 2: 
                    value_to_print = vol
            # swing can varries between -50% and 50%:
            if (i == 1):
                if value_to_print < 0:
                    sign = '-'
                else:
                    sign = ' '
                value_to_print = str(abs(value_to_print))
                how_many_fills = 2 - len(value_to_print)
                value_to_print = sign + '0'*how_many_fills + value_to_print
            else:
                value_to_print = str(value_to_print)
                how_many_fills = 3 - len(value_to_print)
                value_to_print = '0'*how_many_fills + value_to_print

            for j in range(11):
                if (j < 8):
                    self._screen_matrix[1+i][x+j] = info_text[:1]
                    info_text = info_text[1:]
                else:
                    self._screen_matrix[1+i][x+j] = value_to_print[:1]
                    value_to_print = value_to_print[1:]
        return self._screen_matrix 

    def put_tracker_data(cursor):
        self.draw_tracks()
        self.draw_numbers()

if __name__ == '__main__':
    import time
    columns = {0: 'idk', 2: 'Drumz', 4:'MIDI'}
    test_tracks = {1: {1: 120}, 3: {1: 666}}
    test_track2 = {1: {1: ['C5', 'F'], 3: ['C#5', '4']}}
    cursor = [1, 1]
    tracker = TrackerLike(iskmscon=False)
    tracker.draw_pots_values(180, -10, 100)
    tracker.draw_tracks()
    tracker.print()
    tracker.alter_numbers()
    tracker.alter_track_names(columns)
    time.sleep(2)
    tracker.display_played_quarter(1)
    time.sleep(2)
    tracker.display_played_quarter(2)
    time.sleep(2)
    tracker.alter_numbers()