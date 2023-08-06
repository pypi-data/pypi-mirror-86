import typer

cli = typer.Typer()


@cli.command()
def migrate():
    typer.echo("Running Migrations..")
    from alembic.config import Config
    import alembic.command

    config = Config('alembic.ini')
    config.attributes['configure_logger'] = False

    alembic.command.upgrade(config, 'head')


@cli.command()
def create_migration(message: str = typer.Option(..., prompt=True)):
    typer.echo("Creating migration..")
    from alembic.config import Config
    import alembic.command

    config = Config('alembic.ini')
    config.attributes['configure_logger'] = False

    alembic.command.revision(config, autogenerate=True, message=message)


if __name__ == '__main__':
    cli()
