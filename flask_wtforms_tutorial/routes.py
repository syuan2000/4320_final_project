from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *
from .charts import *

seat = emptySeats(12, 4)
flight = initialSeats(seat)


#@app.route("/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    message=None
    form = AdminLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        #make sure the admin username and password are correct...
        username = request.form["username"]
        password = request.form["password"]
        cost=get_cost_matrix()
        sale=sales(flight, cost)

        file=open("flask_wtforms_tutorial/passcodes.txt", "r")
        for line in file:
            login=line.split(", ")
            if username == login[0] and password == login[1].strip():
                err= None
                chart = print_flightChart(flight)
                message= "Total sales: ${}".format(sale)
                return render_template("admin.html", form=form,template="form-template", err=err, chart = chart, message=message)

        err = "Invalid username or password. Try again. "
        chart = None
        return render_template("admin.html", form=form,template="form-template", err=err, chart = chart) 
                

    return render_template("admin.html", form=form, template="form-template")

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    chart = print_flightChart(flight)
    err=None
    message=None

    form = ReservationForm()

    if request.method == 'POST' or form.validate_on_submit():
        firstName = request.form["first_name"]
        lastName = request.form["last_name"]
        seat = request.form["seat"]
        row = request.form["row"]
        success,updateFlight=assign_seat(flight,row,seat)
        bookingID=ticket_number(firstName)
        
    
        if success:
            
            chart = print_flightChart(updateFlight)
            message = "\nCongradulation {}! Seat Row {} Seat {} has been assigned.\n".format(firstName,row, seat)
            message+= "\nYour eticket number is : " + bookingID
            saveToText(firstName, row, seat, bookingID)
            return render_template("reservations.html", form=form, template="form-template", err=err, chart = chart, message=message)
        else:
            err= "Error: Row {} Seat {} has been assigned!\n".format(row,seat)
            return render_template("reservations.html", form=form, template="form-template", err=err, chart = chart)

    return render_template("reservations.html", form=form, template="form-template",chart=chart)


