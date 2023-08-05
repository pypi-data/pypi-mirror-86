# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rrl']
install_requires = \
['redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'rrl',
    'version': '0.3.1',
    'description': 'simple redis rate limiting',
    'long_description': '# rrl - Redis Rate Limiting\n\nVery simple reusable redis-backed rate limiting code.  Designed for OpenStates.org.\n\n![Test](https://github.com/jamesturk/rrl/workflows/Test/badge.svg)\n\n## Configuration\n\n`rrl`, as the name implies, requires a [Redis](https://redis.io) server.\n\n`rrl` is entirely configured by environment variables:\n\n**RRL_REDIS_HOST** - hostname of Redis instance (default: *localhost*)\n**RRL_REDIS_PORT** - port of Redis instance (default: *6379*)\n**RRL_REDIS_DB** - database ID to use for RRL (default: *0*)\n\n## Usage\n\nUsage can be throttled on a per-minute, per-hour, and/or per-day basis.\n\n`rrl` has the concept of a `Tier` which associates a name with a set of limitations, for instance:\n\n```\n# create two tiers\nbronze = Tier(name="bronze", per_minute=1, per_hour=0, per_day=500)\nsilver = Tier(name="silver", per_minute=5, per_hour=0, per_day=4000)\n```\n\nThese tiers do not use the per_hour feature, but will limit users to 1 or 5 requests per minute respectively.  There\'s also a daily limit at 500 or 4000 requests per day.\n\nThen you\'ll need an instance of `rrl.RateLimiter`, which will be instantiated with these tiers:\n\n```\nlimiter = RateLimiter(tiers=[bronze, silver])\n```\n\nThen to apply limiting, you\'ll call the `check_limit` function, which takes three parameters:\n\n* `key` - A unique-per user key, often the user\'s API key or username. (Note: `rrl` does not know if a key is valid or not, that validation should be in your application and usually occur before the call to `check_limit`.)\n* `tier_name` - The name of one of the tiers as specified when instantiating the `RateLimiter` class.  (Note: `rrl` does not have a concept of which users are in which tier, that logic should be handled by your key validation code.)\n\nExample call:\n\n```\nlimiter.check_limit(key="1234", tier_name="bronze")\n```\n\nThis call will return without any error if the call is deemed allowed.\n\nIf any of the rate limits are exceeded it will instead raise a `RateLimitExceeded` exception describing which limit was exceeded.  \nIf multiple limits were exceeded it will return the shortest limit violated.\n\n## Advanced Usage\n\n### Obtaining Usage Information\n\nYour `RateLimiter` instance also has a method named `get_usage_since`, which takes four parameters:\n\n* `key` - Which key you\'re requesting usage information for.\n* `start` - Date that you\'d like usage since, as a `datetime.date` object.\n* `end` - Optional end date if you\'d only like usage within a certain window, otherwise the current day is used.\n\nThis will return a list of `DailyUsage` dataclasses with the following attributes:\n\n* `date` - `datetime.date`\n* `calls` - Number of calls made on that date.\n\nThis method can be useful for showing users an overview of their data.\n\n### Advanced Configuration\n\nWhen instantiating a `RateLimiter` there are several keyword-only parameters you may set:\n\n**prefix**\n\nPassing a prefix like: \n```\nlimiter = RateLimiter(tiers, prefix="v1")\n```\nwill scope all calls to limiter to a given prefix, this can be useful if you want multiple limiters but want to ensure that they do not interfere with one another.\n\n**use_redis_time**\n\n`True` by default, but if you set to `False` the application\'s system time will be used instead. \n\nThe tradeoff here is one fewer call to Redis per call to `check_limit`, but if your machines experience any clock drift unexpected results may occur.\n\n**track_daily_usage**\n\n`True` by default, but if set to `False`, `rrl` will not store the necessary information to make `get_usage_since` work.  This results in a slight overhead reduction, but the usage information will not be stored in Redis and will be impossible to retrieve.\n',
    'author': 'James Turk',
    'author_email': 'dev@jamesturk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
