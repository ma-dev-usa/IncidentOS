import argparse

def main():
    parser = argparse.ArgumentParser(prog="incidentos")
    subparsers = parser.add_subparsers(dest="command")

    replay = subparsers.add_parser("replay")
    replay.add_argument("--url", required=True)
    replay.add_argument("--traffic", required=True)

    subparsers.add_parser("report")
    subparsers.add_parser("risk")

    args = parser.parse_args()

    if args.command == "replay":
        print(f"Replaying traffic from {args.traffic} against {args.url}")
    elif args.command == "report":
        print("Generating incident report")
    elif args.command == "risk":
        print("Release risk: LOW")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
