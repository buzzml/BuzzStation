from tracklike import TrackerLike
from txtcolor import TextColor


class SampleTracker(TrackerLike):
    def __init__(self, smpls_playltrack, iskmscon=True, triplets=False):
        if triplets:
            stripes = 3
        else:
            stripes = 4
        super().__init__(
             mode_title=f'Samples{smpls_playltrack}',
             iskmscon=iskmscon,
             triplets=triplets,
             qfirst_number=0,
             stripes=stripes
        )
        self.draw_menu()

    def put_data(
         self, bcursor=None, bpm=None, swing=None, vol=None,
         tracks=None, isplaying=False, is_song_play=None,
         info_text=None, tracker_data=None
    ):
        super().put_data(  
             bcursor=bcursor, 
             bpm=bpm, 
             swing=swing, 
             vol=vol,
             tracks=tracks, 
             isplaying=isplaying, 
             is_song_play=is_song_play, 
             info_text=info_text
        )

        if tracker_data is not None:
            self.draw_tracker_data(tracker_data)

    def draw_menu(self, selected=None, menu_y_str=7):
        ## Draw 'Menu:' Title:
        string = TextColor.color_bg('blue', 'Menu:')
        self.alter_con_out(y=menu_y_str, x=55, string=string)
        ## Draw toggling pattern buttons:
        string = TextColor.color_bg('blue', 'pattern:')
        self.alter_con_out(y=menu_y_str+1, x=51, string=string)
        butt1 = '⇽'
        if selected == 'prev':
            butt1 = TextColor.selected_text(butt1)
        butt2 = '⇾'
        if selected == 'next':
            butt2 = TextColor.selected_text(butt2)
        space = TextColor.color_bg('blue', ' ')
        string = butt1 + space + butt2
        self.alter_con_out(y=menu_y_str+1, x=60, string=string)
        ## Clone pattern button:
        string = ' Clone '
        if selected == 'clone':
            string = TextColor.selected_text(string)
        self.alter_con_out(y=menu_y_str+2, x=53, string=string)
        string = ' Clear '
        if selected == 'clear':
            string = TextColor.selected_text(string)
        self.alter_con_out(y=menu_y_str+3, x=53, string=string)

    ## Draw sample notes and volumes on tracks:
    def draw_tracker_data(self, tracker_data):
        t_start = ((self._page_number - 1) * 8)
        if self._triplets:
            track_length = 12
            n = 3
        else:
            track_length = 16
            n = 4
        # For each track:
        for i in range(8):
            for j in range(1, track_length+1):
                if ((t_start+i in tracker_data) and (j in tracker_data[t_start+i])):
                    if i % n == 1:
                        bg_color = 'black grey'
                    else:
                        bg_color = 'dark grey'
                    note = tracker_data[t_start+i][j]
                    to_print = note[0]
                    while (len(to_print) < 4):
                        to_print += ' '
                    to_print += note[1]
                else:
                    to_print = '.....'
                self.update_track_field(track=i, lvl=j, val=to_print)


if __name__ == '__main__':
    stracker = SampleTracker(smpls_playltrack=1, iskmscon=False)
    stracker.put_data(bcursor=[8, 8], tracks={}, info_text=('Sample name:', 60*'x'+'1'))
    tracker_data = {
                    0:{1: ['C5', 'F'], 3: ['C5', 'B']},
                    2:{1: ['A#5', '1']},
                    8: {1: ['TT', 'F'], 3: ['ST', 'B']},
                    }
    stracker.put_data(tracker_data=tracker_data)
    #stracker.update_track_field(track=1, lvl=2, val='1234')