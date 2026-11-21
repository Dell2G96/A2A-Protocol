
from datetime import datetime, timezone

TASKS: dict[str, dict] = {}

def now() -> str:
  return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def create(task_id : str, context_id: str, message : dict) -> dict:
  task={
      "id" : task_id,
      "contextId": context_id,
      "status":{"state" : "TASK_STATE_SUBMITTED", "timestamp": now()},
      "artifacts": [],
      "history" : [message],
  }
  TASKS[task_id] = task
  return task

def set_state(task_id : str, state: str)->dict:
  task = TASKS[task_id]
  task["status"] = {"state": state, "timestamp": now()}
  return task

def add_artifact(task_id : str, artifact: dict) -> dict:
  TASKS[task_id]["artifacts"].append(artifact)
  return TASKS[task_id]