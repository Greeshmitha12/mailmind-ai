from .mailmind_runner import run_mailmind


def execute_workflow(user_id):

    print(
        f"\nExecuting MailMind Workflow for User {user_id}"
    )

    run_mailmind(user_id)