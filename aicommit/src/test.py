import subprocess
import pytest

def test_check_for_merge_conflicts():
    # Simulate a conflict by having an intentionally conflicting change
    subprocess.run(["git", "fetch"], check=True)
    result = subprocess.run(
        ["git", "diff", "main", "--staged"],
        capture_output=True, text=True, check=True
    )
    assert "conflict" in result.stdout, "Expected a conflict but did not find one"
