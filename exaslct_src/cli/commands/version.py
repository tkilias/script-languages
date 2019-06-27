from typing import Tuple

from yaml import load, dump, Loader, Dumper

from exaslct_src.cli.cli import cli
from exaslct_src.cli.common import add_options
from exaslct_src.cli.options \
    import flavor_options


@cli.command()
@add_options(flavor_options)
def version(flavor_path: Tuple[str, ...], ):
    """
    This command collects the version information for exaslct, the script-client and for the given flavors.
    """
    with open("exaslct_src/VERSION") as f:
        exaslct_version = load(f, Loader=Loader)
    with open("src/VERSION") as f:
        udf_client_version = load(f, Loader=Loader)
    flavor_versions = {}
    for path in flavor_path:
        with open(path + "/VERSION") as f:
            flavor_versions[path] = load(f, Loader=Loader)
    versions = {"exaslct": exaslct_version,
                "udf_client": udf_client_version,
                "flavors": flavor_versions}
    # with open("src/VERSION","w") as f1:
    output = dump(versions, Dumper=Dumper)
    print(output)
