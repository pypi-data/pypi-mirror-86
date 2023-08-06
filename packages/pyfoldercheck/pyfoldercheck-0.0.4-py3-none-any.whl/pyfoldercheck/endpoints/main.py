import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch

from pyfoldercheck.endpoints.group_default import register_group_default


def register_all_groups():
    # order of registration is important
    register_group_default()


@register_main()
def main():
    """
    A program to help you out with your mp3 library
    """
    pylogconf.core.setup()
    register_all_groups()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()
