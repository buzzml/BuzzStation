# Colors:
RESET = "\033[0m"
BG_BLUE = "\033[48;5;93m"
BG_BLUE_DARKER = '\033[48;5;60m'
BG_GREEN = "\033[48;5;10m"
BG_GREY = "\033[47m"
BG_WHITE = "\033[48;5;15m"
BG_BLACK_GREY = "\033[48;5;235m"
BG_DARK_GREY = "\033[48;5;236m"
BG_LIGHT_GREY = "\033[48;5;237m"
FONT_BLACK = "\033[30m"
FONT_BLUE = "\033[38;5;93m"
FONT_YELLOW = "\033[38;5;226m"
FONT_GREEN = "\033[38;5;10m"
CURSOR = "\033[60;5;10m"
CURSOR1 = "\033[30;5;107m"
BG_BLUE_LIGHT = "\033[30;1;104m"
BG_SEL_BLUE = "\033[44;10;1m"
#BG_TEST_BLUE = "\033[43;5;93m"


# Change char's background color:
class TextColor():
    @staticmethod
    def color_bg(color, text):
        colored_string = ""
        match color:
            case "green":
                colored_string = (f"{BG_GREEN}{FONT_BLACK}{text}{RESET}")
            case "blue":
                colored_string = (f"{BG_BLUE}{text}{RESET}")
            case "grey":
                colored_string = (f"{BG_GREY}{FONT_BLACK}{text}{RESET}")
            case "white":
                colored_string = (f"{BG_WHITE}{FONT_BLACK}{text}{RESET}")
            case "black grey":
                colored_string = (f"{BG_BLACK_GREY}{text}{RESET}")
            case "dark grey":
                colored_string = (f"{BG_DARK_GREY}{text}{RESET}")
            case "light grey":
                colored_string = (f"{BG_LIGHT_GREY}{text}{RESET}")
            case 'dark blue':
                colored_string = (f"{BG_BLUE_DARKER}{text}{RESET}")
            case 'sel blue':
                colored_string = (f"{BG_SEL_BLUE}{text}{RESET}")
            case 'light blue':
                colored_string = (f"{BG_BLUE_LIGHT}{text}{RESET}")
            case None:
                return text
            case _:
                raise ValueError(f'No such color as "{color}" available in this method.')
        return colored_string

    @staticmethod
    def color_font(color, text):
        colored_string = ""
        match color:
            case "blue":
                colored_string = (f"{FONT_BLUE}{text}{RESET}")
            case "black":
                colored_string = (f"{FONT_BLACK}{text}{RESET}")
            case "yellow":
                colored_string = (f"{FONT_YELLOW}{text}{RESET}")
            case "green":
                colored_string = (f"{FONT_GREEN}{text}{RESET}")
            case None:
                return text
        return colored_string

    @classmethod
    def selected_text(cls, text, bg_color='grey', font_color='black'):
        text = cls.color_font(font_color, text)
        text = cls.color_bg(bg_color, text)
        return text

    def blinking(text, whitebg=True):
        text = (f"{CURSOR}{text}{RESET}")
        return text