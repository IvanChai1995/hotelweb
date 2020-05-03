from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

#con = sqlite3.connect("employee.db")
#print("Database opened successfuly")
#con.execute("create table Employees (id INTEGER PRIMERY KEY, name TEXT NOT NULL, email TEXT NOT NULL, address TEXT NOT NULL)")
#print("Table created successfuly")

@app.route("/")
def index():
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from Info")
	rows = cur.fetchall()
	return render_template("index.html", rows=rows)

@app.route("/repopulate")
def repopulate():
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from Employees where name is null")
	rows = cur.fetchall()
	return render_template("repopulate.html", rows=rows)

@app.route("/outpopulate")
def outpopulate():
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from Employees where StartDate is not null and EndDate is null")
	rows = cur.fetchall()
	return render_template("outpopulate.html", rows=rows)

@app.route("/add")
def add():
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from Employees")
	rows = cur.fetchall()
	return render_template("add.html", rows=rows)

@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
	msg = "msg"
	if request.method == "POST":	
		try:
			id_room = request.form["id_room"]
			name = request.form["name"]
			email = request.form["email"]
			StartDate = request.form["StartDate"]
			EndDate = request.form["EndDate"]
			with sqlite3.connect("employee.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO Employees (id,name,email,StartDate,EndDate) values (?,?,?,?,?)", (id_room, name, email, StartDate, EndDate))
				con.commit()
				msg = "Комната успешно добавлена"
		except:
			con.rollback()
			msg = "ERROR"
		finally:
			return render_template("success.html", msg=msg)
			con.close()

@app.route("/updatedetails",methods = ["POST","GET"])
def updateDetails():
	msg = "msg"
	if request.method == "POST":
		try:
			id_room = request.form["id_room"]
			name = request.form["name"]
			email = request.form["email"]
			StartDate = request.form["StartDate"]
			EndDate = request.form["EndDate"]
			with sqlite3.connect("employee.db") as con:
				cur = con.cursor()
				cur.execute("UPDATE Employees SET name=?,email=?,StartDate=?,EndDate=? WHERE id=? ", (name,email,StartDate,EndDate,id_room,))
				con.commit()
				msg = "Клиент успешно заселен в номер"
		except:
			con.rollback()
			msg = "ERROR"
		finally:
			return render_template("success.html", msg=msg)
			con.close()

@app.route("/outdatedetails",methods = ["POST","GET"])
def outdateDetails():
	msg = "msg"
	if request.method == "POST":
		try:
			id_room = request.form["id_room"]
			with sqlite3.connect("employee.db") as con:
				cur = con.cursor()
				cur.execute("UPDATE Employees SET name=NULL,email=NULL,StartDate=NULL,EndDate=NULL WHERE id=? ", (id_room,))
				con.commit()
				msg = "Клиент успешно выселен из номера"
		except:
			con.rollback()
			msg = "ERROR"
		finally:
			return render_template("success.html", msg=msg)
			con.close()

@app.route("/view")
def view():
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from Employees")
	rows = cur.fetchall()
	return render_template("view.html", rows=rows)



@app.route("/delete")
def delete():
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from Employees")
	rows = cur.fetchall()
	return render_template("delete.html", rows=rows)

@app.route("/deleterecord", methods = ["POST"])
def deleterecord():
	id = request.form["id"]
	with sqlite3.connect("employee.db") as con:
		try:
			cur = con.cursor()
			cur.execute("delete from Employees where id = ?", (id))
			msg = "record successfuly deleted"
		except:
			msg = "can't be deleted"
		finally:
			return render_template("delete_record.html",msg = msg)


if __name__ == '__main__':
	app.run(debug=True)