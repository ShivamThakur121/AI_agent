def handle_api_error(e):
    print(f"API Error: {e}")
    return {"error": str(e)}

def retry_on_failure(func, retries=3):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            if attempt == retries - 1:
                raise e
