import typer


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
                    typer.secho(
                        f"[✓]{success_message}: {result}",
                        fg=typer.colors.GREEN,
                    )
                return result

            except Exception as e:
                typer.secho(f"[✗]{error_message}: {e}", fg=typer.colors.RED)
                return None

        return wrapper

    return report_outcome_decorator
