import argparse
from terminal_app import initialize, capture_and_process, show_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Quiz assistant command line")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("capture", help="Capture screen and process once")
    sub.add_parser("config", help="Show current configuration")

    args = parser.parse_args()

    initialize()

    if args.command == "capture":
        capture_and_process()
    elif args.command == "config":
        show_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
