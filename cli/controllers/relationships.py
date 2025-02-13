from difflib import get_close_matches
import json
from typer import Exit, confirm
from cli import app
from cli.controllers.normalize_format import listify_object
from challenge import discover_most_likely_god, make_family_tree
from rich.progress import Progress, SpinnerColumn, TextColumn


@app.command()
def get_most_likely(
    query: str,
    description_weight: int = 3,
    is_file: bool = False,
    verbose: bool = False,
):
    """
    Pass in an item to find the most likely Deity to have created it!

    Required Params:
        query: Either the name of an existing item, or a file path to a JSON representation of an item. Will do fuzzy searching to help in case of typos
    Optional Params:
        description-weight(default: 3): An integer multiplier to the weight of the description vectors, 0 means to ignore them, 1 is to take them at standard level, and 3 is baseline. Anything 10 or above will cause the description to be the primary source of matching
        is-file: a flag to designate that query is a file path rather than an item name
        verbose: a flag to return the entire Deity's JSON rather than just the name
    """
    item_to_read = None
    if is_file:
        try:
            item_to_read = json.load(open(query))
        except FileNotFoundError:
            print(f"Error: File {query} not found. Please check your file path")
            raise Exit()
        except json.JSONDecodeError:
            print(
                f"Error: File {query} was unable to be parsed. Please check your file for errors"
            )
            raise Exit()

    else:
        items = json.load(open("items.json"))
        if isinstance(items, dict):
            items = listify_object(items, "item")
        item_names = [x["item_name"] for x in items]
        close_items = get_close_matches(query, item_names)
        for item in close_items:
            if confirm(f"Did you mean: {item}"):
                item_to_read = [x for x in items if x["item_name"] == item]
                break
        if not item_to_read:
            print(f"Hmmmm.. I'm not sure what item '{query}' is. Please try again")
            raise Exit()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Looking for connections...", total=None)
            originator = discover_most_likely_god(item_to_read, description_weight)
            print(f"The most likely god to have created {item} is:")
            if verbose:
                print(json.dumps(originator, indent=1))
            else:
                print(originator["deity_name"])


@app.command()
def family_tree(description_weight: int = 3, distance_cutoff: float = 7.5):
    """
    Utilizes AI to try to figure out the relationships between Deities, returns a list of inferred relationships, based on the descriptions of items, and their euclidean distance from the Deities
    Optional Params:
        description-weight(default: 3): An integer multiplier to the weight of the description vectors, 0 means to ignore them, 1 is to take them at standard level, and 3 is baseline. Anything 10 or above will cause the description to be the primary source of matching
        distance-cutoff(default: 7.5): A float representing the max euclidean distance between an item and a Deity that still counts as a connection between them, too low and theres not enough data, too high and connections are made that aren't realistic
    """
    relationships = make_family_tree(description_weight, distance_cutoff)
    print(json.dumps(relationships, indent=2))
