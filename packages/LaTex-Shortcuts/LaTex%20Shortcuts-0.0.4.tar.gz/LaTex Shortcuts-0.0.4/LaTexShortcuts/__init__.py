import keyboard


def run():
    keyboard.add_hotkey('ctrl+alt+f', keyboard.write, args=("\\frac{}{}",))
    keyboard.add_hotkey('ctrl+alt+i', keyboard.write, args=("\\int{dx}",))
    keyboard.add_hotkey('ctrl+alt+d', keyboard.write, args=("\\frac{d}{dx}",))
    keyboard.add_hotkey('ctrl+alt+g', keyboard.write, args=("{}",))
    keyboard.add_hotkey('ctrl+alt+l', keyboard.write, args=("\\lim_{x->}",))
    keyboard.add_hotkey('ctrl+alt+a', keyboard.write, args=("\\infty",))
    keyboard.add_hotkey('ctrl+alt+s', keyboard.write, args=("\\space ",))

    keyboard.wait()


if __name__ == '__main__':
    run()