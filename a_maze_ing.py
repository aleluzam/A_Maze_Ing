#!/usr/bin/env python3
"""Entry point for the A-Maze-ing application.

Parses a configuration file, constructs a :class:`MazeApplication` instance,
and runs it. The script expects exactly one command‑line argument: the path
to a configuration file (e.g. ``config.txt``). Errors are reported on standard
error and cause a non‑zero exit status.
"""

import sys

from maze_application import MazeApplication
from maze_application.config_parser import ConfigError, parse_config


def main() -> None:
    """Parse the configuration and launch the maze application.

    The function validates the number of command‑line arguments, reads the
    configuration using :func:`parse_config`,
    creates a :class:`MazeApplication`, and starts it. It catches configuration
    errors and unexpected exceptions, prints an explanatory message
    to ``stderr`` and exits with status ``1``.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        application = MazeApplication(config)
        application.run()

    except ConfigError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
