import argparse
import json
import sys

from incidentos.classifier import classify_replay, load_classification, save_classification
from incidentos.replay import load_replay, run_replay
from incidentos.report import generate_markdown_report
from incidentos.risk import score_release_risk, should_fail


def main() -> None:
    parser = argparse.ArgumentParser(prog="incidentos")
    subparsers = parser.add_subparsers(dest="command")

    replay_parser = subparsers.add_parser("replay")
    replay_parser.add_argument("--url", required=True)
    replay_parser.add_argument("--traffic", required=True)
    replay_parser.add_argument("--output", default="reports/generated/latest_replay.json")

    classify_parser = subparsers.add_parser("classify")
    classify_parser.add_argument("--replay", default="reports/generated/latest_replay.json")
    classify_parser.add_argument("--output", default="reports/generated/latest_classification.json")

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("--replay", default="reports/generated/latest_replay.json")
    report_parser.add_argument("--classification", default="reports/generated/latest_classification.json")
    report_parser.add_argument("--output", default="reports/generated/incident_report.md")

    risk_parser = subparsers.add_parser("risk")
    risk_parser.add_argument("--classification", default="reports/generated/latest_classification.json")
    risk_parser.add_argument("--fail-on", choices=["LOW", "MEDIUM", "HIGH"], default=None)

    flow_parser = subparsers.add_parser("flow")
    flow_parser.add_argument("--url", required=True)
    flow_parser.add_argument("--traffic", required=True)

    args = parser.parse_args()

    if args.command == "replay":
        payload = run_replay(args.url, args.traffic, args.output)
        print(json.dumps(payload["summary"], indent=2))
        print(f"Replay written to {args.output}")
        return

    if args.command == "classify":
        replay_payload = load_replay(args.replay)
        classification = classify_replay(replay_payload)
        output = save_classification(classification, args.output)
        print(json.dumps(classification.to_dict(), indent=2))
        print(f"Classification written to {output}")
        return

    if args.command == "report":
        replay_payload = load_replay(args.replay)
        classification = load_classification(args.classification)
        output = generate_markdown_report(classification, replay_payload, args.output)
        print(f"Incident report written to {output}")
        return

    if args.command == "risk":
        classification = load_classification(args.classification)
        risk = score_release_risk(classification)
        print(json.dumps(risk, indent=2))

        if args.fail_on and should_fail(risk["risk"], args.fail_on):
            sys.exit(1)

        return

    if args.command == "flow":
        replay_payload = run_replay(args.url, args.traffic)
        classification = classify_replay(replay_payload)
        save_classification(classification)
        report_path = generate_markdown_report(classification, replay_payload)
        risk = score_release_risk(classification)

        print(json.dumps(replay_payload["summary"], indent=2))
        print(json.dumps(classification.to_dict(), indent=2))
        print(json.dumps(risk, indent=2))
        print(f"Incident report written to {report_path}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
