class todo_service:
    def get_todos(repository: todo_repository = Depends(get_todo_repository)):
        return repository.get_all_todos()


