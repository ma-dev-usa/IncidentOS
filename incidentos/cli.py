import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from incidentos.classifier import classify_replay
from incidentos.replay import load_replay, run_replay
from incidentos.report import generate_markdown_report
from incidentos.risk import score_release_risk, should_fail

console = Console()


def cmd_replay(args: argparse.Namespace) -> None:
    payload = run_replay(args.url, args.traffic, args.out)
    summary = payload["summary"]

    table = Table(title="IncidentOS Replay Summary")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Total requests", str(summary["total_requests"]))
    table.add_row("Failed requests", str(summary["failed_requests"]))
    table.add_row("Success rate", str(summary["success_rate"]))
    table.add_row("Output", args.out)

    console.print(table)


def cmd_classify(args: argparse.Namespace) -> None:
    payload = load_replay(args.input)
    classification = classify_replay(payload)

    console.print(json.dumps(classification.to_dict(), indent=2))


def cmd_report(args: argparse.Namespace) -> None:
    payload = load_replay(args.input)
    classification = classify_replay(payload)
    output = generate_markdown_report(classification, payload, args.out)

    console.print(f"Generated incident report: {output}")


def cmd_risk(args: argparse.Namespace) -> None:
    payload = load_replay(args.input)
    classification = classify_replay(payload)
    risk = score_release_risk(classification)

    console.print(json.dumps(risk, indent=2))

    if args.fail_on and should_fail(risk["risk"], args.fail_on):
        console.print(f"Release gate failed: risk {risk['risk']} >= {args.fail_on}")
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="incidentos")
    subparsers = parser.add_subparsers(dest="command", required=True)

    replay = subparsers.add_parser("replay")
    replay.add_argument("--url", required=True)
    replay.add_argument("--traffic", required=True)
    replay.add_argument("--out", default="reports/generated/latest_replay.json")
    replay.set_defaults(func=cmd_replay)

    classify = subparsers.add_parser("classify")
    classify.add_argument("--input", default="reports/generated/latest_replay.json")
    classify.set_defaults(func=cmd_classify)

    report = subparsers.add_parser("report")
    report.add_argument("--input", default="reports/generated/latest_replay.json")
    report.add_argument("--out", default="reports/generated/incident_report.md")
    report.set_defaults(func=cmd_report)

    risk = subparsers.add_parser("risk")
    risk.add_argument("--input", default="reports/generated/latest_replay.json")
    risk.add_argument("--fail-on", choices=["LOW", "MEDIUM", "HIGH"])
    risk.set_defaults(func=cmd_risk)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    Path("reports/generated").mkdir(parents=True, exist_ok=True)

    args.func(args)


if __name__ == "__main__":
    main()
