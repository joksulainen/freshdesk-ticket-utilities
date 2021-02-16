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


def fetchTicketList(page, fromDate, untilDate):
    """Returns a list of tickets in specified date range."""
    return desk.tickets.filter_tickets(page=page, query=f"created_at:>'{fromDate}'%20AND%20created_at:<'{untilDate}'")

def fetchTicket(ticketid):
    """Returns ticket object."""
    return desk.tickets.get_ticket(ticketid, "stats", "requester", "company")

def fetchAgent(agentid):
    """Returns agent object."""
    return desk.agents.get_agent(agentid)

def fetchCompanies():
    """Returns list of companies."""
    return desk.companies.list_companies()

def closeTicket(ticketid):
    """Returns True on success."""
    try:
        desk.tickets.update_ticket(ticketid, status=5)
        return True
    except:
        return False
