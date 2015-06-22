"""
live environment
"""

from fabric.state import env
from fabric.decorators import task
from frojd_fabric.utils import get_stage_var


@task
def live:
    # Recipe
    from frojd_fabric.recipes import wordpress

    # Metadata
    env.stage = "live"

    # VC
    env.branch = None

    # SSH Config
    env.hosts = [get_stage_var("HOST")]
    env.user = get_stage_var("USER")
    env.password = get_stage_var("PASSWORD", "")
    env.key_filename = get_stage_var("KEY_FILENAME")
    env.forward_agent = False
