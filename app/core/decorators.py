from functools import wraps


def with_app_context(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        from app import create_app
        app = create_app()
        with app.app_context():
            return f(*args, **kwargs)
    return wrapper