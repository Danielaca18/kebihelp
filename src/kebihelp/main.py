#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
import sys
import argparse
from kebihelp.parsers import Parsers
from kebihelp.config import Config
from kebihelp.gui import MainWindow

VERSION = "0.1.2"


def main():
    parser = argparse.ArgumentParser(
        description="Kebihelp - The universal keybinder helper"
    )

    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        action="store_true",
        help="Show the current version",
    )
    subparsers = parser.add_subparsers(dest="command", help="Main action to perform")

    parser_import = subparsers.add_parser("import", help="Import new keybindings")
    parser_import.add_argument("-t", dest="import_tab", help="Import to this tab")
    parser_import.add_argument("-s", dest="import_source", help="Source to import")

    parser_keys = subparsers.add_parser("list", help="List the existing keybindings")
    parser_keys.add_argument("-t", "--tab", dest="list_tab", help="Select the tab")

    parser_tabs = subparsers.add_parser("tabs", help="List the tabs")

    parser_clear = subparsers.add_parser("clear", help="Clear/Remove existing bindings")

    parser_watch = subparsers.add_parser("watch", help="Manage and update import paths")
    parser_watch.add_argument(
        "-a", dest="watch_add", help="Add a directory to the watch list"
    )
    parser_watch.add_argument(
        "-l",
        "--list",
        action="store_true",
        dest="watch_list",
        help="List all watched paths",
    )
    parser_watch.add_argument(
        "-u",
        "--update",
        action="store_true",
        dest="watch_update",
        help="Import all watched paths",
    )

    parser_show = subparsers.add_parser("show", help="Show the keybindings")
    parser_show.add_argument("-t", "--tab", dest="show_tab", help="Show only this tab")
    parser_show.add_argument(
        "-a",
        "--auto",
        action="store_true",
        dest="show_auto",
        help="Show the right tab depending of focused window",
    )

    args = parser.parse_args()

    if args.version:
        print("Kebihelp - v" + VERSION)
        exit(0)

    if not args.command:
        parser.print_usage()
        exit(0)

    if args.command == "import":
        parsers = Parsers(args.import_tab, args.import_source)
        parsers.import_bindings()

    if args.command == "list":
        config = Config()
        config.output_table(args.list_tab)

    if args.command == "clear":
        config = Config()
        config.config["Keybindings"] = {}
        config.save()

    if args.command == "watch":
        config = Config()
        if "Sources" not in config.config:
            config.config["Sources"] = {}

        if args.watch_add:
            config.config["Sources"][args.watch_add] = {}
            config.save()
            print(f"Path added to sources: {args.watch_add}")

        if args.watch_list:
            src_list = config.config["Sources"].keys()
            if not src_list:
                print("No paths are currently being watched.")
            else:
                print("Currently watched paths:")
                for path in src_list:
                    print(f" - {path}")

        if args.watch_update:
            src_list = config.config["Sources"].keys()
            for source in src_list:
                parsers = Parsers(None, source)
                parsers.import_bindings()

    if args.command == "show":
        app = QApplication(sys.argv)
        window = MainWindow(args.show_tab, args.show_auto)
        window.show()
        app.exec()


if __name__ == "__main__":
    main()
