# Import dependencies
import time
# Import tkinter toolkits
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkcalendar as tkc
# Import backend
import backend

# Prepare variables
loadedTicket = None
companyDict = {}

# Button commands
def getTicketList():
    ticketlist = backend.getTicketList(1)
    for x in range(len(ticketlist)):
        ticket = ticketlist[x]
        trv_ticketlist.insert("", "end", iid=x, text=ticket.id, values=("", ticket.subject, ticket.status, ticket.created_at.strftime("%d.%m.%Y")))

def bulkClose():
    pass

def confirmBulkClose():
    if confirmBulkCloseVar.get():
        btn_bulkclose.config(state="normal")
    else:
        btn_bulkclose.config(state="disabled")

def getTicket():
    try:
        loadedTicket = backend.getTicket(int(ticketidVar.get()))
    except ValueError:
        return messagebox.showerror("Error", "Ticket ID is not a number")
    if loadedTicket.status != "closed":
        btn_closeticket.config(state="normal")
    else:
        btn_closeticket.config(state="disabled")
    agent = backend.getAgent(loadedTicket.responder_id)
    lbl_details.config(text=f"""ID: {loadedTicket.id}
Subject: {loadedTicket.subject}

Status: {loadedTicket.status}
Priority: {loadedTicket.priority}
Escalated: {loadedTicket.is_escalated}
Type: {loadedTicket.type}
Tags: {', '.join(loadedTicket.tags)}
Agent: {agent.contact["name"]}

Created: {loadedTicket.created_at.strftime("%d.%m.%Y %H.%M")}
Updated: {loadedTicket.updated_at.strftime("%d.%m.%Y %H.%M")}
Due by: {loadedTicket.due_by}
First response by: {loadedTicket.fr_due_by}

Source: {loadedTicket.source}
Requester: {loadedTicket.requester['name']}
E-Mail: {loadedTicket.requester['email']}
Phone: {loadedTicket.requester['phone']}
Requester ID: {loadedTicket.requester['id']}
Company: {loadedTicket.company['name']}
Company ID: {loadedTicket.company['id']}""")
    lbl_description.config(text=loadedTicket.description_text)

def closeTicket():
    if backend.closeTicket(loadedTicket.id):
        btn_closeticket.config(state="disabled")
    else:
        messagebox.showerror("Problem with closing ticket", "An error has occurred while attempting to close ticket")

# Create GUI
win_main = tk.Tk()
win_main.resizable(False, False)
win_main.title("Freshdesk Ticket Utilities")
# Main frame
frm_ticketlist = ttk.Frame(borderwidth=1, height=400, relief='raised', width=600)
u0 = ttk.Label(frm_ticketlist, text='Company')
u0.place(x=5, y=0)
sel_company = ttk.Combobox(frm_ticketlist, values='""', width=16)
sel_company.place(x=5, y=20)
u1 = ttk.Label(frm_ticketlist, text='From')
u1.place(x=130, y=0)
ent_startdate = tkc.DateEntry(frm_ticketlist, locale="fi_FI", width=12)
ent_startdate.place(x=130, y=20)
u2 = ttk.Label(frm_ticketlist, text='Until')
u2.place(x=230, y=0)
ent_enddate = tkc.DateEntry(frm_ticketlist, locale="fi_Fi",width=12)
ent_enddate.place(x=230, y=20)
btn_refreshlist = ttk.Button(frm_ticketlist, text='Refresh and filter', command=getTicketList)
btn_refreshlist.place(x=330, y=19)
btn_bulkclose = ttk.Button(frm_ticketlist, state='disabled', text='Close tickets on page', command=bulkClose)
btn_bulkclose.place(x=5, y=45)
confirmBulkCloseVar = tk.BooleanVar()
chk_confirm = ttk.Checkbutton(frm_ticketlist, state='disabled', text='Are you sure?', variable=confirmBulkCloseVar, command=confirmBulkClose)
chk_confirm.place(x=128, y=47)
sel_statusfilter = ttk.Combobox(frm_ticketlist, values='"" "open" "pending" "resolved" "closed"', width=13)
sel_statusfilter.place(x=330, y=45)
# Treeview configuration
trv_ticketlist = ttk.Treeview(frm_ticketlist, height=14, columns=("Company", "Subject", "Status", "Created"), selectmode="browse", show="headings")
trv_ticketlist.heading("#0", text="ID")
trv_ticketlist.heading("#1", text="Company")
trv_ticketlist.heading("#2", text="Subject")
trv_ticketlist.heading("#3", text="Status")
trv_ticketlist.heading("#4", text="Created")
trv_ticketlist.column("#1", stretch="yes", minwidth=150, width=150)
trv_ticketlist.column("#2", stretch="yes", minwidth=200, width=200)
trv_ticketlist.column("#3", stretch="no", minwidth=60, width=60)
trv_ticketlist.column("#4", stretch="no", minwidth=70, width=70)
trv_ticketlist.place(width=560, x=10, y=80)
vsb_ticketlist = ttk.Scrollbar(frm_ticketlist, orient='vertical', command=trv_ticketlist.yview)
trv_ticketlist.configure(yscrollcommand=vsb_ticketlist.set)
vsb_ticketlist.place(height=307, x=570, y=80)
frm_ticketlist.pack(anchor='nw', side='top')
# Ticket view frame
frm_ticket = ttk.Frame(borderwidth=1, height=410, relief='raised', width=600)
u3 = ttk.Label(frm_ticket, text='Description')
u3.place(x=236, y=0)
lbl_description = ttk.Label(frm_ticket, borderwidth=1, relief='sunken', wraplength=350)
lbl_description.place(height=380, width=355, x=236, y=20)
u4 = ttk.Label(frm_ticket, text='Ticket ID')
u4.place(x=5, y=0)
lbl_details = ttk.Label(frm_ticket)
lbl_details.configure(text='''ID: 
Subject: 

Status: 
Priority: 
Escalated: 
Type: 
Tags: 
Agent: 

Created: 
Updated: 
Due by: 
First response by: 

Source: 
Requester: 
E-Mail: 
Phone: 
Requester ID: 
Company: 
Company ID: ''', wraplength=220)
lbl_details.place(width=220, x=5, y=50)
ticketidVar = tk.StringVar()
ent_ticketid = ttk.Entry(frm_ticket, width=10, exportselection="no", textvariable=ticketidVar)
ent_ticketid.place(x=5, y=20)
btn_getticket = ttk.Button(frm_ticket, text='Get ticket', command=getTicket)
btn_getticket.place(x=75, y=19)
btn_closeticket = ttk.Button(frm_ticket, state='disabled', text='Close ticket', command=closeTicket)
btn_closeticket.place(x=155, y=19)
frm_ticket.pack(anchor='nw', side='top')

# Treeview selection
def selectTicket(e):
    selectedTicket = trv_ticketlist.item(trv_ticketlist.focus())["text"]
    ticketidVar.set(selectedTicket)
    getTicket()

trv_ticketlist.bind("<Double-Button-1>", selectTicket)

# Get companies
companies = backend.getCompanies()
for company in companies:
    companyDict[company.name] = company.id

# Construct company combobox options
companyOptions = '"" '
for company in companyDict:
    companyOptions = companyOptions + f'"{company} ({companyDict[company]})" '
sel_company.config(values=companyOptions)

# Start the main loop which in turn displays the window
win_main.mainloop()
