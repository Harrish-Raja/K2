import os 
from google import genai 
from dotenv import load_dotenv 

load_dotenv(override=True)

model = os.getenv("GEMINI_MODEL")

def extract_remediation_items(review):
    prompt = (
        "Give every remediation or follow-up action"
        "carry one action per line, each line open with marker FIX: followed by action"
        f"review:{review}"

    )
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(model=model,contents=prompt)
    return [
        line.strip().removeprefix("FIX:").strip()
        for line in response.text.splitlines()
        if line.strip().startswith("FIX:")
    ]
def assign_engineer_and_priority(task:str,responders:list[str]):
    prompt = (
        "select exactly one engineer from responder list"
        "priority to be one of High , Medium or Low , Require reply exactly two lines the first with opening ENGINEER: and the second with PRIORITY:"
        "ENGINEER:<name>\n"
        "PRIORITY:<High,Medium,orLow>\n"
        f"task:{task}\n"
        f"responders:{", ".join(responders)}"
    )   
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(model=model,contents=prompt)
    fields = {}
    for line in response.text.splitlines():
        label , sep , val = line.strip().partition(":")
        if sep and label in {"ENGINEER","PRIORITY"}:
            fields[label] = val.strip()
    engineer , priority = fields["ENGINEER"] , fields["PRIORITY"]
    return engineer,priority






















# import os 
# from google import genai 
# from dotenv import load_dotenv 

# load_dotenv(override=True)

# model = os.getenv("GEMINI_MODEL")

# def extract_remediation_items(review:str):
#     prompt = (
#         "each beginning with FIX:. "
#         f"Incident review:\n{review}"
#     )
#     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#     response  = client.models.generate_content(model=model,contents=prompt)
#     return [
#         line.strip().removeprefix("FIX:").strip()
#         for line in response.text.splitlines()
#         if line.strip().startswith("FIX:")
#     ]

# def assign_engineer_and_priority(task:str,responders:list[str]):
#     prompt = (
#     "ENGINEER: <responder name>\n"
#     "PRIORITY: <High, Medium, or Low>"
#     f"task:{task}"
#     "responders:" + " ".join(responders)
#     )
#     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#     response  = client.models.generate_content(model=model,contents=prompt)
#     fields = {}
#     for line in response.text.splitlines():
#         label , sep , val = line.strip().partition(":")
#         if sep and label in {'ENGINEER','PRIORITY'}:
#             fields[label] = val.strip()

#     engineer , priority = fields['ENGINEER'] , fields['PRIORITY']
#     return engineer,priority




















# """Gemini agents for extracting remediation fixes and assigning engineers."""

# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from google import genai


# load_dotenv(Path(__file__).resolve().parent / ".env")


# def extract_remediation_items(review: str) -> list[str]:
#     """Return the fixes reported by the model, without rewriting them."""
#     prompt = (
#         "Identify every remediation or follow-up action arising from this incident "
#         "review. Preserve any named system, deadline, and urgency in each action. "
#         "Do not invent actions. Reply with one action per line, each beginning with "
#         "FIX: followed by the action. Do not include commentary. If there are no "
#         "actions, return no FIX: lines.\n\n"
#         f"Incident review:\n{review}"
#     )
#     client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
#     response = client.models.generate_content(
#         model=os.environ["GEMINI_MODEL"], contents=prompt
#     )
#     if response.text is None:
#         raise ValueError("The extraction model returned no text.")
#     return [
#         line.strip().removeprefix("FIX:").strip()
#         for line in response.text.splitlines()
#         if line.strip().startswith("FIX:")
#     ]


# def assign_engineer_and_priority(task: str, responders: list[str]) -> tuple[str, str]:
#     """Ask the model for one responder and priority, then read its labelled reply."""
#     prompt = (
#         "Assign this remediation action to exactly one engineer from the complete "
#         "responder list below. Copy the engineer's name exactly as written. Choose "
#         "the priority as exactly High, Medium, or Low. Reply with exactly two lines:\n"
#         "ENGINEER: <responder name>\nPRIORITY: <High, Medium, or Low>\n\n"
#         f"Action: {task}\nResponders:\n" + "\n".join(responders)
#     )
#     client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
#     response = client.models.generate_content(
#         model=os.environ["GEMINI_MODEL"], contents=prompt
#     )
#     if response.text is None:
#         raise ValueError("The assignment model returned no text.")

#     fields = {}
#     for line in response.text.splitlines():
#         label, separator, value = line.strip().partition(":")
#         if separator and label in {"ENGINEER", "PRIORITY"}:
#             fields[label] = value.strip()

#     if "ENGINEER" not in fields or "PRIORITY" not in fields:
#         raise ValueError("The model reply must include ENGINEER: and PRIORITY: lines.")
#     engineer, priority = fields["ENGINEER"], fields["PRIORITY"]
#     if engineer not in responders or priority not in {"High", "Medium", "Low"}:
#         raise ValueError("The model returned an invalid engineer or priority.")
#     return engineer, priority
