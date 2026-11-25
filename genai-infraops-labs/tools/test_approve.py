import argparse
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import approve


def plan():
    return {
        "id": "REM-0001",
        "status": "APPROVED",
        "approved_by": "Rajesh",
        "pre_checks": [
            ["kubectl", "get", "service", "portal-web", "-n", "portal", "--context=lab"]
        ],
        "command": [
            "kubectl", "patch", "service", "portal-web", "-n", "portal",
            "--context=lab", "--type=merge", "-p",
            '{"spec":{"selector":{"app":"portal-web"}}}',
        ],
        "rollback": [
            "kubectl", "patch", "service", "portal-web", "-n", "portal",
            "--context=lab", "--type=merge", "-p",
            '{"spec":{"selector":{"app":"portal-web-v2"}}}',
        ],
        "verification": [
            {
                "command": [
                    "kubectl", "get", "endpoints", "portal-web", "-n", "portal",
                    "--context=lab",
                ],
                "expect": "At least one endpoint",
            }
        ],
    }


class ApproveExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.approvals = Path(self.temp_dir.name) / "approvals"
        (self.approvals / "approved").mkdir(parents=True)
        self.audit_path = self.approvals / "audit.log"
        self.plan_path = self.approvals / "approved" / "REM-0001.json"
        self.plan_path.write_text(json.dumps(plan()))
        self.approvals_patch = patch.object(approve, "A", str(self.approvals))
        self.audit_patch = patch.object(approve, "AUDIT", str(self.audit_path))
        self.approvals_patch.start()
        self.audit_patch.start()
        self.addCleanup(self.approvals_patch.stop)
        self.addCleanup(self.audit_patch.stop)

    def tearDown(self):
        self.temp_dir.cleanup()

    def execute_args(self):
        return argparse.Namespace(id="REM-0001", dry_run=False)

    def test_kubectl_mutation_requires_explicit_context(self):
        command = plan()["command"]
        command.remove("--context=lab")

        problems = approve.policy_check(command)

        self.assertIn(
            "kubectl context must be explicit with exactly one --context",
            problems,
        )

    def test_failed_precheck_aborts_before_mutation(self):
        with (
            patch.object(approve, "run", return_value=(1, "context unavailable")) as run,
            patch("builtins.input", side_effect=AssertionError("confirmation must not be requested")),
            redirect_stdout(StringIO()),
        ):
            with self.assertRaises(SystemExit) as raised:
                approve.cmd_execute(self.execute_args())

        self.assertIn("execution aborted", str(raised.exception))
        self.assertEqual(run.call_count, 1)
        record = json.loads(self.audit_path.read_text().splitlines()[0])
        self.assertEqual(record["event"], "PRECHECK_FAILED")
        failed_path = self.approvals / "failed" / "REM-0001.json"
        failed_plan = json.loads(failed_path.read_text())
        self.assertEqual(failed_plan["status"], "PRECHECK_FAILED")
        self.assertFalse(self.plan_path.exists())

    def test_failed_verification_is_recorded_as_failed_not_executed(self):
        with (
            patch.object(
                approve,
                "run",
                side_effect=[
                    (0, "selector is portal-web"),
                    (0, "patched"),
                    (1, "no endpoints"),
                ],
            ),
            patch("builtins.input", return_value="y"),
            redirect_stdout(StringIO()),
        ):
            with self.assertRaises(SystemExit):
                approve.cmd_execute(self.execute_args())

        failed_path = self.approvals / "failed" / "REM-0001.json"
        failed_plan = json.loads(failed_path.read_text())
        self.assertEqual(failed_plan["status"], "EXECUTION_FAILED")
        self.assertFalse((self.approvals / "executed" / "REM-0001.json").exists())
        record = json.loads(self.audit_path.read_text().splitlines()[0])
        self.assertEqual(record["event"], "EXECUTION_FAILED")
        self.assertEqual(record["verification"][0]["rc"], 1)


if __name__ == "__main__":
    unittest.main()
