# Colors:
FONT_PURPLE = "\033[38;5;93m"
BG_BLUE = "\033[48;5;93m"
BG_BLUE_DARKER = '\033[48;5;60m'
RESET = "\033[0m"
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
            case _:
                raise ValueError(f'No such color as "{color}" available in this method.')
        return colored_string

    @staticmethod
    def color_font(color, text):
        colored_string = ""
        match color:
            case "blue":
                colored_string = (f"{FONT_BLUE}{text}{RESET}")
            case "purple":
                colored_string = (f"{FONT_PURPLE}{text}{RESET}")
            case "black":
                colored_string = (f"{FONT_BLACK}{text}{RESET}")
            case "yellow":
                colored_string = (f"{FONT_YELLOW}{text}{RESET}")
            case "green":
                colored_string = (f"{FONT_GREEN}{text}{RESET}")
        return colored_string

    @classmethod
    def selected_text(cls, text):
        text = cls.color_font('black', text)
        text = cls.color_bg('grey', text)
        return text