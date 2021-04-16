#  Copyright (c) 2021 ZBW  – Leibniz Information Centre for Economics
#
#  This file is part of qualle.
#
#  qualle is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  qualle is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with qualle.  If not, see <http://www.gnu.org/licenses/>.
from typing import List, Dict, Any, Type

import numpy as np

from qualle.features.base import Features


CombinedFeaturesData = Dict[Type[Features], Any]


class CombinedFeatures(Features):
    """Combine n features by horizontal stacking"""
    def __init__(self, features: List[Features]):
        self.features = features

    def fit(self, X=None, y=None):
        for f in self.features:
            f.fit()
        return self

    def transform(self, X: CombinedFeaturesData):
        combined = [f.transform(X[f.__class__]) for f in self.features]
        return np.hstack(combined)
