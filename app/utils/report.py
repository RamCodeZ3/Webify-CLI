

def report_outcome(
    success: bool | None = True,
    error_message: str | None = None,
    success_message: str | None = None,
):
    def report_outcome_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

                if success:
                    print(f"[✅]{success_message}: {result}")
                return result

            except Exception as e:
                print(f"[❌]{error_message}: {e}")
                return None

        return wrapper

    return report_outcome_decorator
