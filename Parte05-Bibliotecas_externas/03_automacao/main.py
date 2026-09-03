import pyautogui as auto
import time


def ir_pesquisa():
    auto.press("tab")
    auto.press("tab")
    auto.press("tab")
    auto.press("tab")

def main():
    auto.PAUSE = 0.75
    auto.press("win")
    auto.write("firefox")
    auto.press("enter")
    auto.write("https://www.youtube.com/")
    auto.press("enter")
    auto.sleep(2)
    ir_pesquisa()
    auto.write("python")
    auto.press("enter")
    auto.sleep(2)
    auto.hotkey("ctrl", "t")
    auto.write("python.org")
    auto.press("enter")



if __name__ == "__main__":
    main()


# 
#