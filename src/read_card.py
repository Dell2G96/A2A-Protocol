from google.protobuf import json_format

from a2a import types as t

card = t.AgentCard(
  name = "expense-agent",
  description = "출장 경비를 정리하고 사내 규정 위반을 찾는다.",
  version = "1.0.0",
  default_input_modes=["text/plain"],
  default_output_modes=["text/plain"],
  capabilities=t.AgentCapabilities(streaming=False),
  skills=[
    t.AgentSkill(
      id = "settle_expense",
      name="경비정산",
      description="출장 번호를 받아 영수증과 환율을 수집한다",
      tags=["expense", "finance"],
    )
  ],
  supported_interfaces=[
    t.AgentInterface(
      url="https://agent.example.test/rpc",
      protocol_binding="JSONRPC",
      protocol_version="1.0",
    )
  ],
)

print(json_format.MessageToJson(card, indent=2, ensure_ascii=False))

 