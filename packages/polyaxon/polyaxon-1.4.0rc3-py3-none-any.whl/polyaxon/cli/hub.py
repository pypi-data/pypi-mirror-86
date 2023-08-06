#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import yaml

import click

from urllib3.exceptions import HTTPError

from polyaxon.cli.utils import get_entity_details
from polyaxon.env_vars.getters.owner_entity import resolve_entity_info
from polyaxon.env_vars.getters.user import get_local_owner
from polyaxon_sdk import V1ComponentHub
from polyaxon_sdk.rest import ApiException

from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.polyaxonfile import get_specification
from polyaxon.cli.dashboard import get_dashboard_url
from polyaxon.cli.errors import handle_cli_error
from polyaxon.cli.options import OPTIONS_OWNER, OPTIONS_HUB
from polyaxon.client import HubClient
from polyaxon.utils.formatting import (
    Printer,
    dict_tabulate,
    dict_to_tabulate,
    get_meta_response,
    list_dicts_to_tabulate,
)
from polyaxon.utils.validation import validate_tags


def get_specification_details(polyaxonfile, specification):
    if specification.inputs:
        Printer.print_header("Component inputs:")
        objects = list_dicts_to_tabulate([i.to_dict() for i in specification.inputs])
        dict_tabulate(objects, is_list_dict=True)

    if specification.outputs:
        Printer.print_header("Component outputs:")
        objects = list_dicts_to_tabulate([o.to_dict() for o in specification.outputs])
        dict_tabulate(objects, is_list_dict=True)

    Printer.print_header("Content:")
    click.echo(polyaxonfile)


def get_component_details(response, polyaxonfile, specification):
    response = dict_to_tabulate(
        response.to_dict(), humanize_values=True, exclude_attrs=["content"]
    )

    Printer.print_header("Component info:")
    dict_tabulate(response)

    get_specification_details(polyaxonfile, specification)


@click.group()
def hub():
    """Commands for component hub."""


@hub.command()
@click.option(
    "--name", type=str, help="The component hub name, e.g. 'kaniko' or 'acme/kaniko'."
)
@click.option("--description", type=str, help="Description of the component.")
@click.option("--tags", type=str, help="Tags of the component, comma separated values.")
@click.option(
    "--public", is_flag=True, help="Set the visibility of the component to public."
)
def create(name, description, tags, public):
    """Create a new component.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon hub create --name=kaniko --description="Tool to build container images"

    \b
    $ polyaxon hub create --name=owner/name --description="Component Description"
    """
    if not name:
        Printer.print_error(
            "Please provide a name to create a component hub.",
            command_help="ub create",
            sys_exit=True,
        )
    owner, hub_name = resolve_entity_info(
        name, is_cli=True, entity_name="component hub"
    )

    tags = validate_tags(tags)

    if not owner:
        Printer.print_error(
            "Please provide a valid owner with --name=owner/hub-name. "
        )
        sys.exit(1)

    try:
        hub_config = V1ComponentHub(
            name=hub_name, description=description, tags=tags, is_public=public
        )
        polyaxon_client = HubClient(owner=owner)
        _hub = polyaxon_client.create(hub_config)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not create component hub `{}`.".format(hub_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Component hub `{}` was created successfully.".format(_hub.name)
    )
    click.echo(
        "You can view this component hub on Polyaxon UI: {}".format(
            get_dashboard_url(subpath="{}/hub/{}".format(owner, _hub.name))
        )
    )


@hub.command()
@click.option(*OPTIONS_OWNER["args"], **OPTIONS_OWNER["kwargs"])
@click.option(
    "--query", "-q", type=str, help="To filter the component hub based on this query spec."
)
@click.option(
    "--sort", "-s", type=str, help="To order the component hub based on the sort spec."
)
@click.option("--limit", type=int, help="To limit the list of component hub.")
@click.option("--offset", type=int, help="To offset the list of component hub.")
def ls(owner, query, sort, limit, offset):
    """List component hub by owner.

    Uses /docs/core/cli/#caching
    """
    owner = owner or get_local_owner(is_cli=True)
    if not owner:
        Printer.print_error(
            "Please provide a valid owner --owner. "
            "`polyaxon login --help`"
        )
        sys.exit(1)

    try:
        polyaxon_client = HubClient(owner=owner)
        response = polyaxon_client.list(
            limit=limit, offset=offset, query=query, sort=sort
        )
    except (ApiException, HTTPError) as e:
        handle_cli_error(e, message="Could not get list of components.")
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header("Components for owner {}".format(owner))
        Printer.print_header("Navigation:")
        dict_tabulate(meta)
    else:
        Printer.print_header("No component hub found for owner {}".format(owner))

    objects = list_dicts_to_tabulate(
        [o.to_dict() for o in response.results],
        humanize_values=True,
        exclude_attrs=[
            "uuid",
            "readme",
            "description",
            "owner",
            "role",
            "settings",
        ],
    )
    if objects:
        Printer.print_header("Components:")
        dict_tabulate(objects, is_list_dict=True)


@hub.command()
@click.option(*OPTIONS_HUB["args"], "_hub", **OPTIONS_HUB["kwargs"])
def get(_hub):
    """Get info for a component hub by name, or owner/hub_name.

    Uses /docs/core/cli/#caching

    Examples:

    To get a default component hub:

    \b
    $ polyaxon hub get -h tensorboard

    To get by specific owner/name

    \b
    $ polyaxon hub get -p owner/my-component
    """
    owner, hub_name = resolve_entity_info(_hub, is_cli=True, entity_name="component hub")

    try:
        polyaxon_client = HubClient(owner=owner, hub=hub_name)
        polyaxon_client.refresh_data()
        get_entity_details(polyaxon_client.hub_data, "Component hub")
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not get component hub `{}`.".format(hub_name), sys_exit=True
        )


@hub.command()
@click.option(*OPTIONS_HUB["args"], "_hub", **OPTIONS_HUB["kwargs"])
def delete(_hub):
    """Delete component hub.

    Uses /docs/core/cli/#caching
    """
    owner, hub_name = resolve_entity_info(_hub, is_cli=True, entity_name="component hub")

    if not click.confirm(
        "Are sure you want to delete component hub `{}/{}`".format(owner, hub_name)
    ):
        click.echo("Existing without deleting component hub.")
        sys.exit(1)

    try:
        polyaxon_client = HubClient(owner=owner, hub=hub_name)
        polyaxon_client.delete()
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not delete component hub `{}/{}`.".format(owner, hub_name)
        )
        sys.exit(1)

    Printer.print_success(
        "Component hub `{}/{}` was delete successfully".format(owner, hub_name)
    )


@hub.command()
@click.option(*OPTIONS_HUB["args"], "_hub", **OPTIONS_HUB["kwargs"])
@click.option(
    "--name", type=str, help="Name of the component hub, must be unique for the same user."
)
@click.option("--description", type=str, help="Description of the component hub.")
@click.option(
    "--private", type=bool, help="Set the visibility of the component hub to private/public."
)
def update(_hub, name, description, private):
    """Update component hub.

    Uses /docs/core/cli/#caching

    Example:

    \b
    $ polyaxon hub update foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon hub update mike1/foobar --description="Image Classification with DL using TensorFlow"

    \b
    $ polyaxon hub update --tags="foo, bar"
    """
    owner, hub_name = resolve_entity_info(_hub, is_cli=True, entity_name="component hub")

    update_dict = {}
    if name:
        update_dict["name"] = name

    if description:
        update_dict["description"] = description

    if private is not None:
        update_dict["is_public"] = not private

    if not update_dict:
        Printer.print_warning("No argument was provided to update the component hub.")
        sys.exit(1)

    try:
        polyaxon_client = HubClient(owner=owner)
        response = polyaxon_client.update(update_dict)
    except (ApiException, HTTPError) as e:
        handle_cli_error(
            e, message="Could not update component hub `{}`.".format(hub_name)
        )
        sys.exit(1)

    Printer.print_success("Project updated.")
    get_entity_details(response, "Component hub")


@hub.command()
@click.option(*OPTIONS_HUB["args"], "_hub", **OPTIONS_HUB["kwargs"])
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Automatic yes to prompts. "
    'Assume "yes" as answer to all prompts and run non-interactively.',
)
@click.option(
    "--url",
    is_flag=True,
    default=False,
    help="Print the url of the dashboard for this component hub.",
)
def dashboard(_hub, yes, url):
    """Open this operation's dashboard details in browser."""
    owner, hub_name = resolve_entity_info(_hub, is_cli=True, entity_name="component hub")

    hub_url = get_dashboard_url(subpath="{}/{}".format(owner, hub_name))
    if url:
        Printer.print_header("The dashboard is available at: {}".format(hub_url))
        sys.exit(0)
    if not yes:
        click.confirm(
            "Dashboard page will now open in your browser. Continue?",
            abort=True,
            default=True,
        )
    click.launch(hub_url)


@hub.command()
@click.option("--name", type=str, help="The component name.")
@click.option(
    "--save",
    is_flag=True,
    default=False,
    help="Save the content to a local polyaxonfile.",
)
@click.option(
    "--filename",
    type=str,
    help="The filename to use for saving the polyaxonfile, default to `polyaxonfile.yaml`.",
)
def get_version(name, save, filename):
    """Get a component version info by component_name:version, or owner/component_name:version.

    Uses /docs/core/cli/#caching

    Examples:

    To get a component by name

    \b
    $ polyaxon hub get component_name

    To get a component by owner/name

    \b
    $ polyaxon hub get owner/component_name
    """
    if not name:
        Printer.print_error(
            "Please provide a valid component name!", command_help="hub get"
        )
        sys.exit(0)
    try:
        polyaxonfile = ConfigSpec.get_from(name, "hub").read()
    except Exception as e:
        handle_cli_error(e, message="Could not get component `{}`.".format(name))
        sys.exit(1)
    specification = get_specification(data=polyaxonfile)
    polyaxonfile = yaml.dump(polyaxonfile)
    get_specification_details(polyaxonfile=polyaxonfile, specification=specification)
    if save:
        filename = filename or "polyaxonfile.yaml"
        with open(filename, "w") as env_file:
            env_file.write(polyaxonfile)
