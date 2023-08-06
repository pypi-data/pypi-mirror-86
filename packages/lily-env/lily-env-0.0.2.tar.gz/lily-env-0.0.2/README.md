
# Lily-Env - environment variables management by humans for humans

Foundations:
- Detect broken environments
- Inform statically and dynamically about any issues with the env.


## Defining the Environment Parser

Use the below example as a inspiration regarding type of fields one can define.

```python

import lily_env as env


class MyEnvParser(env.EnvParser):

    secret_key = env.CharField()

    is_important = env.BooleanField()

    aws_url = env.URLField()

    number_of_workers = env.IntegerField()

    unit_price = env.FloatField()

```

Each field supports the following arguments:

- `required` (boolean) - if environment variable is required to be present
- `default` (target type) - default to be used in case environment variable was not found
- `allow_null` (boolean) - if environment variable can be nullable
- `description` (str) - where one can describe the purpose of a given field when the name itself is not enough to capture it.

Besides those some fields are supporting extra fields:

- `CharField`:

    - `min_length` - validates if minimum amount of characters was provided
    - `max_length` - validates if maximum amount of characters was provided


## CLI

One can print to stdout dump of currently available environment by running
the following:

```bash

lily_env dump

```


## TODOs

[ ] integrate with AWS secrets
