import datetime
import calendar
import time
import os

'''
ATTAIN SOME PRIOR INFO
'''
# get directory
cwd = os.getcwd()
# print(cwd)

# generate necessary files/folders
if os.path.isdir('history') == False:
    os.mkdir('history')  # Makes history folder
if 'expense_log.txt' not in os.listdir():
    with open('expense_log.txt', 'w'):
        pass  # Generates expense log

# Get date
today = datetime.date.today()
# print(today)

'''
END ATTAINING SOME PRIOR INFO
'''

'''
FUNCTIONS
'''


def invalid_input_check(inp, valid_inputs):  # Handles upper. Invalid input check function. Returns new valid input.
    inp = inp.upper()

    if inp in valid_inputs:
        return inp
    else:
        while inp not in valid_inputs:
            print('Invalid input!')
            time.sleep(.25)
            inp = input('Enter valid input.\n')
            inp = inp.upper()
        return inp


def make_backup(rf):
    global cwd
    history_dir = cwd + '\history'
    os.chdir(history_dir)

    num_files = len(os.listdir()) + 1
    backup_name = 'backup{}.txt'.format(num_files)

    with open(backup_name, 'w') as wf:  # Creates copy file
        for line in rf:
            wf.write(line)

    os.chdir(cwd)


def account_read():
    with open('expense_log.txt', 'r') as rf:
        account_string = rf.readline()
        account_list = account_string.split()

    return account_list


def info_query(message):
    message = message + '\n'
    inp = input(message)
    if inp.upper() == "CANCEL":
        print("Transaction cancelled.")
        time.sleep(2)
        exit()
    return inp


'''
END FUNCTIONS
'''

print('Welcome to the Collective Expense program.')

while True:
    # Update File
    f = open('expense_log.txt')
    f.close()

    # Get Balances

    # Define balance dictionary
    try:
        account_list = account_read()
        bal_dict = dict()
        for name in account_list:
            bal_dict[name] = 0

        with open('expense_log.txt', 'r') as rf:
            receipt = rf.readlines()

            # Define numbers which start reciepts
            for name in bal_dict:
                line_num = 0
                trans_num_list = list()
                pay_num_list = list()

                for line in receipt:
                    if line.startswith('TRANS'):
                        trans_num_list.append(line_num)
                    elif line.startswith('PAYME'):
                        pay_num_list.append(line_num)

                    line_num = line_num + 1

            # Extract Transactions
            trans_dict = bal_dict
            for num in trans_num_list:

                # Extract amt
                amt_string = receipt[num + 1]
                amt = float(amt_string[1:])

                # Extract paid
                paid_string = receipt[num + 2]
                paid_list = paid_string[6:].rstrip().split()
                num_payed = len(paid_list)

                # Extract exempts
                exempt_string = receipt[num + 3]
                exempt_list = exempt_string[8:].rstrip().split()

                # Apply changes [paid]
                for name in paid_list:
                    trans_dict[name] = trans_dict[name] + amt / num_payed / 2

                # Apply changes [payers]
                # 1. Get payer list
                payer_list = list()
                for name in account_list:
                    if name not in paid_list and name not in exempt_list:
                        payer_list.append(name)
                        num_payer = len(payer_list)

                # 2. Apply payments to payer list
                for name in payer_list:
                    trans_dict[name] = trans_dict[name] - amt / num_payer / 2

            # Extract Payments
            pay_dict = bal_dict
            for num in pay_num_list:

                # Extract info
                amt_string = receipt[num + 1]
                amt = float(amt_string[1:])

                paid_string = receipt[num + 2]
                paid = paid_string[6:].rstrip()

                recieved_string = receipt[num + 3]
                recieved = recieved_string[10:].rstrip()

                # Apply change
                pay_dict[paid] = pay_dict[paid] + amt
                pay_dict[recieved] = pay_dict[recieved] - amt

            # Combine Amts of each dict
            print(pay_dict)
    except:
        pay_dict = dict()
        print(pay_dict)

    # Main Query
    inp = input('Options are: FORMAT ACCOUNTS, NEW TRANSACTION, MAKE PAYMENT, VIEW RECEIPTS, and QUIT.\n')
    valid_inputs = ['FORMAT ACCOUNTS', 'NEW TRANSACTION', 'MAKE PAYMENT', 'QUIT', 'VIEW RECEIPTS']
    inp = invalid_input_check(inp, valid_inputs)

    if inp == 'QUIT':
        break

    if inp == 'VIEW RECEIPTS':
        with open('expense_log.txt', 'r') as rf:
            for line in rf:
                print(line, end='')
                time.sleep(.1)
        print('\n')
        input('Press enter to continue.')

    if inp == 'FORMAT ACCOUNTS':
        inp = input('Options are: ADD ACCOUNT, RESTORE BACKUP, and CLEAR ALL ACCOUNTS.\n')
        valid_inputs = ['ADD ACCOUNT', 'CLEAR ALL ACCOUNTS', 'RESTORE BACKUP']
        inp = invalid_input_check(inp, valid_inputs)

        if inp == 'CLEAR ALL ACCOUNTS':
            inp = input('Are you sure? This will also delete all financial history. YES or NO.\n')
            valid_inputs = ['YES', 'NO']
            inp = invalid_input_check(inp, valid_inputs)

            if inp == 'NO':
                pass
            if inp == 'YES':
                with open('expense_log.txt', 'r') as rf:
                    make_backup(rf)  # Backs up prior to deleting

                with open('expense_log.txt', 'w'):
                    pass  # Deletes all information

        if inp == 'RESTORE BACKUP':
            inp = input('Are you sure? This will replace all financial history. YES or NO.\n')
            valid_inputs = ['YES', 'NO']
            inp = invalid_input_check(inp, valid_inputs)

            if inp == 'NO':
                pass
            if inp == 'YES':
                with open('expense_log.txt', 'r') as rf:
                    make_backup(rf)  # Backs up prior to restoring

                history_dir = cwd + '\history'  # Change to history directory
                os.chdir(history_dir)

                inp = input('Which backup would you like to restore? Full name, eg. backup3.txt\n')
                while inp not in os.listdir():
                    print('Invalid input!')
                    time.sleep(.25)
                    inp = input('Enter valid input.\n')

                with open(inp, 'r') as rf:

                    os.chdir(cwd)

                    with open('expense_log.txt', 'w') as wf:
                        for line in rf:
                            wf.write(line)

                    print('Backup restored!')
                    time.sleep(2)

        if inp == 'ADD ACCOUNT':
            with open('expense_log.txt', 'r') as rf:
                make_backup(rf)  # Make backup

            inp = input('What will the new account be named? Enter CANCEL to cancel.\n')

            if inp.upper() == 'CANCEL':
                print('Program quitting...')
                time.sleep(2)
                exit()

            account_list = account_read()
            account_list.append(inp.upper())

            account_string = ' '.join(account_list)
            with open('expense_log.txt', 'r+') as rw:
                receipt = rw.readlines()  # Saves current text file
                rec_len = len(receipt)

                with open('expense_log.txt', 'w') as wf:  # Re-generates file
                    wf.write(account_string + '\n')

                    # Rewrite all the rest of the lines
                    for line in range(1, rec_len):
                        wf.write(receipt[line])

    if inp == 'NEW TRANSACTION':
        print('Type CANCEL at any time to quit.')

        with open('expense_log.txt', 'r') as rf:  # Make Backup.
            make_backup(rf)

        # Query information
        amt = info_query('How much did the transaction cost?')
        who_paid = info_query('Who paid for this? Separate multiple names with spaces.')
        who_exempt = info_query('Who is exempt from oweing for this? Separate multiple names with spaces. Press enter if no exemptions.')
        desc = info_query('Describe the item(s) purchased. (optional)')

        # Make sure information valid
        account_list = account_read()
        if who_exempt.upper() == 'NONE':
            none_exempt = True
            write_info = True
        else:
            # Check if who_exempt is all valid
            who_exempt_list = who_exempt.split()
            for name in who_exempt_list:
                write_info = True
                if name.upper() not in account_list:
                    print('Attempted to attribute an account that does not exist. Cancelling transaction.')
                    print('Existing accounts are:', account_list)
                    time.sleep(2)
                    write_info = False
                    break

        # Check if who_paid is all valid
        who_paid_list = who_paid.split()
        for name in who_paid_list:
            write_info = True
            if name.upper() not in account_list:
                print('Attempted to attribute an account that does not exist. Cancelling transaction.')
                print('Existing accounts are:', account_list)
                time.sleep(2)
                write_info = False
                break

        # Last assurance
        if write_info == True:
            print('\n')
            print('Amount:', amt)
            print('Who paid:', who_paid)
            print('Who exempt:', who_exempt)
            print('Description:', desc)
            inp = input('Is this information correct? YES or NO\n')
            valid_inputs = ['YES', 'NO']
            inp = invalid_input_check(inp, valid_inputs)
            if inp == 'YES':
                write_info = True
            else:
                write_info = False

        # Write info
        if write_info == True:
            with open('expense_log.txt', 'a') as af:
                af.write('\n')
                af.write('\n')
                af.write('TRANSACTION\n')
                af.write('$' + amt + '\n')
                af.write('PAID: ' + who_paid.upper() + '\n')
                af.write('EXEMPT: ' + who_exempt.upper() + '\n')
                af.write('DESCRIPTION: ' + desc)

                print('Transaction saved!')
                time.sleep(1)

    if inp == 'MAKE PAYMENT':
        print('Type CANCEL at any time to quit.')

        with open('expense_log.txt', 'r') as rf:  # Make Backup.
            make_backup(rf)

        # Query information
        amt = info_query('How much was the payment?')
        who_paid = info_query('Who paid?')
        who_recieved = info_query('Who recieved the payment?')
        desc = info_query('Any notes?')

        # Make sure information valid
        account_list = account_read()
        if who_paid.upper() not in account_list or who_recieved.upper() not in account_list:
            print('Attempted to attribute an account that does not exist. Cancelling transaction.')
            print('Existing accounts are:', account_list)
            time.sleep(2)
            write_info = False
        else:
            write_info = True

        # Last assurance:
        if write_info == True:
            print('\n')
            print('Amount:', amt)
            print('Who paid:', who_paid)
            print('Who recieved:', who_recieved)
            print('Description:', desc)
            inp = input('Is this information correct? YES or NO\n')
            valid_inputs = ['YES', 'NO']
            inp = invalid_input_check(inp, valid_inputs)
            if inp == 'YES':
                write_info = True
            else:
                write_info = False

        # Write info:
        if write_info == True:
            with open('expense_log.txt', 'a') as af:
                af.write('\n')
                af.write('\n')
                af.write('PAYMENT\n')
                af.write('$' + amt + '\n')
                af.write('PAID: ' + who_paid.upper() + '\n')
                af.write('RECIEVED: ' + who_recieved.upper() + '\n')
                af.write('DESCRIPTION: ' + desc)

                print('Payment saved!')
                time.sleep(1)

'''
TODO:
    1. Make a feature that added person adds exception to all prev. Transactions
'''
