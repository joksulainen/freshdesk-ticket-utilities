# Import Freshdesk API library
from freshdesk.api import API

tokenFile = open("token.txt", "r")
tokenContents = tokenFile.read()
tokenFile.close()
tokenContents = tokenContents.splitlines()

desk = API(tokenContents[0], tokenContents[1])

tokenContents = None


# API limit is 9k tickets. Do this until empty page.
def getTicketList(page, fromDate, untilDate):
    return desk.tickets.filter_tickets(page=page, query=f"created_at:>'{fromDate}'%20AND%20created_at:<'{untilDate}'")

# Returns ticket object
def getTicket(ticketid):
    return desk.tickets.get_ticket(ticketid, "stats", "requester", "company")

# Returns agent object
def getAgent(agentid):
    return desk.agents.get_agent(agentid)

# Returns list of companies
def getCompanies():
    return desk.companies.list_companies()

# Returns True on success
def closeTicket(ticketid):
    try:
        desk.tickets.update_ticket(ticketid, status=5)
        return True
    except:
        return False
