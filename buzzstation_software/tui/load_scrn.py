from scrmx import ScreenMatrix
from txtcolor import TextColor

class LoadingScreen(ScreenMatrix):
    def __init__(self):
        super().__init__(iskmscon=False)
        self.draw_box(x=0, y=0, x_siz=64, y_siz=17)
        self.draw_ascii_art(x_start=8, y_start=6)

    def get_ascii_art(self):
        ascii_txt_loading = []
        empty_line = ' ' * 48
        ascii_txt_loading.append('  _     ___    _    ____ ___ _   _  ____        ')
        ascii_txt_loading.append(' | |   / _ \  / \  |  _ \_ _| \ | |/ ___|       ')
        ascii_txt_loading.append(' | |  | | | |/ _ \ | | | | ||  \| | |  _        ')
        ascii_txt_loading.append(' | |__| |_| / ___ \| |_| | || |\  | |_| |_ _ _  ')
        ascii_txt_loading.append(' |_____\___/_/   \_\____/___|_| \_|\____(_|_|_) ')
        ascii_txt_loading.append(empty_line)
        return ascii_txt_loading

    def draw_ascii_art(self, x_start, y_start):
        ascii_txt_loading = self.get_ascii_art()
        for i in range(len(ascii_txt_loading)):
            line = TextColor.blinking(ascii_txt_loading[i])
            self.alter_con_out(y=y_start+i, x=x_start, string=line)

if __name__ == '__main__':
    LoadingScreen()
