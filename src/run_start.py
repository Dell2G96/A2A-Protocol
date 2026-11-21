import os
import sys

from langgraph.checkpoint.postgres import PostgresSaver

from graph import build_graph

trip = sys.argv[1] if len(sys.argv) > 1 else "T-2026-03"
thread = sys.argv[2] if len(sys.argv) > 2 else "trip-approve"

with PostgresSaver.from_conn_string(os.environ["POSTGRES_URL"]) as saver:
  saver.setup()
  graph = build_graph(checkpointer=saver)
  config = {"configurable": {"thread_id": thread}}

  if graph.get_state(config).values:
    raise SystemExit(f"{thread}는 이미 사용한 thread_id입니다. 다른 이름을 주세요.")

  graph.invoke({"trip_id": trip, "messages": [], "log": [], "steps": 0}, config)

  snapshot = graph.get_state(config)
  if snapshot.next:  # interrupt()에서 멈춘 상태
    question = snapshot.tasks[0].interrupts[0].value
    print("멈췄습니다. 물어보는 내용:")
    for key, value in question.items():
      print(f"  {key}: {value}")
    print()
  print("다음에 갈 노드:", snapshot.next)
