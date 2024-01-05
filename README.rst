discord.py-self (stable)
================

A modern, easy to use, feature-rich, and async ready API wrapper for Discord's user API written in Python.

| **Note:**
| Automating user accounts is against the Discord ToS. This library is a proof of concept and I cannot recommend using it. Do so at your own risk.

Fork Changes
------------

These changes have become too numerous to mention, so check out our `docs <https://discordpy-self.readthedocs.io/en/latest/index.html>`_.

**Credits:**

- `Rapptz <https://github.com/Rapptz>`_ for the original library this fork is based on. Without it, the project would not exist.
- `arandomnewaccount <https://www.reddit.com/user/obviouslymymain123/>`_ for help when the project was first started.
- `dolfies <https://github.com/dolfies>`_ Producer of the original discord.py-self.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.
- Mostly compatible with the upstream ``discord.py``.
- Prevents user account automation detection.
- (not original) Reduce the amount of logging that overwhelms the console, such as rate limits.
- (not original) Fixed problem of not replying to own messages (need to add code to prevent looping).
- (not original) Reduce account disabling due to age restrictions.
- (not original) Fix the build number and related information to stabilize and reduce captchas when joining guilds as much as possible.
- (not original) Optimized transmission of voice packets.
- Implements vast amounts of the user account-specific API. For a non-exhaustive list:

 * Sessions
 * Read states
 * Connections
 * Relationships
 * Experiments
 * Protobuf user settings
 * Application/team management
 * Store/SKUs/entitlements
 * Billing (e.g. subscriptions, payments, boosts, promotions, etc.)
 * Interactions (slash commands, buttons, etc.)

Installing
----------

**Python 3.8 or higher is required.**

To install, do the following:

.. code:: sh

    $ git clone https://github.com/voidpro-dev/discord.py-self
    $ cd discord.py-self
    $ python3 -m pip install -U .[voice]
..

or

.. code:: sh

    $ pip install git+https://github.com/voidpro-dev/discord.py-self.git
..

Optional Packages
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (for voice support)

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)

Using with Upstream
~~~~~~~~~~~~~~~~~~~~

If you would like to use the library alongside upstream ``discord.py``, you can install ``selfcord.py`` instead of ``discord.py-self``. Check out the `renamed branch <https://github.com/dolfies/discord.py-self/tree/renamed>`_ for more information.

Quick Example
--------------

.. code:: py

    import discord

    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # only respond to ourselves
            if message.author != self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

    client = MyClient()
    client.run('token')

Bot Example
~~~~~~~~~~~~~

.. code:: py

    import discord
    from discord.ext import commands

    bot = commands.Bot(command_prefix='>', self_bot=True)

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    bot.run('token')

You can find more examples in the examples directory.

Links
------

- `Documentation <https://discordpy-self.readthedocs.io/en/latest/index.html>`_
