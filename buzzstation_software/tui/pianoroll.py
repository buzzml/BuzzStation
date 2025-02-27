from scrmx import ScreenMatrix
from txtcolor import TextColor


underlined_text = lambda text: (f'\033[4m{text}\033[0m')

class PianoRoll(ScreenMatrix):
    def __init__(self, iskmscon=True, triplets=False):
        super().__init__(iskmscon)
        self.__notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self._displayed_notes = []
        self._triplets=triplets
        self._last_played = None
        self.bg_quarter_note_nbrs()
        self.print()

    # Draw grids-like pattern:
    def draw_roll(self):
        line1 = ''
        line2 = ''
        '''
        half value of length below, beacuse due to colloring
        two fields are added at one loop iteration.
        '''
        if self._triplets:
            r = 6 #pattern length 12;
        else:
            r = 8 #pattern length 16
        for i in range(r):
            line1 += TextColor.color_bg('light grey', ' '*3)
            line1 += TextColor.color_bg('dark grey', ' '*3)
            line2 += TextColor.color_bg('black grey', ' '*3)
            line2 += ' ' * 3

        ## roll will fits full octave on screen:
        every_scnd = False
        for i in range(13):
            if every_scnd:
                to_print = line1
                every_scnd = False
            else:
                to_print = line2
                every_scnd = True
            self.alter_con_out(x=8, y=2+i, string=to_print)

    ## Draw above each quarter note, it's note number
    def bg_quarter_note_nbrs(self):
        if self._triplets:
            r = 12
            n = 3
        else:
            r = 16
            n = 4
        for i in range(r):
            #Size of numbers through 1 to 16 are in single char:
            char_number = chr(0x2488 + i)
            if i % n == 0:
                char_number = TextColor.color_font('black', char_number)
            self._screen_matrix[0][8+3*i] = TextColor.color_bg(self.bg_clr, char_number)

    ## Create a list of notes range which should be displayed:
    def create_displ_notes(self, first_note):
        note = first_note[:-1]
        octave = first_note[-1]
        note_indx = self.__notes.index(note)
        displ_notes = self.__notes[note_indx:]
        displ_notes += self.__notes[:note_indx+1]
        c_passed = 0
        c_count = displ_notes.count('C')
        for i in range(len(displ_notes)):
            if displ_notes[i] == 'C':
                if ((c_count > 1) and (c_passed == 0)):
                    c_passed += 1
                elif (
                    ((c_count > 1) and (c_passed == 1)) 
                    or (c_count == 1) 
                    ):
                    octave = str(1 + int(octave))
            displ_notes[i] = displ_notes[i] + octave
        self._displayed_notes = displ_notes

    '''
    Draw full octave of piano 
    on the left of the screen from choosed note:
    '''
    def draw_piano(self, selected_note):
        for i in range(13):
            note = self._displayed_notes[i]
            note_len = len(note)
            if note == selected_note:
                #note = underlined_text(note)
                pass
            while (note_len < 3):
                note = ' ' + note
                note_len += 1
            piano_key = ''
            if '#' in note:
                piano_key = (' ' * 3) + TextColor.color_bg('white', note)
            else:
                note = (' ' * 3) + note
                piano_key = TextColor.color_bg('white', note)
            self.alter_con_out(x=2, y=14-i, string=piano_key)

 
    #Draw playing or pause in colored background:
    def draw_play_pause(self, isplaying, is_song_play):
        if not isplaying:
            string = '  Pause   '
            bg_color = 'dark blue'
        else:
            string = 'Playing'
            if is_song_play:
                string += '[S]'
            else:
                string += '[P]'
            bg_color = 'green'
        string = TextColor.color_bg(bg_color, string)
        self.alter_con_out(x=54, y=17, string=string)

    '''
    Draw info about midi in form MIDIxCy,
    where's x stands for midi output, and y
    for channel.
    '''
    def draw_midi_info(self, midi_out_params):
        while (len(midi_out_params) < 5):
            midi_out_params += ' '
        midi_out_params = ' ' + midi_out_params + ' '
        string = TextColor.color_bg('dark blue', midi_out_params)
        self.alter_con_out(x=57, y=1, string=string)

    def draw_menu(self, selected_button=None):
        self.draw_box(y=4, x=14, y_siz=9, x_siz=35, title='Menu')
        ## Buttons:
        lay1 = [' ⇽P ', ' P⇾ ', 'clone']
        lay2 = ['curs+o', 'curs-o']
        lay3 = ['notes+o', 'notes-o', 'notes+s', 'notes-s',]
        buttons = [lay1, lay2, lay3]
        l_butt_len = len('notes+o') #longest button length

        for i in range(len(buttons)):
            string = ''
            for j in range(len(buttons[i])):
                pad = l_butt_len - len(buttons[i][j]) #used to center button in row
                if buttons[i][j] == selected_button:
                    string += TextColor.selected_text(buttons[i][j])
                else:
                    string += buttons[i][j]
                string += TextColor.color_bg(self.bg_clr, ' '*pad)
                string += TextColor.color_bg(self.bg_clr, ' ')
            self.alter_con_out(x=16, y=7+i*2, string=string)

    def draw_cursor(self, bcursor, note_len_cur):
        if note_len_cur:
            char = '↔' #change note length cursor
        else:
            char = '☟' #normal cursor, for inserting notes
        #char = TextColor.blinking(char)
        bc_y, bc_x = bcursor
        bc_x = (bc_x + 2) * 3
        bc_y = 17 - self._displayed_notes.index(bc_y)
        if (bc_y % 2) == 1:
            if ((bc_x/3) % 2) == 1:
                color = 'light grey'
            else:
                color = 'dark grey'
        else:
            if (bc_x % 2) == 1:
                color = 'black grey'
            else:
                color = None
        string = TextColor.color_bg(color, char)
        self.alter_con_out(x=bc_x-1, y=bc_y-4, string=string)

    def calc_first_note(self, note_pointed):
        '''
        Cursor is above the note on which is poiting, so if cursor
        should point on last note on top, scroll by one key.
        '''
        if (
            (note_pointed in self._displayed_notes)
            and (self._displayed_notes.index(note_pointed) == len(self._displayed_notes)-1)
        ):
            first_note = self._displayed_notes[1]
        #if piano was not printed alredy or if cursor points
        #on note, which key is one level below screen
        elif (
                (len(self._displayed_notes) == 0)
                or (note_pointed not in self._displayed_notes)
        ):
            first_note = note_pointed
        #Cursor is on note, which key is alredy printed:
        else:
            first_note = self._displayed_notes[0]

        return first_note

    def draw_pots_vals(self, bpm, swing, vol):
        def add_pad(val):
            string = str(val)
            while (len(string) < 3):
                string += ' '
            return string
        x_pos = 15
        ## Print clocks:
        if bpm is not None:
            bpm = add_pad(bpm)
            string = f' BPM: {bpm} '
            self.alter_con_out(x=x_pos, y=16, string=string)
        if swing is not None:
            swing = add_pad(swing)
            string = f' Swing: {swing} '
            self.alter_con_out(x=x_pos+11, y=16, string=string) 
        if vol is not None:
            vol = add_pad(vol)
            string = f' bVOL: {vol} '
            self.alter_con_out(x=x_pos+24, y=16, string=string)

    def draw_pattern_nbr(self, pattern_nbr):
        pattern_nbr = str(pattern_nbr)
        while (len(pattern_nbr) < 4):
            pattern_nbr += ' '
        string = f'Pattern {pattern_nbr}'
        string = TextColor.color_bg('dark blue', string)
        self.alter_con_out(x=0, y=17, string=string)

    def create_note_str(self, vol, note_len, ind_y):
        char = chr(0x2580 + vol)
        string = ''
        for i in range(note_len):
            if (ind_y % 2 == 1):
                if (i % 2 == 1):
                    color = 'dark grey'
                else:
                    color = 'light grey'
            else:
                if (i % 2 == 0):
                    color = 'black grey'
                else:
                    color = None
            if (i == note_len-1):
                x = 2
            else:
                x = 3
            string += TextColor.color_bg(color, char*x)
        #print(len(string))
        return string

    def draw_notes_on_roll(self, pattern):
        # For each quarter note:
        for i in range(1, 17):
            if i in pattern:
                # For each note in quarter:
                for j in range(len(pattern[i])):
                    note = pattern[i][j][0]
                    if note in self._displayed_notes:
                        vol = pattern[i][j][2]
                        note_len = pattern[i][j][1]
                        '''
                        Note graphic representation is note_len * 3 (single char size) - 1
                        -1: to distingish this note from note behind.
                        '''
                        ind_y = self._displayed_notes.index(note)
                        string = self.create_note_str(vol, note_len, ind_y)
                        self.alter_con_out(x=5+(i*3), y=14-ind_y, string=string)

    # draw arrow poinint at currently played quarter, and removes previous
    def draw_cur_play_note(self, played_qrtr):
        if self._triplets:
            n = 3
        else:
            n = 4

        if played_qrtr is not None:
            char = TextColor.color_font('green', '⇩')
            char = TextColor.color_bg(self.bg_clr, char)
            self.alter_con_out(x=8+3*played_qrtr, y=1, string=char)

        if self._last_played is not None:
            if self._last_played % n == 0:
                fcolor = 'black'
            else:
                fcolor = None
            char = chr(0x2488 + self._last_played)
            char = TextColor.color_font(fcolor, char)
            char = TextColor.color_bg(self.bg_clr, char)
            self.alter_con_out(x=8+3*self._last_played, y=1, string=char)

        self._last_played = played_qrtr


    def update_tui(self, 
             bcursor=None,
             note_len_cur=False,
             pattern=None,
             isplaying=None, 
             is_song_play=None,
             midi_out_params=None,
             selected_button=None,
             pattern_nbr=None,
             bpm=None,
             swing=None,
             vol=None,
    ):
        if ((bcursor is not None) and (pattern is not None)):
            first_note = self.calc_first_note(bcursor[0])
            if (
                (len(self._displayed_notes) == 0)
                or (first_note != self._displayed_notes[0])
            ):
                self.create_displ_notes(first_note)
            self.draw_roll()
            self.draw_notes_on_roll(pattern)
            self.draw_piano(bcursor[0])
            self.draw_cursor(bcursor, note_len_cur)

        if ((isplaying is not None) and (is_song_play is not None)):
            self.draw_play_pause(isplaying, is_song_play)

        if (midi_out_params is not None):
            self.draw_midi_info(midi_out_params)

        if selected_button is not None:
            self.draw_menu(selected_button)

        if pattern_nbr is not None:
            self.draw_pattern_nbr(pattern_nbr)

        if (
            (bpm is not None)
            or (swing is not None)
            or (vol is not None)
        ):
            self.draw_pots_vals(bpm, swing, vol)


if __name__ == '__main__':
    data = {1: [['C5', 2, 2], ['E5', 2, 2]],
        3: [['B5', 2, 1]]
    }
    pr = PianoRoll(False)
    pr.update_tui(isplaying=False, is_song_play=False, midi_out_params='M1C16')
    pr.update_tui(pattern_nbr=1)
    pr.update_tui(selected_button='clone')
    pr.update_tui(bcursor=['C5', 1], pattern=data, note_len_cur=True)
    pr.update_tui(bpm=100, swing=-5, vol=80)
    
    import time
    for i in range(1, 16):
        pr.draw_cur_play_note(played_qrtr=i)
        time.sleep(1)
    pr.draw_cur_play_note(played_qrtr=None)
    #pr.update_tui(bcursor=['C5', 3])



    '''
    ## Tests:
    import time
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    for j in range(2):
        for i in range(len(notes)-1):
            note = notes[i] + str(5+j)
            pr.update_tui(bcursor=[note, 3])
            time.sleep(0.4)
    for j in range(2):
        for i in range(len(notes)-1):
            note = notes[-(i+1)] + str(6-j)
            pr.update_tui(bcursor=[note, 3])
            time.sleep(0.4)
    '''
    