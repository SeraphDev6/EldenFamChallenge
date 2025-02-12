from enum import StrEnum
import json
from pydantic import BaseModel, Field
from cli.utils import get_file_list
from cli.utils.instructor_client import get_client_and_model


class FileToSearch(BaseModel):
    file_name: str = Field(
        description="The name of the file most likely to have the answer to the user's question"
    )


client, model = get_client_and_model()


def get_file_to_use(query: str) -> FileToSearch:
    files = get_file_list()
    return client.chat.completions.create(
        model=model,
        response_model=FileToSearch,
        messages=[
            {
                "role": "system",
                "content": f"""
             You are an assistant trying to help a user answer questions about the data available.
             Please return the name of the file which is most likely to contain data to help answer the user's question from the following list:
             {"\n".join(files)}
            Only return a file name which is in that list, and don't make anything up
             """,
            },
            {"role": "user", "content": query},
        ],
    )


class ReturnEnum(StrEnum):
    answer = "answer"
    context = "context"
    all = "all"


class QuestionAnswer(BaseModel):
    context: list[dict] = Field(
        description="The exact JSON found to inform the answer, including all it's attributes"
    )
    answer: str = Field(
        description="The answer to the question in a concise, friendly tone"
    )


def answer_question(query: str, file: FileToSearch, returns: ReturnEnum):
    data = json.load(open(file.file_name))
    answer = client.chat.completions.create(
        model=model,
        response_model=QuestionAnswer,
        messages=[
            {
                "role": "system",
                "content": f"""
             You are an assistant trying to help a user answer questions about the data available.
             Use only the JSON data below to assist you in answering the question, and respond with "I'm not sure" if you are unable to answer with the data.
             {data}
            Be sure to think through the question step by step as you are generating your answer.
             """,
            },
            {"role": "user", "content": query},
        ],
    )
    if returns == "all":
        return answer.model_dump_json(indent=1)
    return answer.model_dump_json(indent=1, include=returns)
