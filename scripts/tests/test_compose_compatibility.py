"""Compose CLI integration checks; configuration only, no deployed resources changed."""
import json
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ComposeNamingCompatibilityTests(unittest.TestCase):
    def config(self, **variables):
        environment = os.environ.copy()
        for key in ("AEGLYSAI_PORT", "AEGISAI_PORT", "AEGLYSAI_COMPOSE_PROJECT", "COMPOSE_PROJECT_NAME"):
            environment.pop(key, None)
        environment.update(variables)
        result = subprocess.run(["docker", "compose", "--env-file", os.devnull,
                                 "-f", str(ROOT / "deployment/docker/compose.yaml"),
                                 "config", "--format", "json"], cwd=ROOT,
                                env=environment, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def port(self, **variables):
        return str(self.config(**variables)["services"]["api"]["ports"][0]["published"])

    def test_default_port_and_existing_resource_identity_are_preserved(self):
        config = self.config()
        self.assertEqual("aegisai-local", config["name"])
        self.assertEqual("5080", str(config["services"]["api"]["ports"][0]["published"]))

    def test_legacy_port_variable_remains_supported(self):
        self.assertEqual("5090", self.port(AEGISAI_PORT="5090"))

    def test_new_port_variable_takes_precedence(self):
        self.assertEqual("5091", self.port(AEGLYSAI_PORT="5091", AEGISAI_PORT="5090"))

    def test_empty_new_port_falls_back_to_legacy(self):
        self.assertEqual("5090", self.port(AEGLYSAI_PORT="", AEGISAI_PORT="5090"))

    def test_new_resource_identity_is_explicit_opt_in(self):
        self.assertEqual("aeglysai-local", self.config(AEGLYSAI_COMPOSE_PROJECT="aeglysai-local")["name"])


if __name__ == "__main__":
    unittest.main()
