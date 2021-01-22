# Import dependencies

# Import Freshdesk API library
from freshdesk.api import API

desk = API("datakolmio.freshdesk.com", "QN7iapNyeE1nT0qDXooc")

testcustomer = 62006642867
ticketsPerPage = 20

divider = "-----------------------"

def mainMenu():
    while True:
        # Print choices
        print("1: List tickets")
        print("2: View ticket")
        print("3: Update ticket status")
        print("4: Exit")
        # Check input for invalid choices
        while True:
            try:
                choice = int(input("Enter choice: "))
                if choice > 4 or choice < 1:
                    print("Invalid choice")
                else:
                    break
            except ValueError:
                print("Choice is not an integer")
        # Switch-case statement because python doesn't have that
        if choice == 1:
            listTickets()
        elif choice == 2:
            viewTicket()
        elif choice == 3:
            print("Choice 3")
        elif choice == 4:
            exit()

def listTickets():
    while True:
        companyid = input("Company ID (leave empty for no filtering): ")
        if companyid == "":
            ticketlist = desk.tickets.list_tickets(filter_name=None, page=1, per_page=ticketsPerPage)
            break
        else:
            try:
                companyid = int(companyid)
                ticketlist = desk.tickets.list_tickets(filter_name=None, company_id=companyid, page=1, per_page=ticketsPerPage)
                break
            except ValueError:
                print("Company ID is not an integer")
    # Print ticketlist contents in a presentable format
    print("ID | SUBJECT | STATUS | UPDATED")
    for ticket in ticketlist:
        print(f"{ticket.id} | {ticket.subject} | {ticket.status} | {ticket.updated_at}")
    print(divider)

def viewTicket():
    while True:
        ticketid = input("Ticket ID (leave empty to go back): ")
        if ticketid == "":
            return
        else:
            try:
                ticketid = int(ticketid)
                ticket = desk.tickets.get_ticket(ticketid, "stats", "requester", "company")
                break
            except ValueError:
                print("Ticket ID is not an integer")
    print(divider)
    print(f"ID: {ticket.id}")
    print(f"Subject: {ticket.subject}")
    print(f"Description: {ticket.description_text}")
    print(divider)
    print(f"Status: {ticket.status}")
    print(f"Priority: {ticket.priority}")
    print(f"Escalated: {ticket.is_escalated}")
    print(f"Type: {ticket.type}")
    print(f"Tags: {', '.join(ticket.tags)}")
    print(divider)
    print(f"Created: {ticket.created_at}")
    print(f"Updated: {ticket.updated_at}")
    print(f"Due by: {ticket.due_by}")
    print(f"First response by: {ticket.fr_due_by}")
    print(divider)
    print(f"Source: {ticket.source}")
    print(f"Requester: {ticket.requester['name']}")
    print(f"E-mail: {ticket.requester['email']}")
    print(f"Phone: {ticket.requester['phone']}")
    print(f"Requester ID: {ticket.requester['id']}")
    print(f"Company: {ticket.company['name']}")
    print(f"Company ID: {ticket.company['id']}")
    print(divider)


mainMenu()
