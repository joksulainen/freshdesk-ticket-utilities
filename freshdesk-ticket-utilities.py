# Import dependencies
# Modules
from datetime import date, timedelta
import re
# Tkinter toolkits
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkcalendar as tkc
# Backend
import backend

# Prepare variables
loadedTicket = None
ticketList = []
filteredView = []
statusDict = {0: "", 1: "open", 2: "pending", 3: "resolved", 4: "closed"}
companyDict = {}

# Button commands
def reloadBtnClick():
    """Called when the reload button is clicked."""
    # Since the function returns a tuple we can assign them to an equivelant
    # quantity of variables directly
    btn_reloadlist.config(state="disabled")
    btn_refreshlist.config(state="disabled")
    chk_confirm.config(state="disabled")
    btn_bulkclose.config(state="disabled")
    confirmBulkCloseVar.set(False)
    fromDates, untilDates = constructDateRanges()
    getTicketList(fromDates, untilDates)
    btn_reloadlist.config(state="normal")
    btn_refreshlist.config(state="normal")

def getTicketList(fromDates=[date.today()-timedelta(days=30)], untilDates=[date.today()]):
    """Fetches tickets from backend and appends them to global ticketList variable.\n
    Fetches the past 30 days by default."""
    global ticketList
    ticketList = []
    for x in range(len(fromDates)):
        fromDate = fromDates[x]
        untilDate = untilDates[x]
        y = 0
        while True:
            # Add 1 to y each loop for page increment
            y = y + 1
            toAppend = backend.fetchTicketList(y, fromDate, untilDate)
            if len(toAppend) == 0:
                break
            for item in toAppend:
                ticketList.append(item)
    filterView()
    refreshView()

def constructDateRanges():
    """Constructs 2 lists containing the given date range split into chunks starting from fromDate and ending at untilDate.\n
    Returns tuple containing both lists."""
    fromDate = ent_startdate.get_date()
    untilDate = ent_enddate.get_date()
    mFrom = fromDate.month
    yFrom = fromDate.year
    mUntil = fromDate.month + 1
    yUntil = fromDate.year
    if mUntil > 12:
        mUntil = 1
        yUntil = yUntil + 1
    fromDates = [fromDate]
    untilDates = [date(yUntil, mUntil, 1) - timedelta(days=1)]
    while True:
        mFrom = mFrom + 1
        if mFrom > 12:
            mFrom = 1
            yFrom = yFrom + 1
        mUntil = mFrom + 1
        yUntil = yFrom
        if mUntil > 12:
            mUntil = 1
            yUntil = yUntil + 1
        dFrom = date(yFrom, mFrom, 1)
        dUntil = date(yUntil, mUntil, 1) - timedelta(days=1)
        fromDates.insert(0, dFrom)
        if dUntil >= untilDate:
            untilDates.insert(0, untilDate)
            break
        else:
            untilDates.insert(0, dUntil)
    return fromDates, untilDates

def filterView():
    """Filters the view in treeview to include specific companies and/or statuses."""
    global filteredView
    filteredView = []
    filterByCompany = False
    filterByStatus = False
    if selectedStatus.get() == "resolved":
        chk_confirm.config(state="normal")
        btn_bulkclose.config(state="disabled")
        confirmBulkCloseVar.set(False)
    else:
        chk_confirm.config(state="disabled")
        btn_bulkclose.config(state="disabled")
        confirmBulkCloseVar.set(False)
    if sel_company.current():
        filterByCompany = True
        companyid = selectedCompany.get()
        companyid = re.search(r"([\d]+)", companyid)
        companyid = int(companyid.group())
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

def refreshView():
    """Rebuilds the view in treeview."""
    lbl_ticketcount.config(text=f"Total: {len(ticketList)} ({len(filteredView)})")
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
    """Closes all tickets in the filtered view."""
    successful = 0
    failed = 0
    for item in filteredView:
        if backend.closeTicket(item.id):
            successful = successful + 1
        else:
            failed = failed + 1
    if failed > 0:
        return messagebox.showwarning("Tickets closed", f"Successfully closed {successful} ticket(s)\nFailed to close {failed} ticket(s)\nTotal: {successful+failed}")
    else:
        return messagebox.showinfo("Tickets closed", f"Successfully closed {successful} ticket(s)")
    btn_bulkclose.config(state="disabled")
    confirmBulkCloseVar.set(False)

def confirmBulkClose():
    if confirmBulkCloseVar.get():
        btn_bulkclose.config(state="normal")
    else:
        btn_bulkclose.config(state="disabled")

def getTicket():
    """Fetches a ticket by its ID and displays details about it."""
    global loadedTicket
    try:
        loadedTicket = backend.fetchTicket(int(ticketidVar.get()))
    except ValueError:
        return messagebox.showerror("Error", "Ticket ID is not a number")
    if loadedTicket.status != "closed":
        btn_closeticket.config(state="normal")
    else:
        btn_closeticket.config(state="disabled")
    agent = backend.fetchAgent(loadedTicket.responder_id)
    try:
        companyname = loadedTicket.company['name']
        companyid = loadedTicket.company['id']
    except KeyError:
        companyname = None
        companyid = None
    lbl_details.config(text=f'ID: {loadedTicket.id}\n'
    +f'Subject: {loadedTicket.subject}\n'
    +'\n'
    +f'Status: {loadedTicket.status}\n'
    +f'Priority: {loadedTicket.priority}\n'
    +f'Escalated: {loadedTicket.is_escalated}\n'
    +f'Type: {loadedTicket.type}\n'
    +f'Tags: {", ".join(loadedTicket.tags)}\n'
    +f'Agent: {agent.contact["name"]}\n'
    +'\n'
    +f'Created: {loadedTicket.created_at.strftime("%d.%m.%Y %H.%M")}\n'
    +f'Updated: {loadedTicket.updated_at.strftime("%d.%m.%Y %H.%M")}\n'
    +f'Due by: {loadedTicket.due_by}\n'
    +f'First response by: {loadedTicket.fr_due_by}\n'
    +'\n'
    +f'Source: {loadedTicket.source}\n'
    +f'Requester: {loadedTicket.requester["name"]}\n'
    +f'E-Mail: {loadedTicket.requester["email"]}\n'
    +f'Phone: {loadedTicket.requester["phone"]}\n'
    +f'Requester ID: {loadedTicket.requester["id"]}\n'
    +f'Company: {companyname}\n'
    +f'Company ID: {companyid}')
    lbl_description.config(text=loadedTicket.description_text)

def closeTicket():
    """Closes the currently loaded ticket."""
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
frm_ticketlist = ttk.Frame(borderwidth=1, height=400, relief='raised', width=700)
ttk.Label(frm_ticketlist, text='Company').place(x=5, y=0)
selectedCompany = tk.StringVar()
sel_company = ttk.Combobox(frm_ticketlist, values='""', width=28, textvariable=selectedCompany)
sel_company.place(x=5, y=20)
ttk.Label(frm_ticketlist, text="Status").place(x=260, y=0)
selectedStatus = tk.StringVar()
sel_statusfilter = ttk.Combobox(frm_ticketlist, values='"" "open" "pending" "resolved" "closed"', width=9, textvariable=selectedStatus)
sel_statusfilter.place(x=260, y=20)
sel_statusfilter.current(3)
ttk.Label(frm_ticketlist, text='From').place(x=519, y=0)
ent_startdate = tkc.DateEntry(frm_ticketlist, locale="fi_FI", width=8)
ent_startdate.place(x=519, y=20)
ent_startdate.set_date(date.today()-timedelta(days=30))
ttk.Label(frm_ticketlist, text='Until').place(x=599, y=0)
ent_enddate = tkc.DateEntry(frm_ticketlist, locale="fi_Fi", width=8)
ent_enddate.place(x=599, y=20)
btn_bulkclose = ttk.Button(frm_ticketlist, state='disabled', text='Close tickets on page', command=bulkClose)
btn_bulkclose.place(x=5, y=45)
confirmBulkCloseVar = tk.BooleanVar()
chk_confirm = ttk.Checkbutton(frm_ticketlist, state='disabled', text='Are you sure?', variable=confirmBulkCloseVar, command=confirmBulkClose)
chk_confirm.place(x=160, y=47)
lbl_ticketcount = ttk.Label(frm_ticketlist, text="Total: ")
lbl_ticketcount.place(x=300, y=60)
btn_refreshlist = ttk.Button(frm_ticketlist, text='Refresh', command=filterView, width=7)
btn_refreshlist.place(x=535, y=45)
btn_reloadlist = ttk.Button(frm_ticketlist, text='Reload', command=reloadBtnClick, width=7)
btn_reloadlist.place(x=615, y=45)
# Treeview configuration
trv_ticketlist = ttk.Treeview(frm_ticketlist, height=14, columns=("Company", "Subject", "Status", "Created"), selectmode="browse", show="headings")
trv_ticketlist.heading("#1", text="Company")
trv_ticketlist.heading("#2", text="Subject")
trv_ticketlist.heading("#3", text="Status")
trv_ticketlist.heading("#4", text="Created")
trv_ticketlist.column("#1", stretch="no", minwidth=150, width=150)
trv_ticketlist.column("#2", stretch="yes", minwidth=200, width=200)
trv_ticketlist.column("#3", stretch="no", minwidth=70, width=70)
trv_ticketlist.column("#4", stretch="no", minwidth=80, width=80)
trv_ticketlist.place(width=660, x=10, y=80)
vsb_ticketlist = ttk.Scrollbar(frm_ticketlist, orient='vertical', command=trv_ticketlist.yview)
trv_ticketlist.config(yscrollcommand=vsb_ticketlist.set)
vsb_ticketlist.place(height=307, x=670, y=80)
frm_ticketlist.pack(anchor='nw', side='top')
# Ticket view frame
frm_ticket = ttk.Frame(borderwidth=1, height=450, relief='raised', width=700)
ttk.Label(frm_ticket, text='Description').place(x=336, y=0)
lbl_description = ttk.Label(frm_ticket, borderwidth=1, relief='sunken', font=("Arial", 10), wraplength=350)
lbl_description.place(height=420, width=355, x=336, y=20)
ttk.Label(frm_ticket, text='Ticket ID').place(x=5, y=0)
lbl_details = ttk.Label(frm_ticket, font=("Arial", 10), wraplength=315)
lbl_details.config(text='ID: \n'
+'Subject: \n'
+'\n'
+'Status: \n'
+'Priority: \n'
+'Escalated: \n'
+'Type: \n'
+'Tags: \n'
+'Agent: \n'
+'\n'
+'Created: \n'
+'Updated: \n'
+'Due by: \n'
+'First response by: \n'
+'\n'
+'Source: \n'
+'Requester: \n'
+'E-Mail: \n'
+'Phone: \n'
+'Requester ID: \n'
+'Company: \n'
+'Company ID: ')
lbl_details.place(width=315, x=5, y=50)
ticketidVar = tk.StringVar()
ent_ticketid = ttk.Entry(frm_ticket, width=10, exportselection="no", textvariable=ticketidVar)
ent_ticketid.place(x=5, y=20)
btn_getticket = ttk.Button(frm_ticket, text='Get ticket', command=getTicket)
btn_getticket.place(x=95, y=19)
btn_closeticket = ttk.Button(frm_ticket, state='disabled', text='Close ticket', command=closeTicket)
btn_closeticket.place(x=185, y=19)
frm_ticket.pack(anchor='nw', side='top')

# Event handlers
def selectTicket(e):
    """Treeview selection"""
    selectedTicket = trv_ticketlist.item(trv_ticketlist.focus())["text"]
    ticketidVar.set(selectedTicket)
    getTicket()

trv_ticketlist.bind("<Double-Button-1>", selectTicket)

# Get companies
try:
    companies = backend.fetchCompanies()
    for company in companies:
        companyDict[company.id] = company.name
except:
    messagebox.showerror("Unauthorized user",
                        "You are not authorized.\n"
                        +"Make sure your token file is formatted correctly or replace old details with newer ones.")

# Construct company combobox options
companyOptions = '"" '
for company in companyDict:
    companyOptions = companyOptions + f'"{companyDict[company]} ({company})" '
sel_company.config(values=companyOptions)

# Initial fetch
getTicketList()

# Start the main loop which in turn displays the window
win_main.mainloop()
