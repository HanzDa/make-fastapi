import typer
import uvicorn

from app.core.config import settings

app_cli = typer.Typer()


@app_cli.command()
def runserver(host: str = settings.SERVER_HOST, port: int = settings.SERVER_PORT, debug: bool = settings.DEBUG):
    uvicorn.run("app.main:app", host=host, port=port, reload=debug)


@app_cli.command()
def createsuperuser(
    email: str,
    password: str = typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True)
):
    async def _create_superuser():
        from app.db.session import get_db_session
        from app.core.security import get_password_hash
        from app.models.user import User
        from sqlalchemy.exc import IntegrityError

        async for session in get_db_session():
            try:
                user = User(
                    email=email,
                    hashed_password=get_password_hash(password),
                    is_active=True,
                    is_superuser=True,
                )
                session.add(user)
                await session.commit()
                typer.echo("Superuser created successfully!")
            except IntegrityError:
                typer.echo("User already exists")
            # Break after the first session is used
            break

    import asyncio
    asyncio.run(_create_superuser())


if __name__ == "__main__":
    app_cli()
