import sys
if __name__ == "__main__":
    from kidect import kidect
    running = True
    ki = kidect()
    ki.init()

    while running:
        ki.update()
        if ki.detected():
            sys.stdout.write('!')
        else:
            sys.stdout.write('.')

    ki.close()