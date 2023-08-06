# Copyright 2019 DeepMind Technologies Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Paddings."""

from haiku._src.pad import causal
from haiku._src.pad import create
from haiku._src.pad import full
from haiku._src.pad import PadFn
from haiku._src.pad import reverse_causal
from haiku._src.pad import same
from haiku._src.pad import valid

__all__ = (
    "PadFn",
    "causal",
    "create",
    "full",
    "reverse_causal",
    "same",
    "valid",
)
