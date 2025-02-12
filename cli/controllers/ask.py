from cli import app
from rich.progress import Progress, SpinnerColumn, TextColumn

from cli.chains.ask_data import ReturnEnum, get_file_to_use, answer_question


@app.command()
def ask(query: str, returns: ReturnEnum = ReturnEnum.all):
    """
    Searches the data provided to answer the query from the user, using an LLM.
    Required Params:
        query: Question to be asked against the data
    Optional Params:
        returns: How much information to be returned
            all (default): Returns the context, along with the answer
            answer: Only returns the answer to the query
            context: Only returns the context for the query
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Searching for Data...", total=None)
        file = get_file_to_use(query)
        progress.add_task("Thinking...", total=None)
        answer = answer_question(query, file, returns)
        print(answer)
