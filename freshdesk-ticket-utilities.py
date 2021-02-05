# Import dependencies
from datetime import datetime, timedelta
import re
# Import tkinter toolkits
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkcalendar as tkc
# Import backend
import backend

# Prepare variables
loadedTicket = None
ticketList = []
filteredView = []
statusDict = {0: "", 1: "open", 2: "pending", 3: "resolved", 4: "closed"}
companyDict = {}

# Button commands
def getTicketList():
    global ticketList, filteredView
    ticketList = []
    fromDate = ent_startdate.get_date().strftime("%Y-%m-%d")
    untilDate = ent_enddate.get_date().strftime("%Y-%m-%d")
    x = 0
    while True:
        # Add 1 to x each loop for page increment
        x = x + 1
        toAppend = backend.getTicketList(x, fromDate, untilDate)
        if len(toAppend) == 0:
            break
        for item in toAppend:
            ticketList.append(item)
    filterView()

def filterView():
    global filteredView
    filteredView = []
    filterByCompany = False
    filterByStatus = False
    if sel_company.current():
        filterByCompany = True
        companyid = selectedCompany.get()
        companyid = re.search(r"([\d]+)", companyid)
        companyid = int(companyid.group())
    if selectedStatus.get() == "resolved":
        chk_confirm.config(state="normal")
    else:
        chk_confirm.config(state="disabled")
    if sel_statusfilter.current():
        filterByStatus = True
    if filterByCompany and filterByStatus:
        for item in ticketList:
            if item.company_id == companyid:
                if item.status == selectedStatus.get():
                    filteredView.append(item)
    elif filterByCompany:
        for item in ticketList:
            if item.company_id == companyid:
                filteredView.append(item)
    elif filterByStatus:
        for item in ticketList:
            if item.status == statusDict[sel_statusfilter.current()]:
                filteredView.append(item)
    else:
        filteredView = ticketList
    refreshView()
    
def refreshView():
    if trv_ticketlist.exists(0):
        try:
            x = 0
            while True:
                trv_ticketlist.delete(x)
                x = x + 1
        except tk.TclError: pass
    for x in range(len(filteredView)):
        try:
            ticket = filteredView[x]
        except IndexError:
            return messagebox.showerror("Title", "Index error")
        try:
            company = companyDict[ticket.company_id]
        except KeyError:
            company = None
        trv_ticketlist.insert("", "end", iid=x, text=ticket.id, values=(company, ticket.subject, ticket.status, ticket.created_at.strftime("%d.%m.%Y")))

def bulkClose():
    pass

def confirmBulkClose():
    if confirmBulkCloseVar.get():
        btn_bulkclose.config(state="normal")
    else:
        btn_bulkclose.config(state="disabled")

def getTicket():
    global loadedTicket
    try:
        loadedTicket = backend.getTicket(int(ticketidVar.get()))
    except ValueError:
        return messagebox.showerror("Error", "Ticket ID is not a number")
    if loadedTicket.status != "closed":
        btn_closeticket.config(state="normal")
    else:
        btn_closeticket.config(state="disabled")
    agent = backend.getAgent(loadedTicket.responder_id)
    try:
        companyname = loadedTicket.company['name']
        companyid = loadedTicket.company['id']
    except KeyError:
        companyname = None
        companyid = None
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
Company: {companyname}
Company ID: {companyid}""")
    lbl_description.config(text=loadedTicket.description_text)

def closeTicket():
    if backend.closeTicket(loadedTicket.id):
        btn_closeticket.config(state="disabled")
        ticketidVar.set(loadedTicket.id)
        getTicket()
    else:
        messagebox.showerror("Problem with closing ticket", "An error has occurred while attempting to close ticket")

# Create GUI
win_main = tk.Tk()
win_main.resizable(False, False)
win_main.title("Freshdesk Ticket Utilities")
# Main frame
frm_ticketlist = ttk.Frame(borderwidth=1, height=400, relief='raised', width=600)
ttk.Label(frm_ticketlist, text='Company').place(x=5, y=0)
selectedCompany = tk.StringVar()
sel_company = ttk.Combobox(frm_ticketlist, values='""', width=30, textvariable=selectedCompany)
sel_company.place(x=5, y=20)
ttk.Label(frm_ticketlist, text="Status").place(x=216, y=0)
selectedStatus = tk.StringVar()
sel_statusfilter = ttk.Combobox(frm_ticketlist, values='"" "open" "pending" "resolved" "closed"', width=9, textvariable=selectedStatus)
sel_statusfilter.place(x=216, y=20)
sel_statusfilter.current(3)
ttk.Label(frm_ticketlist, text='From').place(x=419, y=0)
ent_startdate = tkc.DateEntry(frm_ticketlist, locale="fi_FI", width=8)
ent_startdate.place(x=419, y=20)
ent_startdate.set_date(datetime.today()-timedelta(days=30))
ttk.Label(frm_ticketlist, text='Until').place(x=499, y=0)
ent_enddate = tkc.DateEntry(frm_ticketlist, locale="fi_Fi", width=8)
ent_enddate.place(x=499, y=20)
btn_bulkclose = ttk.Button(frm_ticketlist, state='disabled', text='Close tickets on page', command=bulkClose)
btn_bulkclose.place(x=5, y=45)
confirmBulkCloseVar = tk.BooleanVar()
chk_confirm = ttk.Checkbutton(frm_ticketlist, state='disabled', text='Are you sure?', variable=confirmBulkCloseVar, command=confirmBulkClose)
chk_confirm.place(x=128, y=47)
btn_refreshlist = ttk.Button(frm_ticketlist, text='Refresh', command=filterView)
btn_refreshlist.place(x=415, y=45)
btn_reloadlist = ttk.Button(frm_ticketlist, text='Reload', command=getTicketList)
btn_reloadlist.place(x=495, y=45)
# Treeview configuration
trv_ticketlist = ttk.Treeview(frm_ticketlist, height=14, columns=("Company", "Subject", "Status", "Created"), selectmode="browse", show="headings")
trv_ticketlist.heading("#1", text="Company")
trv_ticketlist.heading("#2", text="Subject")
trv_ticketlist.heading("#3", text="Status")
trv_ticketlist.heading("#4", text="Created")
trv_ticketlist.column("#1", stretch="no", minwidth=200, width=200)
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
ttk.Label(frm_ticket, text='Description').place(x=236, y=0)
lbl_description = ttk.Label(frm_ticket, borderwidth=1, relief='sunken', wraplength=350)
lbl_description.place(height=380, width=355, x=236, y=20)
ttk.Label(frm_ticket, text='Ticket ID').place(x=5, y=0)
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

# Event handlers
# Treeview selection
def selectTicket(e):
    selectedTicket = trv_ticketlist.item(trv_ticketlist.focus())["text"]
    ticketidVar.set(selectedTicket)
    getTicket()

trv_ticketlist.bind("<Double-Button-1>", selectTicket)

# Get companies
companies = backend.getCompanies()
for company in companies:
    companyDict[company.id] = company.name

# Construct company combobox options
companyOptions = '"" '
for company in companyDict:
    companyOptions = companyOptions + f'"{companyDict[company]} ({company})" '
sel_company.config(values=companyOptions)

getTicketList()

# Start the main loop which in turn displays the window
win_main.mainloop()
