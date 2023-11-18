import keyboard
a=0
while True:
    if keyboard.read_key()==('w'):
        a=a+1
        print(a)

    elif keyboard.read_key()==('q'):
        print('Quit!')
        break