from enum import Enum
from typing import Dict, List, Literal, NamedTuple, Optional, TypedDict

InputType = Literal["IMAGE", "LLM_INSTR_FOLLOWING", "LLM_RLHF", "PDF", "TEXT", "VIDEO"]

class JobCategory(NamedTuple):
    """Contains information for a category."""

    category_name: str
    id: int
    job_id: str

class JobTool(str, Enum):
    """List of tools."""

    MARKER = "marker"
    POLYGON = "polygon"
    POLYLINE = "polyline"
    POSE = "pose"
    RANGE = "range"
    RECTANGLE = "rectangle"
    SEMANTIC = "semantic"
    VECTOR = "vector"


class ProjectDict(TypedDict):
    description: str
    id: str
    inputType: InputType
    jsonInterface: Optional[Dict]
    organizationId: str
    title: str


class ChatItemRole(str, Enum):
    """Enumeration of the supported chat item role."""

    ASSISTANT = "ASSISTANT"
    USER = "USER"
    SYSTEM = "SYSTEM"
    
class ChatItem(TypedDict):
    """Dict that represents a ChatItem."""

    id: str
    content: str
    createdAt: Optional[str]
    externalId: str
    modelId: Optional[str]
    modelName: Optional[str]
    role: ChatItemRole


class ConversationLabel(TypedDict):
    """Dict that represents a ConversationLabel."""

    completion: Optional[Dict]
    conversation: Optional[Dict]
    round: Optional[Dict]


class Conversation(TypedDict):
    """Dict that represents a Conversation."""

    chatItems: List[ChatItem]
    externalId: Optional[str]
    label: Optional[ConversationLabel]
    labeler: Optional[str]
    metadata: Optional[dict]

class ExportLLMItem(TypedDict):
    """LLM asset chat part."""

    role: str
    content: str
    id: Optional[str]
    chat_id: Optional[str]
    model: Optional[str]

class JobLevel:
    ROUND = "round"
    CONVERSATION = "conversation"
    COMPLETION = "completion"