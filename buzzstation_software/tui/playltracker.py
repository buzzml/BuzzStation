from tracklike import TrackerLike
from txtcolor import TextColor


class PlaylistTracker(TrackerLike):
    def __init__(self, iskmscon=True, version='2.0.0'):
        super().__init__(mode_title='Playlist', iskmscon=iskmscon)
        self.bg_software_v(version)
        self.print()

    def bg_software_v(self, version):
        line1 = 'BuzzStation'
        for i in range(len(line1)):
            char = TextColor.color_bg(self.bg_clr, line1[i]) 
            self._screen_matrix[6][51+i] = char
        line2 = f'v{version}'
        for i in range(len(line2)):
            char = TextColor.color_bg(self.bg_clr, line2[i])
            self._screen_matrix[7][53+i] = char

    def update_tui(
         self,
         bcursor=None, 
         bpm=None, 
         swing=None, 
         vol=None,
         tracks=None, 
         isplaying=None, 
         is_song_play=None,
         info_text=None
        ):
        super().update_tui(
             bcursor=bcursor, 
             bpm=bpm, 
             swing=swing, 
             vol=vol,
             tracks=tracks, 
             isplaying=isplaying, 
             is_song_play=is_song_play,
             info_text=info_text
        )

        if bcursor is not None:
            first_number = self.calc_first_nbr(bcur_y=bcursor[0])
            if self._qfirst_number != first_number:
                self._qfirst_number = first_number
                self.draw_numbers()


if __name__ == '__main__':
    pt = PlaylistTracker(False)
    pt.update_tui(bcursor=[0, 0], tracks={})
