# marzeqdiscord
My own extensions for discord.py.

Features list:
* Custom command parser with support for command flags and parameters.
    * Pros:
        * Support for command flags and parameters
        * The default command parser still can be used
    * Cons:
        * Every command needs to be initialised separately
        * The parser gives us the invoked message to work with, not the context
