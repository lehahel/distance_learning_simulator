from client import studlib

default_ip = "localhost:8000"

handlers = {
    'size': 3,
    'text': [
        "Enter your name",
        "Enter your weight",
        "Enter your ip (with port)"
    ],
    'checker': [
        studlib.check_name,
        studlib.check_weight,
        studlib.check_ip
    ],
    'error_text': [
        "Error!\nName can only contain symbols\nfrom latin alphabet!",
        "Error!\nWeight should be a number",
        "Error!\nip should have format *.*.*.*:*"
    ],
    'info_type': [
        'name',
        'weight',
        'ip'
    ]
}

interrupted_sleep_reasons = [
    "You've been woken up by your aggressive cat"
]

well_slept_reasons = [
    "You've slept enough and now feeling like cucumber"
]

min_stat_limits = {
    "energy": 0,
    "mood_level": -5
}

max_stat_limits = {
    "energy": 15,
    "mood_level": 5
}

errors = {
    "connection": "no connection",
    "wrong_args_food": "wrong arguments given to food",
    "wrong_food": "food should have Food type",
    "wrong_args_student": "Wrong arguments given to student"
}

end_text = {
    "eat": "You've eaten {} and now feeling happier",
    "no_en_play": "No energy to play;(",
    "play": "You won {} games",
    "no_en_study": "Not enough energy (5 at least needed)",
    "study": "You've run out of energy and your mood's bad, but you've become smarter"
}
