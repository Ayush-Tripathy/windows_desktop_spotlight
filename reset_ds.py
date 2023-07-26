#!/usr/bin/env python
import constants.flags
import handlers.flags_handler

handlers.flags_handler.reset([constants.flags.RESET_FLAG], verifyfiles=True)
print("Reset complete. Press Enter to exit.")
input()
