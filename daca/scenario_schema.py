scenario_schema = {
    'name': {
        'required': True,
        'type': 'string'
    },
    'description': {
        'required': True,
        'type': 'string'
    },
    'provisioner': {
        'required': True,
        'type': 'string',
        'regex': '^(?i)(vagrant|docker|terraform)$'
    },
    'use_default_templates': {
        'required': True,
        'type': 'boolean'
    },
    'components': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {
                    'required': True,
                    'type': 'string'
                },
                'description': {
                    'required': True,
                    'type': 'string'
                },
                'image': {
                    'required': True,
                    'type': 'string'
                },
                'setup': {
                    'required': True,
                    'type': 'dict',
                    'schema': {
                        'type': {
                            'required': True,
                            'type': 'string',
                            'regex': '^(?i)(shell|ansible)$'
                        },
                        'val': {
                            'required': True,
                            'type': 'string'
                        }
                    }
                },
                'run': {
                    'required': True,
                    'type': 'dict',
                    'schema': {
                        'type': {
                            'required': True,
                            'type': 'string',
                            'regex': '^(?i)(shell|script)$'
                        },
                        'val': {
                            'required': True,
                            'type': 'string'
                        }
                    }
                },
                'artifacts_to_collect': {
                    'required': False,
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'type': {
                                'type': 'string',
                                'required': True,
                                'regex': '^(?i)(pcap|files|mordor|elastic)$'
                            },
                            'val': {
                                'type': 'list',
                                'schema': {
                                    'type': 'string'
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    'variables': {
        'required': True,
        'type': 'list',
        'nullable': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {
                    'type': 'string',
                    'required': True
                },
                'val': {
                    'type': 'list',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    }
                }
            }
        }
    }
}