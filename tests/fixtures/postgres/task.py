TASKS = (
    {
        'id': 1,
        'title': 'Implement authentication feature',
        'description': 'Create an authentication feature with JWT support.',
        'author_id': 1,
        'responsible_id': 2,
        'deadline': '2024-10-01 12:00:00',
        'status': 'TODO',
        'estimated_time': 5,
    },
    {
        'id': 2,
        'title': 'Design database schema',
        'description': 'Design and document the database schema for the project.',
        'author_id': 2,
        'responsible_id': 3,
        'deadline': '2024-10-05 15:00:00',
        'status': 'IN_PROGRESS',
        'estimated_time': 3,
    },
)

TASK_WATCHERS = (
    {
        'task_id': 1,
        'user_id': 3,
    },
    {
        'task_id': 1,
        'user_id': 4,
    },
    {
        'task_id': 2,
        'user_id': 1,
    },
)

TASK_EXECUTORS = (
    {
        'task_id': 1,
        'user_id': 2,
    },
    {
        'task_id': 2,
        'user_id': 3,
    },
)
