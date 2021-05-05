def emptySeats(row, column):

    emptyFlight = [["O" for c in range(column)] for r in range(row)]
    return emptyFlight

def initialSeats(flight):

    try:
        file  = open("flask_wtforms_tutorial/reservations.txt")
        for data in file:
            reserved = data.split(",")
            row = int(reserved[1].strip())
            column = int(reserved[2].strip())
            flight[row][column] = "X"

        file.close()    
    except:
        print("ERROR loading reservation system")

    return flight

def print_flightChart(flight):
    map=""
    for row in flight:
        map+=str(row)
        map+="\n"
        
    return map


def ticket_number(first):
    className = "INFOTC4320"
    if len(className)>len(first):
        bookingID = "".join([first[i] + className[i] for i in range(len(first))]) + className[len(first):]
    elif len(className)<len(first):
        bookingID = "".join([first[i] + className[i] for i in range(len(first))]) + first[len(className):]
    else:
        bookingID = "".join([first[i] + className[i] for i in range(len(first))])
    return bookingID

def assign_seat(flight, row, seat):
    row=int(row)
    seat=int(seat)
    if flight[row-1][seat-1] == "O":
        flight[row-1][seat-1] = "X"
        
        return True, flight
    else:
        print("\nRow:{} Seat:{} is already assigned. Choose again.\n".format(row, seat))
        return False, flight

def saveToText(first_name, row, seat, bookingID):
    row=int(row)
    seat=int(seat)
    info=first_name+', '+str(row-1)+', '+str(seat-1)+', '+bookingID+'\n'
    try:
        save_data = open('flask_wtforms_tutorial/reservations.txt', 'a')
        save_data.write(info)
    except:
        print("Error updating the reservation to .txt file")

    save_data.close()
    return
def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def sales(flight, cost_matrix):
    total= 0

    for r in range(len(flight)):
        for c in range(len(flight[r])):
            if flight[r][c] == "X":
                total+= cost_matrix[r][c]
    
    return total
def admin():
    admins=[]
    admin={}
    file=open("flask_wtforms_tutorial/passcodes.txt", "r")
    for line in file:
        login = line.split(",")
        
        admin["username"]=login[0]
        admin["password"]=login[1].strip()
        admins.append(admin)
    return admins