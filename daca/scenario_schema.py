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
    'template_dir': {
        'required': False,
        'nullable': True,
        'type': 'string'
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
                'ipv4_address': {
                    'required': False,
                    'nullable': False,
                    'type': 'string',
                    'regex': '^(127|10)(\.\d{1,3}){3}$|^(172\.1[6-9]|172\.2[0-9]|172\.3[0-1]|192\.168)(\.\d{1,3}){2}$'
                },
                'setup': {
                    'required': True,
                    'type': 'dict',
                    'schema': {
                        'type': {
                            'required': True,
                            'type': 'string',
                            'regex': '^(?i)(shell|script|ansible)$'
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
                    'nullable': True,
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'type': {
                                'type': 'string',
                                'required': True,
                                'regex': '^(?i)(pcap|files|mordor|elastic|cli_recording)$'
                            },
                            'val': {
                                'type': 'list',
                                'schema': {
                                    'type': 'string'
                                }
                            }
                        }
                    }
                },
                'depends_on': {
                    'required': False,
                    'type':'list',
                    'schema': {
                        'type': 'string'
                    }
                }
            }
        }
    },
    'variables': {
        'required': True,
        'type': 'list',
        'nullable': True,
        'anyof_schema': [
            {
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
                            'type': 'dict'
                        }
                    }
                }
            },
            {
                'type': 'dict',
                'required': True
            }
        ]
    }
}