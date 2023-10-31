import os
import sys
import subprocess
import psycopg2
import click

import django
from django.core.management import call_command

import zelthy
from .utils import replace_placeholders_in_file


def test_db_conection(db_name, db_user, db_password, db_host, db_port):
    """
    Establishes a connection to a PostgreSQL database using the provided credentials.

    Args:
        db_name (str): The name of the database.
        db_user (str): The username for the database.
        db_password (str): The password for the database.
        db_host (str): The host address for the database.
        db_port (int): The port number for the database.

    Returns:
        bool: True if the connection is successfully established, False otherwise.
    """

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            host=db_host,
            password=db_password,
            port=db_port,
            connect_timeout=30,
        )
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_project_root(project_name, directory=None):
    """
    Returns the root directory of the specified project.

    Parameters:
        project_name (str): The name of the project.

    Returns:
        str: The root directory of the project.
    """
    current_dir = directory or os.getcwd()
    project_root = os.path.join(current_dir, project_name)
    return project_root


def create_project(
    project_name, directory, db_name, db_user, db_password, db_host, db_port
):
    """
    Create a new Django project with the given project name and directory.

    Args:
        project_name (str): The name of the Django project.
        directory (str): The directory where the project will be created. If not provided, the project will be created in the current directory.
        db_name (str): The name of the database.
        db_user (str): The username for the database.
        db_password (str): The password for the database.
        db_host (str): The host for the database.
        db_port (str): The port for the database.
    """
    command = f"django-admin startproject {project_name}"
    if directory:
        command = f"{command} {directory}"

    project_root = get_project_root(project_name, directory=directory)

    if os.path.exists(project_root):
        return False, f"Folder already exists: {project_root}"

    project_template_path = os.path.join(
        os.path.dirname(zelthy.cli.__file__), "project_template"
    )
    command = f"{command} --template {str(project_template_path)}"

    subprocess.run(command, shell=True, check=True)

    settings_file = os.path.join(project_root, project_name, "settings.py")
    replace_placeholders_in_file(
        settings_file,
        {
            "{db_name}": db_name,
            "{db_user}": db_user,
            "{db_password}": db_password,
            "{db_host}": db_host,
            "{db_port}": db_port,
        },
    )

    return True, "Project created successfully"

    # PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # sys.path.insert(


def create_public_tenant():
    from zelthy.apps.shared.tenancy.models import TenantModel, Domain

    # Creating public tenant
    if not TenantModel.objects.filter(schema_name="public").exists():
        public_tenant = TenantModel.objects.create(
            name="public",
            schema_name="public",
            description="Public Tenant",
            tenant_type="shared",
        )

        # Creating domain
        Domain.objects.create(tenant=public_tenant, domain="localhost", is_primary=True)


def create_platform_user(platform_username, platform_username_password):
    from zelthy.apps.shared.platformauth.models import PlatformUserModel

    # Creating default SuperAdmin User
    result = PlatformUserModel.create_user(
        name="Default Super Admin",
        email=platform_username,
        mobile="",
        password=platform_username_password,
        is_superadmin=True,
        require_verification=False,
    )

    return result


@click.command(name="start-project")
@click.argument("project_name")
@click.option("--directory", help="Project Directory")
@click.option("--db_name", prompt=True, help="DB Name")
@click.option("--db_user", prompt=True, help="DB User")
@click.option("--db_password", prompt=True, hide_input=True, help="DB Password")
@click.option("--db_host", prompt=True, help="DB Host", default="127.0.0.1")
@click.option("--db_port", prompt=True, help="DB Port", default="5432")
def start_project(
    project_name, directory, db_name, db_user, db_password, db_host, db_port
):
    """Create Project"""
    if directory:
        click.echo(f"Creating Project under: {directory}")

    db_connection_status = test_db_conection(
        db_name, db_user, db_password, db_host, db_port
    )
    click.echo(f"db_connection_status: {db_connection_status}")
    if not db_connection_status:
        raise click.ClickException("DB Connection Failed!")

    project_status, project_message = create_project(
        project_name, directory, db_name, db_user, db_password, db_host, db_port
    )

    if not project_status:
        raise click.ClickException(project_message)

    # Initializing the project
    project_root = get_project_root(project_name, directory=directory)
    sys.path.insert(0, project_root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")

    django.setup()

    # Migrating Schemas
    call_command("migrate_schemas", schema="public")

    # Creating Public Tenant
    create_public_tenant()

    # Prompting default platform user details
    click.echo("Please enter platform user details")
    platform_username = click.prompt("Email")
    platform_username_password = click.prompt(
        "Password", hide_input=True, confirmation_prompt=True
    )

    user_creation_result = create_platform_user(
        platform_username, platform_username_password
    )
    if not user_creation_result["success"]:
        click.echo("User Creation Failed!")

    click.echo(user_creation_result["message"])