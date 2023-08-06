# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE

from rowgenerators.exceptions import AppUrlError

class PumsError(Exception):
    pass

class PumsUrlError(AppUrlError):
    pass