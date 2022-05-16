import PySimpleGUI as sg
import sqlite3

logs = 'LoginLibrary.sqLite'


def tableCheck(table_name: str):

    sql_query = f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'"

    conn = sqlite3.connect(logs) #creates connection with database
    c = conn.cursor()
    c.execute(sql_query)
    exist = c.fetchone()

    if exist[0] >= 1: #exist is a list, so checks first value to see if table exists
        conn.close()

    else:
        c.execute('CREATE TABLE logs (userid INTEGER PRIMARY KEY, username STRING, password STRING)') #creates database table
        conn.commit()
        conn.close()


def dbSearch(x): #searches the database using the username input

    conn1 = sqlite3.connect(logs) #connects to the database
    c = conn1.cursor()   
    c.execute('SELECT password FROM logs WHERE username=:chosenUser',{'chosenUser':x})
    password = c.fetchone() #returns null if the username doesn't exist
        
    if password: #runs if 'password' isn't null
        found = True
        password = str(password[0])
    else: #runs if 'password' is null (username doesn't exist)
        found = False
        password = ''
            
    conn1.commit()
    conn1.close() #closes the database connection
    return(found,password)
    

def dbAppend():

    sg.theme('DarkAmber')
    layout = [[sg.Text('Username: '), sg.Input(key = '-IN-')],
              [sg.Text('Password: '), sg.Input(key = '-IN2-')],
              [sg.Button('Enter'),sg.Button('Exit')]]

    window = sg.Window('NEW USER', layout)
    event, values = window.read()
    
    conn2 = sqlite3.connect(logs) #creates connection with database
    c = conn2.cursor()
    uname = values['-IN-']
    exists = dbSearch(uname)[0] #checks username isn't already in use

    if event == 'Exit':
        window.close()

    elif event == 'Enter':

        if exists == True:
            sg.popup("That username is taken", font=16)
            window.close()
            dbAppend() #restarts dbAppend() to clear inputted data

        elif exists == False:
            c.execute('SELECT userid FROM logs ORDER BY userid DESC LIMIT 1')
            uid = c.fetchone()
            
            if uid:
                uid = int(uid[0])+1
            else:
                uid = 1 #avoids errors if no other entries exist and uid returns null
                    
            pword = values['-IN2-']
            c.execute('INSERT INTO logs (userid, username, password) VALUES (?,?,?)',(uid, uname, pword))
            sg.popup("Success!", font=16)
            window.close()

#        elif exists == False:
#
#            if uname.isalpha(): #checks if username contains only letters
#                window.close()
#                dbAppend() #clears user input by restarting the window
#                c.execute('SELECT userid FROM logs ORDER BY userid DESC LIMIT 1')
#                uid = c.fetchone()
#            
#                if uid:
#                    uid = int(uid[0])+1
#                else:
#                    uid = 1 #avoids errors if no other entries exist and uid returns null
#                    
#                pword = values['-IN2-']
#                c.execute('INSERT INTO logs (userid, username, password) VALUES (?,?,?)',(uid, uname, pword))
#                sg.popup("Success!", font=16)
#                window.close() 
#
#            else:
#                sg.popup("Username can’t have numbers/symbols", font=16)

    conn2.commit()
    conn2.close()


def login():
    
    sg.theme('DarkAmber')
    layout = [[sg.Text('Username: '), sg.Input(key = '-IN-')],
              [sg.Text('Password: '), sg.Input(key = '-IN2-')],
              [sg.Button('Enter'),sg.Button('Exit'),sg.Button('Create new user')]]

    window = sg.Window('LOGIN', layout)

    while True:
        event, values = window.read()
        
        if event == 'Exit':
            window.close()
            break
        
        elif event == 'Enter':
            x = values['-IN-'] #takes value from username input   
            found = dbSearch(x)[0] #returns True (username exists) or False
            password = dbSearch(x)[1] #returns the password that correlates with the inputted username

            if found == False:
                sg.popup("Invalid username", font=16)
                window.close()
                login() #resets the login window, clearing any entered text
                break
            
            elif found == True: 
                if values['-IN2-'] == password: #checks password matches
                    window.close()
                    menu() #proceeds to next stage after authentication
                    break       
                else:
                    sg.popup("Incorrect password", font=16)
                    window.close()
                    login() #resets login window, clearing any entered text
                    break  
            break
        
        elif event == 'Create new user': 
            window.close() #closes login window
            dbAppend()
            login() #reopens login window after data is appended to database
            break
        

def menu():
    print('ok') #NEXT STEP


tableCheck('logs')
login()
