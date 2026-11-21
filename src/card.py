AGENT_CARD = {
"name" : "expense-agent",
"description": "출장경비를 정리하고 사내 규정 위반을 찾는다",
"version": "1.0.0",
"supportedInterfaces": [
    {
      "url" : "http://worker:8000",
      "protocolBinding": "JSONRPC",
      "protocolVersion": "1.0",
    }
],
"capabilities":{
  "streaming":False,
  "pushNotifications": False,
  "extendedAgentCard": False,
},
"defaultInputModes": ["text/plain"],
"defaultOutputModes" :["text/plain", "application/json"],
"skills": [
    {
      "id"  : "settle_expense",
      "name" : "경비 정산",
      "description" : (
        "출장 번호를 주면 영수증을 모아 외화를 원화로 환산하고,"
        "사내 규정 한도를 넘는 항목을 찾아 합계와 함께 반환한다."
      ),
      "tags": ["expense", "finance", "policy"],
      "examples":[
        "출장 T-2026-03 경비를 정리해주세요",
        "T-2026-04 규정 위반이 있는지 봐 주세요",
      ],
    }
  ],
}