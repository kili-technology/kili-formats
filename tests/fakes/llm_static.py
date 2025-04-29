from kili_export_formats.llm import JobLevel


llm_static_annotations = [
    {
        "id": "20250115091847438-1",
        "__typename": "ComparisonAnnotation",
        "job": "COMPARISON_JOB",
        "path": [],
        "labelId": "cm5xmrj7c005c9u0w0o7z3tfu",
        "annotationValue": {
            "choice": {
                "code": "Is much better",
                "firstId": "cm5xmqjdp000j9u0w83phhhim",
                "secondId": "cm5xmqjdp000i9u0w72svc1eg",
            }
        },
        "chatItemId": "cm5xmqjdp000h9u0wdt7v45g1",
    },
    {
        "id": "20250115091848649-2",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_1",
        "path": [],
        "labelId": "cm5xmrj7c005c9u0w0o7z3tfu",
        "annotationValue": {"categories": ["MINOR_ISSUES"]},
        "chatItemId": "cm5xmqjdp000i9u0w72svc1eg",
    },
    {
        "id": "20250115091850107-3",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_2",
        "path": [],
        "labelId": "cm5xmrj7c005c9u0w0o7z3tfu",
        "annotationValue": {"categories": ["NO_ISSUES"]},
        "chatItemId": "cm5xmqjdp000j9u0w83phhhim",
    },
    {
        "id": "20250115091856209-4",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_2",
        "path": [],
        "labelId": "cm5xmrj7c005c9u0w0o7z3tfu",
        "annotationValue": {"categories": ["MINOR_INACCURACY"]},
        "chatItemId": "cm5xmqjdp000i9u0w72svc1eg",
    },
    {
        "id": "20250115091857655-5",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_CONVERSATION_LEVEL",
        "path": [],
        "labelId": "cm5xmrj7c005c9u0w0o7z3tfu",
        "annotationValue": {"categories": ["GLOBAL_GOOD"]},
        "chatItemId": None,
    },
    {
        "id": "20250115091858191-6",
        "__typename": "ClassificationAnnotation",
        "job": "CLASSIFICATION_JOB_AT_ROUND_LEVEL",
        "path": [],
        "labelId": "cm5xmrj7c005c9u0w0o7z3tfu",
        "annotationValue": {"categories": ["BOTH_ARE_GOOD"]},
        "chatItemId": "cm5xmqjdp000h9u0wdt7v45g1",
    },
]

llm_static_chat_items = [
    {
        "id": "cm5xmqjdp000g9u0w1s99cejh",
        "content": "You are an assistant helping the user by providing precise answers.",
        "createdAt": "2025-01-15T08:18:11.325Z",
        "externalId": "cm5xn0ir3000108l16u23casm",
        "modelName": None,
        "modelId": None,
        "parentId": None,
        "role": "SYSTEM",
    },
    {
        "id": "cm5xmqjdp000h9u0wdt7v45g1",
        "content": "Can you give me a function to compute Fibonacci numbers?",
        "createdAt": "2025-01-15T08:18:12.325Z",
        "externalId": "cm5xn11sy000208l1aopo9dfx",
        "modelName": None,
        "modelId": None,
        "parentId": "cm5xmqjdp000g9u0w1s99cejh",
        "role": "USER",
    },
    {
        "id": "cm5xmqjdp000i9u0w72svc1eg",
        "content": "Here is a recursive implementation for calculating Fibonacci numbers:\n\n```python\ndef fibonacci_recursive(n):\n    if n <= 1:\n        return n\n    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)\n```\n\nThis is simple to write but has a time complexity of \\( O(2^n) \\) due to redundant calculations. For large values of \\( n \\), this method becomes highly inefficient.",
        "createdAt": "2025-01-15T08:18:13.325Z",
        "externalId": "cm5xn170s000308l1b6vy9nk5",
        "modelName": "gpt-4o",
        "modelId": None,
        "parentId": "cm5xmqjdp000h9u0wdt7v45g1",
        "role": "ASSISTANT",
    },
    {
        "id": "cm5xmqjdp000j9u0w83phhhim",
        "content": "Here is an optimized implementation using matrix exponentiation, along with an explanation of why it is faster:\n\n```python\nimport numpy as np\n\ndef fibonacci_matrix(n):\n    def matrix_power(matrix, power):\n        result = np.identity(len(matrix), dtype=int)\n        while power:\n            if power % 2:\n                result = np.dot(result, matrix)\n            matrix = np.dot(matrix, matrix)\n            power //= 2\n        return result\n\n    if n == 0:\n        return 0\n    base_matrix = np.array([[1, 1], [1, 0]], dtype=int)\n    result_matrix = matrix_power(base_matrix, n - 1)\n    return result_matrix[0, 0]\n```\n\n### Why is Matrix Exponentiation Faster?\n\nThe recursive method recalculates values for overlapping subproblems, leading to exponential time complexity:\n\n\\[ T(n) = T(n-1) + T(n-2) + O(1), \\]\n\nwhich resolves to \\( O(2^n) \\). This inefficiency arises from redundant recalculations.\n\nThe matrix exponentiation method uses the property that Fibonacci numbers can be represented as a matrix multiplication:\n\n\\[ \\begin{bmatrix} F(n+1) & F(n) \\\\ F(n) & F(n-1) \\end{bmatrix} = \\begin{bmatrix} 1 & 1 \\\\ 1 & 0 \\end{bmatrix}^n. \\]\n\nUsing fast exponentiation (repeated squaring), the matrix power can be computed in \\( O(\\log n) \\) steps. For example, instead of multiplying the matrix \\( n \\) times, we:\n\n1. Square the matrix \\( \\lceil \\log_2 n \\rceil \\) times.\n2. Combine results for any remaining powers.\n\nThis drastically reduces the number of operations compared to the recursive method.\n\n### Comparison of Complexities\n\n- **Recursive Method**: \\( O(2^n) \\)\n- **Matrix Exponentiation**: \\( O(\\log n) \\)\n\nFor large \\( n \\), the difference is substantial. Consider \\( n = 50 \\):\n\n- Recursive method performs roughly \\( 2^{50} \\approx 10^{15} \\) operations.\n- Matrix exponentiation performs approximately \\( \\log_2(50) \\approx 6 \\) matrix multiplications, where each multiplication is \\( O(1) \\) for a fixed-size \\( 2 \\times 2 \\) matrix.\n\n### Example\nUsing \\( n = 10 \\):\n\n1. Recursive Method: Explores all possible paths in the Fibonacci tree, recalculating values like \\( F(8) \\) multiple times.\n2. Matrix Exponentiation: Squares the base matrix 4 times and performs 1 additional multiplication, yielding the result in far fewer steps.\n\nThis efficiency makes matrix exponentiation the preferred method for calculating Fibonacci numbers at scale.",
        "createdAt": "2025-01-15T08:18:14.325Z",
        "externalId": "cm5xn1dvw000008mhfsxq2i0o",
        "modelName": "gpt-o1",
        "modelId": None,
        "parentId": "cm5xmqjdp000h9u0wdt7v45g1",
        "role": "ASSISTANT",
    },
]

llm_static_expected_result = {
    JobLevel.COMPLETION: {
        "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_1": {
            "cm5xn170s000308l1b6vy9nk5": {
                "categories": [
                    "MINOR_ISSUES",
                ],
            },
        },
        "CLASSIFICATION_JOB_AT_COMPLETION_LEVEL_2": {
            "cm5xn170s000308l1b6vy9nk5": {
                "categories": [
                    "MINOR_INACCURACY",
                ],
            },
            "cm5xn1dvw000008mhfsxq2i0o": {
                "categories": [
                    "NO_ISSUES",
                ],
            },
        },
    },
    JobLevel.CONVERSATION: {
        "CLASSIFICATION_JOB_AT_CONVERSATION_LEVEL": {
            "categories": [
                "GLOBAL_GOOD",
            ],
        },
    },
    JobLevel.ROUND: {
        "CLASSIFICATION_JOB_AT_ROUND_LEVEL": {
            0: {
                "categories": [
                    "BOTH_ARE_GOOD",
                ],
            },
        },
        "COMPARISON_JOB": {
            0: {
                "code": "Is much better",
                "firstId": "cm5xn1dvw000008mhfsxq2i0o",
                "secondId": "cm5xn170s000308l1b6vy9nk5",
            },
        },
    },
}
