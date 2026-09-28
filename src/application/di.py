from application.interfaces import ToDoServiceProtocol, ToDoRepositoryProtocol
from application.services import ToDoService

def get_to_do_service(repo: ToDoRepositoryProtocol) -> ToDoServiceProtocol:
    return ToDoService(repo=repo)