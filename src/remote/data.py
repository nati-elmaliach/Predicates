test_user = {"user": {"profile": {"age": 30, "score": 85, "active": True}}}

test_predicates = [
    # Age checks
    {
        "feature": ".user.profile.age",
        "operation": {
            "operator": "and",
            "operations": [
                {"operator": "isGreaterThan", "operand": 18},
                {"operator": "isLessThan", "operand": 65},
            ],
        },
    },
    # Score with nested AND/OR
    {
        "feature": ".user.profile.score",
        "operation": {
            "operator": "or",
            "operations": [
                {
                    "operator": "and",
                    "operations": [
                        {"operator": "isGreaterThan", "operand": 80},
                        {"operator": "isLessThan", "operand": 100},
                    ],
                },
                {
                    "operator": "and",
                    "operations": [
                        {"operator": "isGreaterThan", "operand": 0},
                        {"operator": "isLessThan", "operand": 20},
                    ],
                },
            ],
        },
    },
    # Active status check
    {
        "feature": ".user.profile.active",
        "operation": {"operator": "eqTo", "operand": False},
    },
]
