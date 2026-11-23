#!/usr/bin/env python3
"""Check the public skill tree, Git index, or reachable Git history.

Uses only the Python standard library. Findings contain locations and rule
names, never the matched values. This is a heuristic check plus an exact
publication manifest; manual review is still required.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = frozenset({
    ".gitignore",
    "README.md",
    "SKILL.md",
    "references/browser-cdp.md",
    "references/verification.md",
    "references/official-sources.md",
    "assets/change-request.example.json",
    "assets/result.example.json",
    "scripts/check_public.py",
})
MAX_FILE_BYTES = 256 * 1024
EMAIL = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
EXAMPLE_DOMAINS = {"example.com", "example.net", "example.org", "example.invalid"}
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
DOCUMENTATION_NETWORKS = tuple(ipaddress.ip_network(value) for value in (
    "192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24",
))
PATTERNS = (
    ("personal_home_path", re.compile(r"/(?:Users|home)/[^\s/<>]+/")),
    ("windows_home_path", re.compile(r"[A-Za-z]:\\Users\\[^\\\s<>]+\\")),
    ("private_key_material", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("github_token", re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("google_api_key", re.compile(r"AIza[A-Za-z0-9_-]{30,}")),
    ("jwt_token", re.compile(r"eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("totp_provisioning_uri", re.compile(r"\botpauth://(?:totp|hotp)/[^\s<>]+", re.I)),
    ("phone_number", re.compile(r"(?<![\w])(?:\+\d[\d ()-]{8,}\d|1[3-9]\d{9})(?![\w])")),
    ("credentialed_url", re.compile(r"https?://[^\s/@<>:]+:[^\s/@<>]+@", re.I)),
    ("secret_assignment", re.compile(
        r'''["']?(?:password|passwd|totp_seed|api_key|access_token|refresh_token|client_secret)["']?\s*[:=]\s*["'](?!PRIVATE_|<|\{|\s*['"])[^"'\n]{6,}["']''',
        re.I,
    )),
    ("seed_like_string", re.compile(r"(?<![A-Z0-9_])[A-Z2-7]{32,}(?![A-Z0-9_])")),
)
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")


def git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Git command {args[0]} failed (exit {result.returncode}); check repository state.")
    return result.stdout


def scan_text(label: str, text: str, findings: list[str], *, metadata: bool = False) -> None:
    for number, line in enumerate(text.splitlines(), 1):
        for rule, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(f"{label}:{number}: {rule}")
        for match in EMAIL.finditer(line):
            domain = match.group(1).lower()
            if domain not in EXAMPLE_DOMAINS and not (metadata and domain == "users.noreply.github.com"):
                findings.append(f"{label}:{number}: non_example_email")
        for match in IPV4.finditer(line):
            try:
                address = ipaddress.ip_address(match.group())
            except ValueError:
                continue
            if not address.is_loopback and not any(address in network for network in DOCUMENTATION_NETWORKS):
                findings.append(f"{label}:{number}: non_example_ipv4")


def check_snapshot(label: str, files: dict[str, bytes], findings: list[str]) -> None:
    for name in sorted(ALLOWED - files.keys()):
        findings.append(f"{label}: missing manifest entry {name}")
    for name, data in sorted(files.items()):
        where = f"{label}/{name}"
        if name not in ALLOWED:
            findings.append(f"{where}: outside publication manifest")
            continue
        if len(data) > MAX_FILE_BYTES:
            findings.append(f"{where}: exceeds file size limit")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(f"{where}: non-UTF-8 content")
            continue
        scan_text(where, text, findings)
        if name.endswith(".json"):
            try:
                value = json.loads(text)
                if not isinstance(value, dict) or value.get("example_only") is not True:
                    findings.append(f"{where}: expected an example-only JSON object")
            except json.JSONDecodeError:
                findings.append(f"{where}: invalid JSON")
        if name == "SKILL.md":
            parts = text.split("---", 2)
            if len(parts) != 3 or parts[0] != "" or not parts[1].startswith("\n"):
                findings.append(f"{where}: missing YAML frontmatter")
            else:
                if not re.search(r"(?m)^name: google-account-security-update$", parts[1]):
                    findings.append(f"{where}: unexpected skill name")
                if not re.search(r"(?m)^description: .+$", parts[1]):
                    findings.append(f"{where}: missing single-line description")
            if len(text.splitlines()) > 500:
                findings.append(f"{where}: entry exceeds 500 lines")
        if name.endswith(".md"):
            for match in LINK.finditer(text):
                target = match.group(1).strip().strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                path = unquote(parsed.path)
                normalized = os.path.normpath(str(PurePosixPath(name).parent / path)).replace(os.sep, "/")
                if normalized not in ALLOWED or normalized not in files:
                    findings.append(f"{where}: broken or non-public local link")


def working_files(findings: list[str]) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for directory, dirs, names in os.walk(ROOT, followlinks=False):
        current = Path(directory)
        for name in list(dirs):
            item = current / name
            if item.is_symlink():
                findings.append(f"worktree/{item.relative_to(ROOT)}: symlink directory")
                dirs.remove(name)
            elif current == ROOT and name == ".git":
                dirs.remove(name)
            elif not any(path.startswith(item.relative_to(ROOT).as_posix() + "/") for path in ALLOWED):
                findings.append(f"worktree/{item.relative_to(ROOT)}: unexpected directory")
                dirs.remove(name)
        for name in names:
            item = current / name
            relative = item.relative_to(ROOT).as_posix()
            if item.is_symlink():
                findings.append(f"worktree/{relative}: symlink file")
            elif relative not in ALLOWED:
                findings.append(f"worktree/{relative}: outside publication manifest")
            elif not item.is_file() or item.stat().st_size > MAX_FILE_BYTES:
                findings.append(f"worktree/{relative}: non-regular or oversized file")
            else:
                files[relative] = item.read_bytes()
    return files


def index_files(findings: list[str]) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for record in git("ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        header, raw_name = record.split(b"\t", 1)
        mode, _oid, stage = header.decode().split()
        name = raw_name.decode("utf-8")
        if mode not in {"100644", "100755"} or stage != "0":
            findings.append(f"index/{name}: unexpected mode or merge stage")
            continue
        if name not in ALLOWED:
            findings.append(f"index/{name}: outside publication manifest")
            continue
        if int(git("cat-file", "-s", f":{name}")) > MAX_FILE_BYTES:
            findings.append(f"index/{name}: oversized object")
            continue
        files[name] = git("show", f":{name}")
    return files


def history_snapshots(findings: list[str]) -> list[tuple[str, dict[str, bytes]]]:
    snapshots: list[tuple[str, dict[str, bytes]]] = []
    commits = git("rev-list", "--all").decode().splitlines()
    if not commits:
        findings.append("history: no reachable commits")
    for commit in commits:
        label = f"history/{commit[:12]}"
        metadata = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%B", commit).decode("utf-8")
        scan_text(f"{label}/metadata", metadata, findings, metadata=True)
        files: dict[str, bytes] = {}
        for record in git("ls-tree", "-r", "-z", commit).split(b"\0"):
            if not record:
                continue
            header, raw_name = record.split(b"\t", 1)
            mode, kind, oid = header.decode().split()
            name = raw_name.decode("utf-8")
            if mode not in {"100644", "100755"} or kind != "blob":
                findings.append(f"{label}/{name}: unexpected object type")
                continue
            if name not in ALLOWED:
                findings.append(f"{label}/{name}: outside publication manifest")
                continue
            if int(git("cat-file", "-s", oid)) > MAX_FILE_BYTES:
                findings.append(f"{label}/{name}: oversized object")
                continue
            files[name] = git("cat-file", "blob", oid)
        snapshots.append((label, files))
    return snapshots


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--staged", action="store_true", help="Check exactly the Git index")
    modes.add_argument("--history", action="store_true", help="Check reachable commit trees and metadata")
    args = parser.parse_args()
    findings: list[str] = []
    try:
        if args.history:
            snapshots = history_snapshots(findings)
        elif args.staged:
            snapshots = [("index", index_files(findings))]
        else:
            snapshots = [("worktree", working_files(findings))]
        for label, files in snapshots:
            check_snapshot(label, files, findings)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"CHECK ERROR: {type(exc).__name__}; inspect tool and repository state.", file=sys.stderr)
        return 2
    if findings:
        for finding in sorted(set(findings)):
            print(f"FAIL {finding}")
        print(f"FAILED: {len(set(findings))} finding(s); review before publishing.")
        return 1
    count = sum(len(files) for _, files in snapshots)
    print(f"PASS: {len(snapshots)} snapshot(s), {count} file version(s); manifest, structure, links and sensitive-pattern checks.")
    print("Manual review is still required; no account or network operations were performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
