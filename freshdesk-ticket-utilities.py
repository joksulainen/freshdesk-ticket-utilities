# Import tkinter toolkits
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkcalendar as tkc
# Import backend
import backend

def getTicketList():
    pass

def bulkClose():
    pass

def confirmBulkClose():
    pass

def getTicket():
    global loadedTicket
    try:
        loadedTicket = backend.getTicket(int(ent_ticketid.get()))
    except ValueError:
        return messagebox.showerror("Error", "Ticket ID is not a number")
    if loadedTicket.status != "closed":
        btn_closeticket.config(state="normal")
    lbl_details.config(text=f"""ID: {loadedTicket.id}
Subject: {loadedTicket.subject}

Status: {loadedTicket.status}
Priority: {loadedTicket.priority}
Escalated: {loadedTicket.is_escalated}
Type: {loadedTicket.type}
Tags: {', '.join(loadedTicket.tags)}

Created: {loadedTicket.created_at}
Updated: {loadedTicket.updated_at}
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
    pass

# Create GUI
win_main = tk.Tk()
frm_ticketlist = ttk.Frame(borderwidth='1', height='450', relief='raised', width='450')
u0 = ttk.Label(frm_ticketlist, text='Company ID')
u0.place(x='5', y='0')
ent_companyid = ttk.Entry(frm_ticketlist, width='15')
ent_companyid.place(x='5', y='20')
u1 = ttk.Label(frm_ticketlist, text='From')
u1.place(x='105', y='0')
ent_startdate = tkc.DateEntry(frm_ticketlist, width='12')
ent_startdate.place(x='105', y='20')
u2 = ttk.Label(frm_ticketlist, text='Until')
u2.place(x='205', y='0')
ent_enddate = tkc.DateEntry(frm_ticketlist, width='12')
ent_enddate.place(x='205', y='20')
btn_refreshlist = ttk.Button(frm_ticketlist, text='Refresh and filter', command=getTicketList)
btn_refreshlist.place(x='305', y='19')
btn_bulkclose = ttk.Button(frm_ticketlist, state='disabled', text='Close tickets on page', command=bulkClose)
btn_bulkclose.place(x='5', y='45')
bulkCloseConfirm = tk.BooleanVar()
chk_confirm = ttk.Checkbutton(frm_ticketlist, offvalue='False', onvalue='True', state='disabled', text='Are you sure?', variable=bulkCloseConfirm, command=confirmBulkClose)
chk_confirm.place(x='128', y='47')
sel_statusfilter = ttk.Combobox(frm_ticketlist, validate='focusout', values='"" "open" "pending" "resolved" "closed"', width='13')
sel_statusfilter.place(x='305', y='45')
trv_ticketlist = ttk.Treeview(frm_ticketlist, height='14')
trv_ticketlist.place(width='410', x='10', y='80')
scrl_ticketlist = ttk.Scrollbar(frm_ticketlist, orient='vertical')
scrl_ticketlist.place(height='307', x='420', y='80')
frm_ticketlist.pack(anchor='n', side='left')
frm_ticket = ttk.Frame(borderwidth='1', height='450', relief='raised', width='600')
u3 = ttk.Label(frm_ticket, text='Description')
u3.place(x='236', y='0')
lbl_description = ttk.Label(frm_ticket, borderwidth='1', relief='sunken', wraplength='350')
lbl_description.place(height='420', width='355', x='236', y='20')
u4 = ttk.Label(frm_ticket, text='Ticket ID')
u4.place(x='5', y='0')
lbl_details = ttk.Label(frm_ticket)
lbl_details.configure(text='''ID: 
Subject: 

Status: 
Priority: 
Escalated: 
Type: 
Tags: 

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
Company ID: ''', wraplength='220')
lbl_details.place(width='220', x='5', y='50')
ent_ticketid = ttk.Entry(frm_ticket, width='10')
ent_ticketid.place(x='5', y='20')
btn_getticket = ttk.Button(frm_ticket, text='Get ticket', command=getTicket)
btn_getticket.place(x='75', y='19')
btn_closeticket = ttk.Button(frm_ticket, state='disabled', text='Close ticket', command=closeTicket)
btn_closeticket.place(x='155', y='19')
frm_ticket.pack(anchor='n', side='left')


# Event handler
# Define functions
#def getTicket(e):
#    global loadedTicket
#    try:
#        loadedTicket = backend.getTicket(int(ent_ticketid.get()))
#    except ValueError:
#        return messagebox.showerror("Error", "Ticket ID is not a number")
#    if loadedTicket.status != "closed":
#        btn_closeticket.config(state="normal")
#    lbl_ticketid.config(text=f"ID: {loadedTicket.id}")
#    lbl_ticketsubject.config(text=f"Subject: {loadedTicket.subject}")
#    lbl_ticketstatus.config(text=f"Status: {loadedTicket.status}")
#    lbl_ticketpriority.config(text=f"Priority: {loadedTicket.priority}")
#    lbl_ticketescalated.config(text=f"Escalated: {loadedTicket.is_escalated}")
#    lbl_tickettype.config(text=f"Type: {loadedTicket.type}")
#    lbl_tickettags.config(text=f"Tags: {', '.join(loadedTicket.tags)}")
#    lbl_ticketcreated.config(text=f"Created: {loadedTicket.created_at}")
#    lbl_ticketupdated.config(text=f"Updated: {loadedTicket.updated_at}")
#    lbl_ticketdueby.config(text=f"Due by: {loadedTicket.due_by}")
#    lbl_ticketfirstresponse.config(text=f"First response by: {loadedTicket.fr_due_by}")
#    lbl_ticketsource.config(text=f"Source: {loadedTicket.source}")
#    lbl_ticketrequester.config(text=f"Requester: {loadedTicket.requester['name']}")
#    lbl_ticketemail.config(text=f"E-Mail: {loadedTicket.requester['email']}")
#    lbl_ticketphone.config(text=f"Phone: {loadedTicket.requester['phone']}")
#    lbl_ticketrequesterid.config(text=f"Requester ID: {loadedTicket.requester['id']}")
#    lbl_ticketcompany.config(text=f"Company: {loadedTicket.company['name']}")
#    lbl_ticketcompanyid.config(text=f"Company ID: {loadedTicket.company['id']}")

#def closeTicket(e):
#    if btn_closeticket["state"] == "disabled":
#        return
#    if not loadedTicket:
#        return messagebox.showerror("No ticket loaded", "There is no ticket loaded to have its status updated")
#    if backend.closeTicket(loadedTicket.id):
#        getTicket(loadedTicket.id)
#        btn_closeticket.config(state="disabled")
#    else:
#        messagebox.showerror("Ticket update failed", "The ticket could not be updated")

#def resolveTicketTest(e):
#    if backend.resolveTicketTest(loadedTicket.id):
#        getTicket(loadedTicket.id)
#    else:
#        messagebox.showerror("Ticket update failed", "The ticket could not be updated")

# Start the main loop which in turn displays the window
win_main.mainloop()