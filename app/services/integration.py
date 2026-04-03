import os
from notion_client import Client

def add_resume_to_notion(profile: dict, research: str, score: int, swot: str):
    notion_token = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_token or not database_id:
        print("Notion credentials missing. Skipping Notion integration.")
        return False
        
    try:
        notion = Client(auth=notion_token)
        
        name = profile.get("name", "Unknown Candidate")
        email = profile.get("email", "N/A")
        
        new_page = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": name}}]},
                "Email": {"email": email},
                "Score": {"number": score},
            },
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "SWOT Analysis"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": swot}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "Web Research"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": research}}]
                    }
                }
            ]
        }
        
        notion.pages.create(**new_page)
        print(f"Successfully added {name} to Notion.")
        return True
    except Exception as e:
        print(f"Failed to add to Notion: {e}")
        return False
