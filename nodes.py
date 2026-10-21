import json 
from langchain_core.messages import AIMessage 
from agents import extract_remediation_items , assign_engineer_and_priority 
from state import IncidentState 

path = "data/incident_reviews.json"

def load_incident(state: IncidentState):
    incident_id = input().strip()
    with open(path) as f:
        incidents = json.load(f)['incidents']
    for data in incidents:
        if data["incident_id"] == incident_id:
            return {
                "incident_id" : incident_id,
                "service":data['service'],
                'responders':data['responders'],
                'review':data['review'],
                'status':'extracting'
            }
    return {
        'incident_id' : incident_id,
        'service':"",
        'responders':[],
        'review':"",
        'status':'completed'
    }

def extract_fixes(state:IncidentState):
    if not state['review']:
        return {
            'tickets':[],
            'status':"completed",
            "messages":[AIMessage(content="not extracted")]
        }
    tasks = extract_remediation_items(state['review'])
    return {
        "tickets":[{"task":task,"engineer":"","priority":""} for task in tasks],
        "status":"assigning",
        "messages": [AIMessage(content="extract done")]
    }

def assign_engineers(state:IncidentState):
    res = []
    for i in state['tickets']:
        engineer , priority = assign_engineer_and_priority(i['task'],state['responders'])
        res.append({'task':i['task'],'engineer':engineer,'priority':priority})
    return {
        "tickets":res,
        "messages":[AIMessage(content="assigned engineers")]
    }

def format_summary(state: IncidentState):
    lines = [
        "INCIDENT REMEDIATION SUMMARY",
        "",
        f"Incident ID : {state['incident_id']}",
        f"Service     : {state['service']}",
        f"Responders  : {state['responders']}",
        "",
        f"Tickets ({len(state['tickets'])})"
    ]

    for i , val in enumerate(state['tickets'],start=1):
        lines.append(f"   {i}. [{val['priority']}] {val['task']}")
        lines.append(f"      Engineer: {val['engineer']}")

    return {
        "summary":"\n".join(lines),
        "status":"completed",
        "messages":[AIMessage(content="summary formated")]
    }

































































# import json
# from langchain_core.messages import AIMessage 
# from agents import extract_remediation_items , assign_engineer_and_priority
# from state import IncidentState 

# path = "data/incident_reviews.json"
# def load_incident(state:IncidentState):
#     incident_id = input().strip()
#     with open(path) as f:
#         incidents = json.load(f)['incidents']
#     for data in incidents:
#         if data['incident_id'] == incident_id:
#             return {
#                 "incident_id" : incident_id,
#                 "service" : data['service'],
#                 "responders" : data["responders"],
#                 "review" : data["review"],
#                 "status" : "extracting",
#                 "messages" : [AIMessage(content="Incident Loaded")]
#             }
#     return {
#         "incident_id" : incident_id,
#         "service" :"" ,
#         "responders" :[],
#         "review" : "",
#         "status" : "completed",
#         "messages" : [AIMessage(content="Incident Loaded")]
#     }


# def extract_fixes(state:IncidentState):
#     if not state['review']:
#         return {
#             "tickets":[],
#             "status":"completed",
#             "messages":[AIMessage(content="extract the fixes")]
#         }
#     tasks = extract_remediation_items(state['review'])
#     return {
#         "tickets":[{"task":task,"engineer":"","priority":""} for task in tasks],
#         "status":"assigning",
#         "messages":[AIMessage(content="not extracted the fixes")]

#     }


# def assign_engineers(state:IncidentState):
#     res = []
#     for i in state['tickets']:
#         engineer , priority = assign_engineer_and_priority(i['task'],state['responders'])
#         res.append({"task":i["task"],'engineer':engineer,'priority':priority})
#     return {
#         'tickets':res,
#         'meesages':[AIMessage(content="assigned engineers")]
#     }


# def format_summary(state:IncidentState):
#     lines = [
#         f"INCIDENT REMEDIATION SUMMARY",
#         "",
#         f"Incident ID : {state['incident_id']}",
#         f"Service     : {state['service']}",
#         "",
#         f"Responders  : {", ".join(state['responders'])}",
#         "",
#         f"Tickets ({len(state['tickets'])})",
#     ]
#     for i , val in enumerate(state['tickets'],start=1):
#         lines.append(f"   {i}. [{val['priority']}] {val['task']}")
#         lines.append(f"      Engineer: {val['engineer']}")

#     return {
#         "summary":"\n".join(lines),
#         "status":"completed",
#         "messages":[AIMessage(content="summary extracted")]
#     }















































# # """Load, extract, assign, and format the incident review workflow state."""

# # import json
# # from pathlib import Path

# # from langchain_core.messages import AIMessage

# # from agents import assign_engineer_and_priority, extract_remediation_items
# # from state import IncidentState


# # REVIEWS_FILE = Path(__file__).resolve().parent / "data" / "incident_reviews.json"


# # def load_incident(state: IncidentState) -> dict:
# #     """Read an identifier and load the matching incident unchanged."""
# #     incident_id = input("Enter incident ID: ").strip()
# #     with REVIEWS_FILE.open(encoding="utf-8") as file:
# #         incidents = json.load(file)["incidents"]

# #     for incident in incidents:
# #         if incident["incident_id"] == incident_id:
# #             return {
# #                 "incident_id": incident_id,
# #                 "service": incident["service"],
# #                 "responders": incident["responders"],
# #                 "review": incident["review"],
# #                 "status": "extracting",
# #                 "messages": [AIMessage(content=f"Loaded incident {incident_id}.")],
# #             }

# #     return {
# #         "incident_id": incident_id,
# #         "service": "",
# #         "responders": [],
# #         "review": "",
# #         "status": "completed",
# #         "messages": [AIMessage(content=f"Incident {incident_id} was not found.")],
# #     }


# # def extract_fixes(state: IncidentState) -> dict:
# #     """Store each extracted fix with an empty engineer and priority."""
# #     if not state["review"]:
# #         return {
# #             "tickets": [],
# #             "status": "completed",
# #             "messages": [AIMessage(content="No incident review to process.")],
# #         }

# #     tasks = extract_remediation_items(state["review"])
# #     return {
# #         "tickets": [{"task": task, "engineer": "", "priority": ""} for task in tasks],
# #         "status": "assigning",
# #         "messages": [AIMessage(content=f"Extracted {len(tasks)} tickets.")],
# #     }


# # def assign_engineers(state: IncidentState) -> dict:
# #     """Assign each fix separately, preserving the tasks and their order."""
# #     tickets = []
# #     for ticket in state["tickets"]:
# #         engineer, priority = assign_engineer_and_priority(ticket["task"], state["responders"])
# #         tickets.append({"task": ticket["task"], "engineer": engineer, "priority": priority})
# #     return {
# #         "tickets": tickets,
# #         "messages": [AIMessage(content=f"Assigned {len(tickets)} tickets.")],
# #     }


# # def format_summary(state: IncidentState) -> dict:
# #     """Format the incident details and all assigned tickets for the terminal."""
# #     lines = [
# #         "INCIDENT REMEDIATION SUMMARY",
# #         "",
# #         f"Incident ID : {state['incident_id']}",
# #         f"Service     : {state['service']}",
# #         f"Responders  : {', '.join(state['responders'])}",
# #         "",
# #         f"Tickets ({len(state['tickets'])}):",
# #     ]
# #     for index, ticket in enumerate(state["tickets"], start=1):
# #         lines.append(f"  {index}. [{ticket['priority']}] {ticket['task']}")
# #         lines.append(f"     Engineer: {ticket['engineer']}")
# #     return {
# #         "summary": "\n".join(lines),
# #         "status": "completed",
# #         "messages": [AIMessage(content="Incident remediation summary completed.")],
# #     }
