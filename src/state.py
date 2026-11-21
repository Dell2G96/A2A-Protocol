import operator
from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages

# class ExpenseState(TypedDict):
#     trip_id: str # 시작할 때 넣어주는 값
#     messages : Annotated[list, add_messages] # 모델과 주고 받은 대화
#     steps: int # 몇 바퀴 돌았는가? -> 순환이 생기기 때문
#     receipts: list[dict] # 영수증 목록 -> 첫 번째 노드가 채운다.
#     rates : dict # 환율
#     total: int # 합계 -> 두 번쨰 노드가 계산
#     violations: list[str] # 규정 위반에 대한 목록
#     report: str # 사라밍 읽는 한 줄 -> 모델이 작성
#     log: Annotated[list[str], operator.add] # 덮어쓰기 방지 , 이어 붙인다 
#     approved: bool | None

class ExpenseState(TypedDict):
  trip_id: str
  receipts: list[dict]
  rates: dict
  total: int
  violations: list[str]
  report: str
  approved: bool |None
  log: Annotated[list[str], operator.add]

