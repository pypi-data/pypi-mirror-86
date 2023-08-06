# -*- coding: utf-8 -*-
agent_definitions_regex = {
    "test": {
        "confidence": 10,
        "logline": {
            "testkey": "testvalue.*",
        },
    },
    "http": {
        "confidence": 1,
        "url": "https://docs.logdna.com/reference#logsingest",
        "logline": {
            "_ingester": "http",
        },
    },
    "heroku": {
        "confidence": 10,
        "url": "https://docs.logdna.com/docs/heroku",
        "logline": {
            "_ingester": "heroku",
            "_logtype": "heroku_line",
        },
    },
    "linux agent": {
        "confidence": 10,
        "url": "https://github.com/logdna/logdna-agent",
        "logline": {
            "_ingester": "logdna-agent\/.* (.*)",
            "_logtype": "json",
        },
    },
    "nxlog": {
        "confidence": 10,
        "url": "https://docs.logdna.com/docs/nxlog-for-windows",
        "logline": {
            "_line": ".*NXLOG.*",
            "_ingester": ".*syslog.*",
            "_logtype": "json",
        }
    },
    "k8s agent": {
        "confidence": 10,
        "url": "https://github.com/logdna/logdna-agent-v2",
        "logline": {
            "_ingester": "agent",
            "_logtype": "json",
            "namespace": ".*",
            "container": ".*",
            "containerid": ".*",
            "node": ".*",
        },
        "schema": {
            '_ingester': {
                'type': 'string'
            },
            '_logtype': {
                'type': 'string'
            },
            'namespace': {
                'type': 'string'
            },
            'container': {
                'type': 'string'
            },
            'containerid': {
                'type': 'string'
            },
            'node': {
                'type': 'string'
            },
        }
    },
    "Golang code library": {
        "confidence": 10,
        "url": "https://github.com/logdna/logdna-go",
        "logline": {
            "_ingester": "logger-go\/.*",
        },
        "schema": {
            '_ingester': {
                'type': 'string'
            }
        }
    },
    "Node.js code library": {
        "confidence": 10,
        "url": "https://github.com/logdna/nodejs",
        "logline": {
            "_ingester": "nodejs\/.*",
        },
        "schema": {
            '_ingester': {
                'type': 'string'
            }
        }
    },
    "Node.js (Winston) code library": {
        "confidence": 10,
        "url": "https://github.com/logdna/logdna-winston",
        "logline": {
            "_ingester": "logdna-winston\/.*",
        },
        "schema": {
            '_ingester': {
                'type': 'string'
            }
        }
    },
    "Node.js (bunyan) code library": {
        "confidence": 10,
        "url": "https://github.com/logdna/logdna-bunyan",
        "implementation_example": (
            """const {createLogger} = require('bunyan')\n"""
            """const LogDNAStream = require('logdna-bunyan')\n"""
            """\n"""
            """const logDNA = new LogDNAStream({\n"""
            """  key: apikey\n"""
            """}) // See @logdna/logger for more constructor options\n"""
            """\n"""
            """const logger = createLogger({\n"""
            """  name: "My Application"\n"""
            """, streams: [\n"""
            """    {\n"""
            """      stream: process.stdout\n"""
            """    }\n"""
            """  , {\n"""
            """      stream: logDNA\n"""
            """    , type: 'raw'\n"""
            """    , reemitErrorEvents: true // Bubble up 'error' events from @logdna/logger\n"""
            """    }"""
            """  ]\n"""
            """})\n"""
            """\n"""
            """logger.info('Starting application on port %d', app.get('port'))"""),
        "logline": {
            "_ingester": "logdna-bunyan\/.*",
        },
        "schema": {
            '_ingester': {
                'type': 'string'
            }
        }
    },
    "Ruby code library": {
        "confidence": 10,
        "url": "https://github.com/logdna/ruby",
        "logline": {
            "_ingester": "ruby\/.*",
        },
        "implementation_example": (
            """gem 'logdna'\n"""
            """logger = Logdna::Ruby.new(your_api_key, options)\n"""
            """options = {\n"""
            """    :hostname => myHostName,\n"""
            """    :ip =>  myIpAddress,\n"""
            """    :mac => myMacAddress,\n"""
            """    :app => myAppName,\n"""
            """    :level => "INFO",\n"""
            """    :env => "PRODUCTION",\n"""
            """    :meta => {:once => {:first => "nested1", :another => "nested2"}},\n"""
            """    :endpoint => "https://fqdn/logs/ingest"\n"""
            """}\n"""
            """logger.log('This is my first log')\n"""
            """logger.log('This is warn message', {:meta => {:meta => "data"}, :level => "WARN", :app => "awesome", :env => "DEVELOPMENT"})\n"""
        ),
        "schema": {
            '_ingester': {
                'type': 'string',
            }
        }
    },
    "Python code library": {
        "confidence": 10,
        "url": "https://github.com/logdna/python",
        "implementation_example": (
            """import logging\n"""
            """from logdna import LogDNAHandler\n"""
            """\n"""
            """key = 'YOUR INGESTION KEY HERE'\n"""
            """\n"""
            """log = logging.getLogger('logdna')\n"""
            """log.setLevel(logging.INFO)\n"""
            """\n"""
            """options = {\n"""
            """  'hostname': 'pytest',\n"""
            """  'ip': '10.0.1.1',\n"""
            """  'mac': 'C0:FF:EE:C0:FF:EE'\n"""
            """}\n"""
            """\n"""
            """# Defaults to False; when True meta objects are searchable\n"""
            """options['index_meta'] = True\n"""
            """\n"""
            """test = LogDNAHandler(key, options)\n"""
            """\n"""
            """log.addHandler(test)\n"""
            """\n"""
            """log.warning("Warning message", {'app': 'bloop'})\n"""
            """log.info("Info message")"""),
        "logline": {
            "_ingester": "python\/.*",
            "_logtype": "customapp"
        },
        "schema": {
            '_ingester': {
                'type': 'string',
            },
            '_logtype': {
                'type': 'string',
            }
        }
    },
    "aws cloudwatch lambda new": {
        "confidence": 10,
        "url": "https://github.com/logdna/logdna-cloudwatch",
        "logline": {
            "_ingester": "logdna-cloudwatch\/.*",
            "_logtype": "json",
        },
        "schema": {
            '_logtype': {
                'type': 'string',
            },
            '_meta': {
                    "schema": {
                        'filters': {
                            'type': 'list',
                        },
                    }
            }
        }
    },
    "aws cloudwatch lambda old": {
        "confidence": 10,
        "logline": {
            "_ingester": "http",
            "_logtype": "json",
        },
        "schema": {
            '_logtype': {
                'type': 'string',
            },
            '_meta': {
                    "schema": {
                        'filters': {
                            'type': 'list',
                        },
                    }
            }
        }
    },
    "s3 lambda function": {
        "confidence": 10,
        "url": "https://github.com/logdna/logdna-s3",
        "logline": {
            "_ingester": "logdna-s3\/.*",
        },
        "schema": {
            '_ingester': {
                'type': 'string',
            }
        }
    },
}
