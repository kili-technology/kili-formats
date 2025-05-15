from enum import Enum
from typing import Any, Dict, List, Literal, NamedTuple, NewType, Optional, TypedDict, Union

InputType = Literal[
    "GEOSPATIAL", "IMAGE", "LLM_INSTR_FOLLOWING", "LLM_RLHF", "LLM_STATIC", "PDF", "TEXT", "VIDEO"
]
MLTask = Literal["CLASSIFICATION", "NAMED_ENTITIES_RECOGNITION", "OBJECT_DETECTION"]

AnnotationId = NewType("AnnotationId", str)
AnnotationValueId = NewType("AnnotationValueId", str)
JobName = NewType("JobName", str)
KeyAnnotationId = NewType("KeyAnnotationId", str)
LabelId = NewType("LabelId", str)


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


class Job(TypedDict):
    """Contains job settings."""

    content: Any
    instruction: str
    isChild: bool
    tools: List[JobTool]
    mlTask: MLTask
    models: Any  # example: {"interactive-segmentation": {"job": "SEMANTIC_JOB_MARKER"}},
    isVisible: bool
    required: int
    isNew: bool


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


class Vertice(TypedDict):
    """Vertice."""

    x: float
    y: float


class ObjectDetectionAnnotationValue(TypedDict):
    """Object detection annotation value."""

    vertices: List[List[List[Vertice]]]


class ClassificationAnnotationValue(TypedDict):
    """Classification annotation value."""

    categories: List[str]


class ClassificationAnnotation(TypedDict):
    """Classification annotation."""

    # pylint: disable=unused-private-member
    __typename: Literal["ClassificationAnnotation"]
    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]
    annotationValue: ClassificationAnnotationValue


class RankingOrderValue(TypedDict):
    """Ranking order value."""

    rank: int
    elements: List[str]


class RankingAnnotationValue(TypedDict):
    """Ranking annotation value."""

    orders: List[RankingOrderValue]


class RankingAnnotation(TypedDict):
    """Ranking annotation."""

    # pylint: disable=unused-private-member
    __typename: Literal["RankingAnnotation"]
    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]
    annotationValue: RankingAnnotationValue


class TranscriptionAnnotationValue(TypedDict):
    """Transcription annotation value."""

    text: str


class TranscriptionAnnotation(TypedDict):
    """Transcription annotation."""

    # pylint: disable=unused-private-member
    __typename: Literal["TranscriptionAnnotation"]
    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]
    annotationValue: TranscriptionAnnotationValue


class Annotation(TypedDict):
    """Annotation."""

    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]


class ObjectDetectionAnnotation(TypedDict):
    """Object detection annotation."""

    # pylint: disable=unused-private-member
    __typename: Literal["ObjectDetectionAnnotation"]
    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]
    annotationValue: ObjectDetectionAnnotationValue
    name: Optional[str]
    mid: str
    category: str


class FrameInterval(TypedDict):
    """Frame interval."""

    start: int
    end: int


class VideoObjectDetectionKeyAnnotation(TypedDict):
    """Video object detection key annotation."""

    id: KeyAnnotationId
    frame: int
    annotationValue: ObjectDetectionAnnotationValue


class VideoClassificationKeyAnnotation(TypedDict):
    """Video classification key annotation."""

    id: KeyAnnotationId
    frame: int
    annotationValue: ClassificationAnnotationValue


class VideoTranscriptionKeyAnnotation(TypedDict):
    """Video transcription key annotation."""

    id: KeyAnnotationId
    frame: int
    annotationValue: TranscriptionAnnotationValue


class VideoObjectDetectionAnnotation(TypedDict):
    """Video object detection annotation."""

    # pylint: disable=unused-private-member
    __typename: Literal["VideoObjectDetectionAnnotation"]
    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]
    frames: List[FrameInterval]
    keyAnnotations: List[VideoObjectDetectionKeyAnnotation]
    name: Optional[str]
    mid: str
    category: str


class VideoClassificationAnnotation(TypedDict):
    """Video classification annotation."""

    # pylint: disable=unused-private-member
    __typename: Literal["VideoClassificationAnnotation"]
    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]
    frames: List[FrameInterval]
    keyAnnotations: List[VideoClassificationKeyAnnotation]


class VideoTranscriptionAnnotation(TypedDict):
    """Video transcription annotation."""

    # pylint: disable=unused-private-member
    __typename: Literal["VideoTranscriptionAnnotation"]
    id: AnnotationId
    labelId: LabelId
    job: JobName
    path: List[List[str]]
    frames: List[FrameInterval]
    keyAnnotations: List[VideoTranscriptionKeyAnnotation]


VideoAnnotation = Union[
    VideoObjectDetectionAnnotation,
    VideoClassificationAnnotation,
    VideoTranscriptionAnnotation,
]

ClassicAnnotation = Union[
    ClassificationAnnotation,
    ObjectDetectionAnnotation,
    RankingAnnotation,
    TranscriptionAnnotation,
]
