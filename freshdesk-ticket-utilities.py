# Import tkinter toolkits
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar as tkc
# Import 
import backend

# Initialize frames
win_main = tk.Tk()
win_main.title("Freshdesk Ticket Utilities")
win_main.resizable(False, False)
frm_ticketlist = ttk.Frame(win_main, relief="raised", borderwidth=1, height=300, width=450)
frm_ticketlist.pack(side="left", anchor="n")
frm_list = ttk.Frame(frm_ticketlist, relief="sunken", borderwidth=1, height=50, width=425)
frm_list.place(x=10, y=80)
frm_ticket = ttk.Frame(win_main, relief="raised", borderwidth=1, height=450, width=500)
frm_ticket.pack(side="left", anchor="n")

# Create interface for list filtering and refreshing
ttk.Label(frm_ticketlist, text="Company ID").place(x=5, y=0)
ent_companyid = ttk.Entry(frm_ticketlist, width=15)
ent_companyid.place(x=5, y=20)

ttk.Label(frm_ticketlist, text="From").place(x=105, y=0)
ent_startdate = tkc.DateEntry(frm_ticketlist, width=12)
ent_startdate.place(x=105, y=20)

ttk.Label(frm_ticketlist, text="Until").place(x=205, y=0)
ent_enddate = tkc.DateEntry(frm_ticketlist, width=12)
ent_enddate.place(x=205, y=20)

btn_refreshlist = ttk.Button(frm_ticketlist, text="Refresh and filter")
btn_refreshlist.place(x=305, y=19)

# Ticket viewer
# Interface
ttk.Label(frm_ticket, text="Ticket ID").place(x=5, y=0)
ent_ticketid = ttk.Entry(frm_ticket, width=10)
ent_ticketid.place(x=5, y=20)
btn_getticket = ttk.Button(frm_ticket, text="Get ticket")
btn_getticket.place(x=75, y=19)
btn_closeticket = ttk.Button(frm_ticket, text="Close ticket")
btn_closeticket.place(x=150, y=19)
#btn_testticket = ttk.Button(frm_ticket, text="Resolve ticket for testing")
#btn_testticket.place(x=250, y=19)
# Ticket details
# Parameters for easy tweaking
loadedTicket = None
detailPosX = 5
detailPosY = 50
detailSpacing = 18
detailDivider = 10

lbl_ticketid = ttk.Label(frm_ticket, text="ID: ")
lbl_ticketid.place(x=detailPosX, y=detailPosY)
lbl_ticketsubject = ttk.Label(frm_ticket, text="Subject: ")
lbl_ticketsubject.place(x=detailPosX, y=detailPosY+detailSpacing)
btn_ticketdesc = ttk.Button(frm_ticket, text="Description")
btn_ticketdesc.place(x=detailPosX, y=detailPosY+detailSpacing*2)

lbl_ticketstatus = ttk.Label(frm_ticket, text="Status: ")
lbl_ticketstatus.place(x=detailPosX, y=detailPosY+detailSpacing*3+detailDivider)
lbl_ticketpriority = ttk.Label(frm_ticket, text="Priority: ")
lbl_ticketpriority.place(x=detailPosX, y=detailPosY+detailSpacing*4+detailDivider)
lbl_ticketescalated = ttk.Label(frm_ticket, text="Escalated: ")
lbl_ticketescalated.place(x=detailPosX, y=detailPosY+detailSpacing*5+detailDivider)
lbl_tickettype = ttk.Label(frm_ticket, text="Type: ")
lbl_tickettype.place(x=detailPosX, y=detailPosY+detailSpacing*6+detailDivider)
lbl_tickettags = ttk.Label(frm_ticket, text="Tags: ")
lbl_tickettags.place(x=detailPosX, y=detailPosY+detailSpacing*7+detailDivider)

lbl_ticketcreated = ttk.Label(frm_ticket, text="Created: ")
lbl_ticketcreated.place(x=detailPosX, y=detailPosY+detailSpacing*8+detailDivider*2)
lbl_ticketupdated = ttk.Label(frm_ticket, text="Updated: ")
lbl_ticketupdated.place(x=detailPosX, y=detailPosY+detailSpacing*9+detailDivider*2)
lbl_ticketdueby = ttk.Label(frm_ticket, text="Due by: ")
lbl_ticketdueby.place(x=detailPosX, y=detailPosY+detailSpacing*10+detailDivider*2)
lbl_ticketfirstresponse = ttk.Label(frm_ticket, text="First response by: ")
lbl_ticketfirstresponse.place(x=detailPosX, y=detailPosY+detailSpacing*11+detailDivider*2)

lbl_ticketsource = ttk.Label(frm_ticket, text="Source: ")
lbl_ticketsource.place(x=detailPosX, y=detailPosY+detailSpacing*12+detailDivider*3)
lbl_ticketrequester = ttk.Label(frm_ticket, text="Requester: ")
lbl_ticketrequester.place(x=detailPosX, y=detailPosY+detailSpacing*13+detailDivider*3)
lbl_ticketemail = ttk.Label(frm_ticket, text="E-Mail: ")
lbl_ticketemail.place(x=detailPosX, y=detailPosY+detailSpacing*14+detailDivider*3)
lbl_ticketphone = ttk.Label(frm_ticket, text="Phone: ")
lbl_ticketphone.place(x=detailPosX, y=detailPosY+detailSpacing*15+detailDivider*3)
lbl_ticketrequesterid = ttk.Label(frm_ticket, text="Requester ID: ")
lbl_ticketrequesterid.place(x=detailPosX, y=detailPosY+detailSpacing*16+detailDivider*3)
lbl_ticketcompany = ttk.Label(frm_ticket, text="Company: ")
lbl_ticketcompany.place(x=detailPosX, y=detailPosY+detailSpacing*17+detailDivider*3)
lbl_ticketcompanyid = ttk.Label(frm_ticket, text="Company ID: ")
lbl_ticketcompanyid.place(x=detailPosX, y=detailPosY+detailSpacing*18+detailDivider*3)


# Event handler
# Define functions
def getTicket(e):
    global loadedTicket
    try:
        loadedTicket = backend.getTicket(int(ent_ticketid.get()))
    except ValueError:
        return messagebox.showerror("Error", "Ticket ID is not a number")
    lbl_ticketid.config(text=f"ID: {loadedTicket.id}")
    lbl_ticketsubject.config(text=f"Subject: {loadedTicket.subject}")
    lbl_ticketstatus.config(text=f"Status: {loadedTicket.status}")
    lbl_ticketpriority.config(text=f"Priority: {loadedTicket.priority}")
    lbl_ticketescalated.config(text=f"Escalated: {loadedTicket.is_escalated}")
    lbl_tickettype.config(text=f"Type: {loadedTicket.type}")
    lbl_tickettags.config(text=f"Tags: {', '.join(loadedTicket.tags)}")
    lbl_ticketcreated.config(text=f"Created: {loadedTicket.created_at}")
    lbl_ticketupdated.config(text=f"Updated: {loadedTicket.updated_at}")
    lbl_ticketdueby.config(text=f"Due by: {loadedTicket.due_by}")
    lbl_ticketfirstresponse.config(text=f"First response by: {loadedTicket.fr_due_by}")
    lbl_ticketsource.config(text=f"Source: {loadedTicket.source}")
    lbl_ticketrequester.config(text=f"Requester: {loadedTicket.requester['name']}")
    lbl_ticketemail.config(text=f"E-Mail: {loadedTicket.requester['email']}")
    lbl_ticketphone.config(text=f"Phone: {loadedTicket.requester['phone']}")
    lbl_ticketrequesterid.config(text=f"Requester ID: {loadedTicket.requester['id']}")
    lbl_ticketcompany.config(text=f"Company: {loadedTicket.company['name']}")
    lbl_ticketcompanyid.config(text=f"Company ID: {loadedTicket.company['id']}")


def displayTicketDescription(e):
    global loadedTicket
    win_desc = tk.Tk()
    frm_descdetails = ttk.Frame(win_desc, height=50)
    frm_descdetails.pack(side="top", anchor="n", fill="y", expand=True)
    lbl_descdetails_id = ttk.Label(frm_descdetails, text=f"ID: {loadedTicket.id}")
    lbl_descdetails_id.place(x=5, y=0)
    lbl_descdetails_subject = ttk.Label(frm_descdetails, text=f"Subject: {loadedTicket.subject}")
    lbl_descdetails_subject.place(x=5, y=10)

    frm_desctext = ttk.Frame(win_desc)
    frm_desctext.pack(side="top", anchor="n", fill="both", expand=True)
    lbl_desctext = ttk.Label(frm_desctext, text=loadedTicket.description_text)
    lbl_desctext.place(x=5, y=0)
    win_desc.mainloop()

def closeTicket(e):
    if not loadedTicket:
        return messagebox.showerror("No ticket loaded", "There is no ticket loaded to have its status updated")
    if backend.closeTicket(loadedTicket.id):
        getTicket(loadedTicket.id)
    else:
        messagebox.showerror("Ticket update failed", "The ticket could not be updated")

#def resolveTicketTest(e):
#    if backend.resolveTicketTest(loadedTicket.id):
#        getTicket(loadedTicket.id)
#    else:
#        messagebox.showerror("Ticket update failed", "The ticket could not be updated")

def testFunc(e):
    messagebox.showinfo("Hi", ent_companyid.get())

# Bind functions to buttons
btn_getticket.bind("<Button-1>", getTicket)
btn_refreshlist.bind("<Button-1>", testFunc)
btn_ticketdesc.bind("<Button-1>", displayTicketDescription)
btn_closeticket.bind("<Button-1>", closeTicket)
#btn_testticket.bind("<Button-1>", resolveTicketTest)

# Start the main loop which in turn displays the window
win_main.mainloop()