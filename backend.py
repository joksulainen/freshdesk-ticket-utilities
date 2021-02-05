# Import Freshdesk API library
from freshdesk.api import API

tokenFile = open("token.txt", "r")
tokenContents = tokenFile.read()
tokenFile.close()
tokenContents = tokenContents.splitlines()

try:
    desk = API(tokenContents[0], tokenContents[1])
except:
    exit()

tokenContents = None


# Returns a list of tickets in specified date range
def fetchTicketList(page, fromDate, untilDate):
    return desk.tickets.filter_tickets(page=page, query=f"created_at:>'{fromDate}'%20AND%20created_at:<'{untilDate}'")

# Returns ticket object
def fetchTicket(ticketid):
    return desk.tickets.get_ticket(ticketid, "stats", "requester", "company")

# Returns agent object
def fetchAgent(agentid):
    return desk.agents.get_agent(agentid)

# Returns list of companies
def fetchCompanies():
    return desk.companies.list_companies()

# Returns True on success
def closeTicket(ticketid):
    try:
        desk.tickets.update_ticket(ticketid, status=5)
        return True
    except:
        return False
