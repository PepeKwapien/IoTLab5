from tinydb import where
from src.server.serverConfig import db, file_date_format, date_format
from datetime import datetime
import time
import os

no_command = "Unknown command"


def user_interation():
    while True:
        print("\nMAIN MENU: Available commands:\n"
              "'terminal' - modify the list of terminals that can send data to the server\n"
              "'card' - check the card list\n"
              "'employee' - modify the list of employees working in the company\n"
              "'report' - check employee's work time\n"
              "'stop' - disables user's interaction with the server")

        scan = input()

        if scan == "terminal":
            terminal()
        elif scan == "card":
            card()
        elif scan == "employee":
            employee()
        elif scan == "report":
            report()
        elif scan == "stop":
            print("Shutting down!")
            break
        else:
            print(no_command)


def terminal():
    terminals = db.table('terminals')

    print("\nTERMINAL: Available subcommands:\n"
          "'list' - show the list of all available terminals\n"
          "'add {terminal number/id}' - add a terminal to the list\n"
          "'remove {terminal number/id}' - remove a terminal from the list\n"
          "'stop' - go back to the main menu")

    while True:
        scan = input()

        if scan == "list":
            print("List of terminals: ")
            t_list = "\n".join(t['id'] for t in terminals)
            print(t_list)
        elif scan == "stop":
            print("Shutting down 'terminal'")
            break
        else:
            scan = scan.split()
            if len(scan) != 2:
                print(no_command)
            elif scan[0] == "add":
                t_id = scan[1]
                exist = terminals.search(where('id') == t_id)

                if not exist:
                    terminals.insert({'id': t_id})
                    print(f"Terminal {scan[1]} added")
                else:
                    print(f"Terminal {scan[1]} already exists")

            elif scan[0] == "remove":
                t_id = scan[1]
                exist = terminals.search(where('id') == t_id)

                if exist:
                    terminals.remove(where('id') == t_id)
                    print(f"Terminal {scan[1]} removed")
                else:
                    print(f"Terminal {scan[1]} doesn't exist")
            else:
                print(no_command)


def card():
    cards = db.table("cards")
    print("List of cards registered: ")
    c_list = "\n".join(c["id"] for c in cards)
    print(c_list)


def employee():
    employees = db.table("employees")

    print("\nEMPLOYEE: Available subcommands:\n"
          "'list' - show the list of all registered employees\n"
          "'add {employee's id} {employee's first name} {employee's last name}' - add an employee to the list\n"
          "'remove {employee's id}' - remove an employee from the list\n"
          "'assign {employee's id} {card's id}' - assign a card to an employee\n"
          "'discard {employee's id}' - assign no card to an employee\n"
          "'stop' - go back to the main menu")

    while True:
        scan = input()

        if scan == "list":
            print("List of all registered employees: ")
            e_list = "\n".join(emp["id"] + "\t" + emp["first_name"] + "\t" + emp["last_name"]
                               + "\t" + emp["card_id"] for emp in employees)
            print(e_list)
        elif scan == "stop":
            print("Shutting down 'employees'")
            break
        else:
            scan = scan.split()

            if len(scan) > 4 or len(scan) < 2:
                print(no_command)
            elif len(scan) == 4 and scan[0] == "add":
                e_id = scan[1]
                exist = employees.search(where("id") == e_id)

                if not exist:
                    employees.insert({"id": e_id, "first_name": scan[2], "last_name": scan[3], "card_id": ""})
                    print(f"New employee registered - {e_id}\t{scan[2]}\t{scan[3]}")
                else:
                    print(f"ID {e_id} is not unique!")
            elif len(scan) == 2 and scan[0] == "remove":
                e_id = scan[1]
                exist = employees.search(where("id") == e_id)

                if exist:
                    employees.remove(where("id") == e_id)
                    print(f"Employee with ID {e_id} removed")
                else:
                    print(f"No employee with such ID {e_id}")
            elif len(scan) == 3 and scan[0] == "assign":
                cards = db.table("cards")
                e_id = scan[1]
                c_id = scan[2]
                exist = employees.search(where("id") == e_id)

                if not exist:
                    print(f"No employee with such ID {e_id}")
                elif exist[0]["card_id"] != "":
                    print(f"Employee {e_id} has card assigned to him. "
                          f"Discard this card if you want to assign a new one")
                else:
                    exist = cards.search(where("id") == c_id)

                    if not exist:
                        print(f"No card with such ID {c_id}")
                    else:
                        exist = employees.search(where("card_id") == c_id)

                        if exist:
                            print("One card can be assigned only to one employee")
                        else:
                            employees.update({"card_id": c_id}, where("id") == e_id)
                            print(f"Employee with ID {e_id} had his card (ID: {c_id}) assigned")
            elif len(scan) == 2 and scan[0] == "discard":
                e_id = scan[1]
                exist = employees.search(where("id") == e_id)

                if not exist:
                    print(f"No employee with such ID {e_id}")
                elif exist[0]["card_id"] == "":
                    print(f"Employee {e_id} has no card assigned")
                else:
                    employees.update({"card_id": ""}, where("id") == e_id)
                    print(f"Employee with ID {e_id} had his card removed")
            else:
                print(no_command)


def report():
    work_time = db.table("work_time")
    employees = db.table("employees")

    print("\nREPORT: Available subcommands:\n"
          "'list {employee's id}' - show the list of every work entry made by an employee\n"
          "'generate {employee's id}' - generate a csv file containing every work entry made by an employee\n"
          "'stop' - go back to the main menu")

    while True:
        scan = input()

        if scan == "stop":
            print("Shutting down 'report'")
            break
        else:
            scan = scan.split()

            if len(scan) != 2:
                print(no_command)
            else:
                e_id = scan[1]
                exist = employees.search(where("id") == e_id)

                if not exist:
                    print(f"No employee with such ID {e_id}")
                else:
                    c_id = exist[0]["card_id"]

                    if c_id == "":
                        print(f"Employee with ID {e_id} has no cards registered")
                    elif scan[0] == "list":
                        print(f"List of work entries (Card ID {c_id}): ")
                        w_list = "\n".join(w["terminal_id"] + "\t" +
                                           datetime.fromtimestamp(w["time"]).strftime(date_format)
                                           for w in work_time.search(where("card_id") == c_id))
                        print(w_list)
                    elif scan[0] == "generate":
                        specific_employee = work_time.search(where("card_id") == c_id)

                        report_name = "work_time_" + str(e_id) + "_" + str(round(time.time())) + ".csv"
                        report_path = os.path.abspath(report_name)
                        file = open(report_path, "w+")
                        file.write("TerminalID" + "," + "Date" + "," + "Time\n")

                        for se in specific_employee:
                            line = se["terminal_id"] + ","
                            line += datetime.fromtimestamp(se["time"]).strftime(file_date_format) + "\n"
                            file.write(line)

                        file.close()
                        print(f"File {report_name} was saved")

                    else:
                        print(no_command)

