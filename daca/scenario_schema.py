scenario_schema = {
    'name': {
        'required': True,
        'type': 'string'
    },
    'date': {
        'required': True,
        'type': 'date'
    },
    'metrics': {
        'required': True,
        'type': 'dict',
        'schema': {
            'percentage': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'value': {
                        'required': True,
                        'type': 'number',
                        'min': 0,
                        'max': 100
                    },
                    'trend': {
                        'type': 'string',
                        'nullable': True,
                        'regex': '^(?i)(down|equal|up)$'
                    }
                }
            }
        }
    }
}