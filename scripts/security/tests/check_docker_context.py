"""Verify actual Docker ignore behavior using synthetic files and a scratch build."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
protected = ["patent-private/draft.md", "nested/private-research/model.cs",
             "attorney-private/note.md", "evidence-private/report.json",
             "confidential-local/example.txt", "a.confidential.docx", "a.patent-draft.md",
             "nested/.aws/credentials", "nested/.azure/token", "nested/.ssh/id_rsa",
             "nested/credentials.local.json", "nested/gitleaks-report.json",
             "nested/.env.local", "nested/key.pem", "nested/key.snk",
             "nested/secrets.json", "nested/appsettings.Local.json",
             "research/results/local-fixture/summary.json", "docs/aegisai/research/fixture.md"]
public = ["src/Public.cs", "docs/aegisai/specs/SPEC-PUBLIC.md", "research/experiments/public.json"]
with tempfile.TemporaryDirectory(prefix="aeglysai-context-test-") as temporary:
    private = Path(temporary)
    context, output = private / "context", private / "output"
    context.mkdir()
    (context / ".dockerignore").write_bytes((root / ".dockerignore").read_bytes())
    (context / "Dockerfile").write_text("FROM scratch\nCOPY . /context/\n")
    for name in protected + public:
        file = context / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("SYNTHETIC context canary\n")
    result = subprocess.run(["docker", "build", "--network=none", "--progress=quiet",
                             "--output", f"type=local,dest={output}", str(context)],
                            capture_output=True, timeout=120)
    if result.returncode:
        raise SystemExit("Docker context test failed; diagnostic output suppressed")
    assert all(not (output / "context" / name).exists() for name in protected), "Protected file reached builder"
    assert all((output / "context" / name).is_file() for name in public), "Public fixture missing"
    print(f"PASS: actual Docker context excludes {len(protected)} protected fixtures and retains {len(public)} public fixtures")
