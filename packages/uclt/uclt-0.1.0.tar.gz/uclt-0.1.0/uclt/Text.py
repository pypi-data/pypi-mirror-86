class Colors:
  class FGColors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[0;90m"
    LIGHT_RED = "\033[0;91m"
    LIGHT_GREEN = "\033[0;92m"
    YELLOW = "\033[0;93m"
    LIGHT_BLUE = "\033[0;94m"
    LIGHT_PURPLE = "\033[0;95m"
    LIGHT_CYAN = "\033[0;96m"
    LIGHT_WHITE = "\033[0;97m"

  class BGColors:
    BLACK = "\033[0;40m"
    RED = "\033[0;41m"
    GREEN = "\033[0;42m"
    BROWN = "\033[0;43m"
    BLUE = "\033[0;44m"
    PURPLE = "\033[0;45m"
    CYAN = "\033[0;46m"
    LIGHT_GRAY = "\033[0;47m"
    DARK_GRAY = "\033[0;100m"
    LIGHT_RED = "\033[0;101m"
    LIGHT_GREEN = "\033[0;102m"
    YELLOW = "\033[0;103m"
    LIGHT_BLUE = "\033[0;104m"
    LIGHT_PURPLE = "\033[0;105m"
    LIGHT_CYAN = "\033[0;106m"
    LIGHT_WHITE = "\033[0;37m"

  def FG8bit(n):
    if not 0 <= n <= 255:
      raise Exception('n must be between 0 and 255')
    return f'\033[38;5;{n}'

  def BG8bit(n):
    if not 0 <= n <= 255:
      raise Exception('n must be between 0 and 255')
    return f'\033[48;5;{n}'

  def FGrgb(r, g, b):
    if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
      raise Exception('r, g, or b must be between 0 and 255')
    return f'\033[38;2;{r};{g};{b}'
  
  def BGrgb(r, g, b):
    if not 0 <= r <= 255 or not 0 <= g <= 255 or not 0 <= b <= 255:
      raise Exception('r, g, or b must be between 0 and 255')
    return f'\033[48;2;{r};{g};{b}'

class Types:
  BOLD = "\033[1m"
  FAINT = "\033[2m"
  ITALIC = "\033[3m"
  UNDERLINE = "\033[4m"
  BLINK = "\033[5m"
  CROSSED = "\033[9m"
  END = "\033[0m"