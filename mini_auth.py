def auth_manager():
    print('****************************************************************************')
    print('* This is basic password input just in case you forgot to run this in a vm *')
    print('****************************************************************************')

    password = 'mal-ware'
    counter = 0

    while True:
        input_val = input('Input password: ')
        if input_val == password:
            break
        else:
            counter += 1
            log_message = 'You obviously shouldn\'t be here' if counter >= 5 else 'Wrong try again'
            print(log_message)

    return True
