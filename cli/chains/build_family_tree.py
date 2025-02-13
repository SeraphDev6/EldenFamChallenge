import json
from pydantic import BaseModel, Field
from cli.utils.instructor_client import get_client_and_model


class RelationshipDescriptor(BaseModel):
    deity_1: str = Field(
        description="The name of the first deity in the relationship, labeled in a field as 'deity_name'"
    )
    deity_2: str = Field(
        description="The name of the second deity in the relationship, labeled in a field as 'deity_name'"
    )
    relationship: str = Field(
        description="The description of the relationship, such as 'married', 'mother', 'brother'"
    )
    confidence: float = Field(
        description="A number between 0 and 1 describing how confident you are about the relationship"
    )


client, model = get_client_and_model()


def build_tree_chain(
    item_info: str, guessed_relationships: str
) -> RelationshipDescriptor:
    item_info = json.dumps(item_info, indent=2)
    guessed_relationships = json.dumps(guessed_relationships, indent=2)
    return client.chat.completions.create(
        model=model,
        response_model=RelationshipDescriptor,
        messages=[
            {
                "role": "system",
                "content": f"""
             You are an assistant trying to help a user build a family tree of deities.
             Please return the names of two deities, labeled 'deity_name' and their relationships, as well as a confidence score
             Each of the deities are related somehow, try to use the descriptions of the item given to discover how
             Keep in mind these previous attempts to understand the relationships between these deities
             {guessed_relationships}
             But only return the relationship relevant to this item's description
             """,
            },
            {
                "role": "user",
                "content": f"Please assess the relationships based on this item: {item_info}",
            },
        ],
    )
