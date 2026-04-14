from __future__ import annotations

import argparse
from collections import Counter

from .demo import build_demo_terms, write_demo_artifacts
from .repository import load_repository
from .validation import validate_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sanskrit-etymology",
        description="Validate canonical Sanskrit data and build demo artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-data", help="Validate canonical YAML sources.")
    subparsers.add_parser("build-demo", help="Build demo artifacts from canonical data.")
    subparsers.add_parser("stats", help="Print dataset summary.")
    return parser


def cmd_validate_data() -> int:
    repo = load_repository()
    issues = validate_repository(repo)
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    print(
        f"Validated {len(repo.seed_terms)} seed terms, "
        f"{len(repo.analyses)} analyses, {len(repo.mappings)} mappings."
    )
    for issue in issues:
        print(f"{issue.severity.upper():7} {issue.location}: {issue.message}")

    if errors:
        print(f"Validation failed with {len(errors)} error(s).")
        return 1

    if warnings:
        print(f"Validation passed with {len(warnings)} warning(s).")
    else:
        print("Validation passed with no issues.")
    return 0


def cmd_build_demo() -> int:
    repo = load_repository()
    issues = validate_repository(repo)
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        for issue in errors:
            print(f"ERROR   {issue.location}: {issue.message}")
        print("Refusing to build demo artifacts until validation errors are resolved.")
        return 1

    demo_terms = build_demo_terms(repo)
    json_path, inline_path = write_demo_artifacts(demo_terms)
    mapped_terms = sum(1 for term in demo_terms if term.chinese_counterparts)
    print(
        f"Wrote {len(demo_terms)} demo terms to {json_path} and {inline_path}. "
        f"{mapped_terms} terms include Chinese mappings."
    )
    return 0


def cmd_stats() -> int:
    repo = load_repository()
    demo_terms = build_demo_terms(repo)
    bucket_counts = Counter(term.priority_bucket for term in demo_terms if term.priority_bucket)
    demo_only_terms = sum(1 for term in demo_terms if not term.priority_bucket)
    print(f"Seed terms: {len(repo.seed_terms)}")
    print(f"Analyses: {len(repo.analyses)}")
    print(f"Mappings: {len(repo.mappings)}")
    print(f"Demo terms: {len(demo_terms)}")
    print(f"Demo-only bundle terms: {demo_only_terms}")
    print(f"Priority buckets: {dict(sorted(bucket_counts.items()))}")
    print(f"Terms with Chinese mappings: {sum(1 for term in demo_terms if term.chinese_counterparts)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate-data":
        return cmd_validate_data()
    if args.command == "build-demo":
        return cmd_build_demo()
    if args.command == "stats":
        return cmd_stats()

    parser.error(f"unknown command: {args.command}")
    return 2
