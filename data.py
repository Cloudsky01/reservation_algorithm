x = {
    "connections": {
        "golf #1": [
            "HOLDING",
            "golf #2"
        ],
        "golf #2": [
            "HOLDING",
            "golf #1",
            "golf #3"
        ],
        "golf #3": [
            "HOLDING",
            "golf #2",
            "golf #4"
        ],
        "golf #4": [
            "HOLDING",
            "golf #3",
            "golf #5"
        ],
        "golf #5": [
            "HOLDING",
            "golf #4",
            "golf #10"
        ],
        "golf #10": [
            "HOLDING",
            "golf #5",
            "golf #7"
        ],
        "golf #7": [
            "HOLDING",
            "golf #10",
            "golf #8"
        ],
        "golf #8": [
            "HOLDING",
            "golf #7",
            "golfsefs"
        ],
        "golfsefs": [
            "HOLDING",
            "golf #8",
            "golf rs"
        ],
        "golf rs": [
            "HOLDING",
            "golfsefs",
            "quilles 1"
        ],
        "quilles 1": [
            "HOLDING",
            "golf rs",
            "quilles 2"
        ],
        "quilles 2": [
            "HOLDING",
            "quilles 1",
            "quilles 3"
        ],
        "quilles 3": [
            "HOLDING",
            "quilles 2",
            "quilles 4"
        ],
        "quilles 4": [
            "HOLDING",
            "quilles 3",
            "quilles 5"
        ],
        "quilles 5": [
            "HOLDING",
            "quilles 4"
        ]
    },
    "startTime": 32400000,
    "endTime": 97200000,
    "increment": 900000,
    "reservation": [
        {
            "startTime": 64800000,
            "endTime": 68400000,
            "wantedRooms": [
                None,
                None,
                None
            ],
            "actualRooms": [
                "golf #1",
                "golf #2",
                "golf #3"
            ]
        },
        {
            "startTime": 61200000,
            "endTime": 64800000,
            "wantedRooms": [
                None,
                None,
                None,
                None
            ],
            "actualRooms": [
                "golf #1",
                "golf #2",
                "golf #3",
                "golf #4"
            ]
        },
        {
            "startTime": 62100000,
            "endTime": 65700000,
            "wantedRooms": [
                None
            ],
            "actualRooms": [
                "golf #5"
            ]
        },
        {
            "startTime": 62100000,
            "endTime": 65700000,
            "wantedRooms": [
                "golf #10"
            ],
            "actualRooms": [
                "golf #10"
            ]
        },
        {
            "startTime": 63000000,
            "endTime": 70200000,
            "wantedRooms": [
                None,
                None,
                None
            ],
            "actualRooms": [
                "golf #7",
                "golf #8",
                "golfsefs"
            ]
        },
        {
            "startTime": 63000000,
            "endTime": 73800000,
            "wantedRooms": [
                "quilles 5"
            ],
            "actualRooms": [
                "quilles 5"
            ]
        }
    ]
}