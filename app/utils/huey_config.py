from huey import SqliteHuey

# Configure Huey with SQLite
huey = SqliteHuey(filename="instance/ec_workflows.db", immediate=False)