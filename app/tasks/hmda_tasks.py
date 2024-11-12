import dramatiq

@dramatiq.actor
def process_hmda_error_checking(data):
    print(data)
