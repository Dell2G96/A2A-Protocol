import re
import uuid
import store

from fastapi import FastAPI, Request

import rpc
from card import AGENT_CARD

app = FastAPI()
TRIP_PATTERN = re.compile(r"T-\d{4}-\d{2}") # T-2026-04


@app.get("/.well-known/agent-card.json")
def agent_card():
  return AGENT_CARD

def read_text(message: dict) -> str:
  return "".join(part["text"] for part in message.get("parts", []) if "text" in part)

class InvalidParams(Exception):
  pass


def handle_send_message(params: dict) -> dict:
  message = params.get("message") 
  if not message:
    raise InvalidParams("message가 없습니다.")
  if not message.get("messageId"):
    raise InvalidParams("messageID 가 없습니다.")
  if message.get("role") != "ROLE_USER":
    raise InvalidParams(
        f"role은 ROLE_USER여야 합니다. 받은 값: {message.get('role')}"
    )
  text = read_text(message)
  found = TRIP_PATTERN.search(text)
  if not found:
    raise InvalidParams(f"출장 번호를 찾지 못했습니다: {text!r}")

  task_id = str(uuid.uuid4())
  context_id = message.get("contextId") or str(uuid.uuid4())
  task = store.create(task_id, context_id, message)

  config = params.get("configurable") or {}
  if config.get("returnImmediately"):
    return task
  
  store.set_state(task_id, "TASK_STATE_WORKING")
  result = {
      "trip_id" : found.group(),
      "total":50000,
      "violations" : [],
      "receipts":2,
  }
  store.add_artifact(task_id, {
      "artifactId": str(uuid.uuid4()),
      "name" : "정산 요약",
      "description" : "사람이 읽는 요약",
      "parts":[{
          "text": (
              f"출장 {result['trip_id']} 원화 합계 {result['total']}원, "
              f"규정 위반 {len(result['violations'])}건"
          )
      }],
  })
  store.add_artifact(task_id,{
      "artifactId":str(uuid.uuid4()),
      "name": "정산 내역",
      "description" : "프로그램이 읽는 데이터",
      "parts":[{"data": result, "mediaType": "application/json"}],
  })
  return store.set_state(task_id, "TASK_STATE_COMPLETED")


HANDLES = {"SendMessage": handle_send_message}

@app.post("/")
async def jsonrpc(request: Request):
  try:
    body = await request.json()
  except Exception:
    return rpc.err(None, rpc.PARSE_ERROR, "Parse error")

  if body.get("jsonrpc") != "2.0" or "method" not in body:
    return rpc.err(body.get("id"), rpc.INVALID_REQUEST, "Invalid Request")

  handler = HANDLES.get(body["method"])
  if handler is None:
    return rpc.err(
        body.get("id"),
        rpc.METHOD_NOT_FOUND,
        "Method not found",
        "UnsupportedOperationError",
        f"{body['method']}은 지원하지 않습니다.",
    )

  try:
      result = handler(body.get("params")or {})
  except InvalidParams as error:
      return rpc.err(
        body.get("id"), rpc.INVALID_PARAMS, "Invalid params",
        "InvalidParamsError", str(error),
    )

  return rpc.ok(body.get("id"), result)