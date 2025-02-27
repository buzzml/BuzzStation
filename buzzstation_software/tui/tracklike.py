from scrmx import ScreenMatrix
from txtcolor import TextColor


class TrackerLike(ScreenMatrix):
    def __init__(self, mode_title, iskmscon=True, triplets=False, qfirst_number=None, stripes=2):
        super().__init__(iskmscon)
        self._triplets = triplets
        self._stripes = stripes
        self.bg_tracks(stripes)
        self.bg_pots()
        self.bg_title(mode_title)
        self._played_number = None
        self._qfirst_number = qfirst_number #first number of curenntly displayed lvl/quarter note
        self._page_number = None
        # For erasing cursor from it's previous position:
        self._prev_selected = None #[y, x, data]

    '''
    Create rows in different color than background, divided eachother
    by line width column of background color.
    This rows will be fields for tracker notes/pattern data.
    Each second line is colored in differend shade of grey,
    therefore the rows will not be confused with each other.
    Rows are printed from 1 to 17, to leave screen row 0 for rows
    titles.
    '''
    def bg_tracks(self, stripes):
        clrd_empty_chr1 = TextColor.color_bg('black grey', '.')
        clrd_empty_chr2 = TextColor.color_bg('dark grey', '.')
        if self._triplets:
            r_end = 13
        else:
            r_end = 17
        ## 16 visible quarternotes/levels/rows:
        for y in range(1, r_end):
            track_position = 3 #from each screen matrix column track printing will start
            ## 8 tracks:
            for i in range(8):
                # 5 characters ength for track:
                for j in range(5):
                    # each second i
                    if y % stripes == 1:
                        self._screen_matrix[y][track_position+j] = clrd_empty_chr1
                    else:
                        self._screen_matrix[y][track_position+j] = clrd_empty_chr2
                track_position += 6
        return self._screen_matrix

    def bg_pots(self):
        x = 3 + 6*8
        to_print = ['BPM:', 'Swing:', 'bVOL:']
        for i in range(len(to_print)):
            for j in range(12-len(to_print[i])):
                to_print[i] += ' '
            for j in range(len(to_print[i])):
                char = to_print[i][j]
                self._screen_matrix[2+i][51+j] = char 
        return self._screen_matrix 

    def bg_title(self, title):
        x = True
        while (len(title) < 14):
            if x:
                title += ' '
                x = False
            else:
                title = ' ' + title
                x = True

        for i in range(14):
            char = title[i]
            char = TextColor.color_bg('dark blue', char)
            self._screen_matrix[0][50+i] = char
        return self._screen_matrix 

    def update_track_field(self, lvl, track, val, selected=False):
        if selected:
            string = TextColor.selected_text(val)
            fill = (' ' * (5 - len(val)))
            if lvl % self._stripes == 1:
                string += TextColor.color_bg('black grey', fill)
            else:
                string += TextColor.color_bg('dark grey', fill)
        else:
            string = val + ' '*(5 - len(val))
            if lvl % self._stripes == 1: 
                string = TextColor.color_bg('black grey', string)
            else:
                string = TextColor.color_bg('dark grey', string)
        
        x = 3 + (track * 6)
        self.alter_con_out(y=lvl+1, x=x, string=string)

    '''
    Convert quarter level number to 3 length string,
    change it color background and, if needed, font color,
    so for example number 1 can hide previous displayed
    number 100.
        This numbers will mark, with quarternote/track/row number 
    is each row. 1, 5, 9 and 13 numbers font is black, to 
    highligt them from rest.
    '''
    def adjust_qnumber_str(self, nbr):
        nbr_str = str(nbr)
        while (len(nbr_str) < 3):
            nbr_str = ' ' + nbr_str
        nbr_str = TextColor.color_bg(self.bg_clr, nbr_str)
        ## accent each beat:
        if (
            ((not self._triplets) and (nbr % 4 == 1)
            or (self._triplets) and (nbr % 3 == 1))
            ):
            nbr_str = TextColor.color_font('black', nbr_str)
        return nbr_str

    def calc_first_nbr(self, bcur_y):
        if( 
           (self._qfirst_number is None)
           or (not self._qfirst_number <= bcur_y <= self._qfirst_number+16)
          ):
            first_number = (int((bcur_y - 1) / 16) * 16)
            return first_number

    def draw_isplaying(self, isplaying, is_song_play=None):
        if self._triplets:
            y = 13
        else:
            y = 17
        if isplaying:
            string = 'Playing'
            if is_song_play:
                string += '[S]'
            else:
                string += '[P]'
            bg_color = 'green'
        else:
            string = '  Pause  '
            bg_color = 'dark blue'
        string = TextColor.color_bg(bg_color, string)
        self.alter_con_out(y=y, x=52, string=string)

    '''
    Quarer notes will be drawed each 16 notes, depending on buzzstation
    cursor position, so when cursor y is in range 1-16, levels from 1 to 16
    will be displayed.
    '''
    def draw_numbers(self):
        first_number = self._qfirst_number
        if self._triplets:
            r_end = 13
        else:
            r_end = 17
        for i in range(1, r_end):
            nbr = self.adjust_qnumber_str(first_number+i)
            self.alter_con_out(y=1+i, x=0, string=nbr)

    def calc_page_nbr(self, buzz_cursor_x):
        page_nbr = int((buzz_cursor_x) / 8) + 1
        return page_nbr

    def draw_page_nbr(self):
        page_str = f' Page: {self._page_number}  '
        page_str = TextColor.color_bg(self.bg_clr, page_str)
        if self._triplets:
            self.alter_con_out(y=12, x=52, string=page_str)
        else:
            self.alter_con_out(y=16, x=52, string=page_str)

    def draw_played_quarter(self, played_number):
        ## alter lvl number with > sign, to show, which lvl is curenntly played:
        prev_played_nbr = self._played_number       
        if (
            (played_number is not None)
            and (self._qfirst_number <= played_number <= self._qfirst_number+16)
        ):
            play_char = TextColor.color_bg(self.bg_clr, '  >')
            self.alter_con_out(y=1+played_number, x=0, string=play_char)
            self._played_number = played_number
        ## alter previous > sign with quarter note number if needed:
        if (
            (prev_played_nbr is not None)
            and (self._qfirst_number <= prev_played_nbr <= self._qfirst_number+16)
        ):
            nbr_str = self.adjust_qnumber_str(prev_played_nbr)
            self.alter_con_out(y=1+prev_played_nbr, x=0, string=nbr_str)

    def draw_track_names(self, draw_track_names={}, page=1):
        '''
        8 tracks visible on screen, but more are available.
        User by toggling pages, change displayed tracks on which he operates.
        '''
        for i in range(8):
            track = i + (8 * (page-1))
            if track in draw_track_names:
                name = columns[track]
                name += ' ' * (5 - len(name))
            else:
                name = 'Empty' 
            name = TextColor.color_bg(self.bg_clr, name)
            self.alter_con_out(y=1, x=3+i*6, string=name)

    def draw_pots_values(self, bpm=None, swing=None, vol=None, y_start=3):
        def prepare_to_display(val):
            string = str(val)
            for i in range(3-len(string)):
                string = ' ' + string
            return string

        clock_x = 60 #x coordinate, where clock value should be printed
        if bpm is not None:
            bpm = prepare_to_display(bpm)
            self.alter_con_out(y=y_start, x=clock_x, string=bpm)
        if swing is not None:
            swing = prepare_to_display(swing)
            self.alter_con_out(y=y_start+1, x=clock_x, string=swing)
        if vol is not None:
            vol = prepare_to_display(vol)
            self.alter_con_out(y=y_start+2, x=clock_x, string=vol)
    '''
    Displayed updated TUI if needed.
    bcursor stands for this software cursor, not for console cursor.
    '''

    ### 3 lines of information on side, like, full sample name of song name
    def draw_info_text(self, info_text):
        info_text = list(info_text)
        new_info_text = []
        def adjust_string(string):
            # adjust size of too short text
            x = True
            while (len(string) < 12):
                if x:
                    string += ' '
                    x = False
                else:
                    string = ' ' + string
                    x = True
            return string
        free_space = 12
        ## Exceptions:
        if (not isinstance(info_text, tuple) and (not isinstance(info_text, list))):
            raise TypeError('Variable shoud be 2 element tuple.')
        if (len(info_text) > 2):
            raise ValueError('Tuple or list shoud be 2 element long.')
        if (len(info_text[0]) > free_space):
            raise ValueError(f'Info element 0 is longer that 12. Elemenet 0 length: {len(info_text[0])}')
        if (not self._triplets):
            max_line_size = 12
            y = 12
            x = 51
        else:
            max_line_size = 47
            y = 15
            x = 3

        ellipsis = '…'
        # Cut to long text:
        new_info_text.append(info_text[0])
        new_info_text.append(info_text[1][:max_line_size]) 
        new_info_text.append(info_text[1][max_line_size:]) 
        if len(new_info_text[2]) > max_line_size:
            new_info_text[2] = new_info_text[2][max_line_size:(max_line_size * 2) - 1] + ellipsis
        for i in range(len(new_info_text)):
            new_info_text[i] = adjust_string(new_info_text[i])
            new_info_text[i] = TextColor.color_bg(self.bg_clr, new_info_text[i])
            self.alter_con_out(y=y+i, x=x, string=new_info_text[i])


    def update_tui(
         self, bcursor=None, bpm=None, swing=None, vol=None,
         tracks=None, isplaying=None, is_song_play=None,
         info_text=None
    ):
        ## Update page number:
        if bcursor is not None:
            bcur_y = bcursor[1]
            new_page_nbr = self.calc_page_nbr(bcur_y)
            if (new_page_nbr != self._page_number):
                self._page_number = new_page_nbr
                self.draw_page_nbr()
                self.draw_track_names(tracks)

        ## Update pot values:
        pots_vals = [bpm, swing, vol]
        for pot_val in pots_vals:
            if pot_val is not None:
                self.draw_pots_values(pot_val)

        ## Update if it's playing or paused:
        if ((isplaying is not None) and (is_song_play is not None)):
            self.draw_isplaying(isplaying, is_song_play)

        if info_text is not None:
            self.draw_info_text(info_text)



if __name__ == '__main__':
    #Tests:
    import time
    columns = {0: 'idk', 2: 'Drumz', 4:'MIDI'}
    test_tracks = {1: {1: 120}, 3: {1: 666}}
    test_track2 = {1: {1: ['C5', 'F'], 3: ['C#5', '4']}}
    tracker = TrackerLike(mode_title='PLAYLIST',iskmscon=False, qfirst_number=0)
    tracker.print()
    tracker.draw_numbers()
    tracker.draw_pots_values(180, -10, 100)
    tracker.update_tui(bcursor=[1, 7], tracks=columns, isplaying=True, is_song_play=False)
    tracker.update_track_field(1, 0, '12345')
    tracker.update_track_field(1, 1, 'AAAAA')
    tracker.update_track_field(2, 0, 'BB', True)
    tracker.draw_box(x=2, y=2, x_siz=10, y_siz=10, warning_box=True)
    time.sleep(2)
    tracker.draw_played_quarter(16)
    time.sleep(2)
    tracker.draw_played_quarter(1)
    time.sleep(2)
    tracker.draw_played_quarter(None)
