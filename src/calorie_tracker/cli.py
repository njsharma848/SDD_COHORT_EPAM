"""Command-line interface for the Calorie and Nutrition Tracker.

Parses arguments, calls the service layer, and renders results or
clear, non-zero-exit error messages. No business logic lives here
(constitution P-6 — single responsibility per module).
"""

from __future__ import annotations

import argparse
import sys

from . import repository, service
from .validation import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calorie-tracker",
        description="A single-user command-line calorie and nutrition tracker.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_meal = subparsers.add_parser("add-meal", help="Record a meal")
    add_meal.add_argument("--name", required=True)
    add_meal.add_argument("--calories", required=True)
    add_meal.add_argument("--protein", required=True)
    add_meal.add_argument("--date", required=False, default=None,
                           help="YYYY-MM-DD; defaults to today")

    delete_meal = subparsers.add_parser("delete-meal", help="Delete a meal by ID")
    delete_meal.add_argument("--id", required=True, type=int)

    set_targets = subparsers.add_parser(
        "set-targets", help="Set or change today's daily calorie and protein targets"
    )
    set_targets.add_argument("--calories", required=True)
    set_targets.add_argument("--protein", required=True)

    return parser


def _print_error(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)


def run(argv: list[str] | None = None, db_path=None) -> int:
    """Parse argv, dispatch to the service layer, and return an exit
    code (0 = success, non-zero = a reported error, never a raw
    traceback). `db_path` lets tests use an isolated database.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    conn = repository.connect(db_path)
    try:
        if args.command == "add-meal":
            try:
                meal = service.create_meal(
                    conn, args.name, args.calories, args.protein, args.date
                )
            except (ValidationError, service.DomainError) as exc:
                _print_error(str(exc))
                return 1
            print(
                f"Recorded meal {meal.id}: {meal.name} "
                f"({meal.calories_tenths / 10:.1f} kcal, "
                f"{meal.protein_tenths / 10:.1f} g protein) on {meal.meal_date}"
            )
            return 0

        if args.command == "delete-meal":
            try:
                service.delete_meal(conn, args.id)
            except (ValidationError, service.DomainError) as exc:
                _print_error(str(exc))
                return 1
            print(f"Deleted meal {args.id}")
            return 0

        if args.command == "set-targets":
            try:
                target = service.set_targets(conn, args.calories, args.protein)
            except (ValidationError, service.DomainError) as exc:
                _print_error(str(exc))
                return 1
            print(
                f"Targets set effective {target.effective_date}: "
                f"{target.calories_tenths / 10:.1f} kcal, "
                f"{target.protein_tenths / 10:.1f} g protein"
            )
            return 0

        _print_error(f"Unknown command: {args.command}")
        return 1

        
    finally:
        conn.close()