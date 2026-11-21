from langgraph.checkpoint.memory import MemorySaver

from graph import build_graph

saver = MemorySaver() # 메모리의 값을 담는다.
graph = build_graph(checkpointer=saver)
config = {"configurable": {"thread_id": "trip-3"}}

result = graph.invoke({"trip_id": "T-2026-03", "messages":[], "log": [], "steps":0}, config)
print("1회차 합계:", result["total"])

snapshot = graph.get_state(config)
print("저장된 합계:", snapshot.values["total"])
print("저장된 메세지 수:", len(snapshot.values["messages"]))
print("다음에 갈 노드:", snapshot.next)
