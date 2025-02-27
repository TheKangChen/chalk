from dotenv.main import dotenv_values


def get_env_vars() -> dict:
    return dotenv_values(".env")
