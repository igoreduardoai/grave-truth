from pathlib import Path

from grave_truth.skeleton import DocumentAgent, GroundedAnswer

FIXTURE = Path(__file__).resolve().parents[3] / "fixtures" / "sample_lease.txt"


def load_agent(path: Path | None = None) -> DocumentAgent:
    agent = DocumentAgent()
    agent.ingest("sample-lease", (path or FIXTURE).read_text(encoding="utf-8"))
    return agent


def check_clause(question: str, agent: DocumentAgent | None = None) -> GroundedAnswer:
    return (agent or load_agent()).answer(question)
