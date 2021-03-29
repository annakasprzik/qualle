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

import numpy as np
import pytest
from sklearn.exceptions import NotFittedError
from stwfsapy.text_features import mk_text_features

from qualle.label_calibration.base import LabelCalibrator


class DummyRegressor:

    def fit(self, X, y):
        # No implementation required
        pass

    def predict(self, X):
        return np.array(range(X.shape[0]))


@pytest.fixture
def calibrator():
    return LabelCalibrator(DummyRegressor())


def test_lc_predict(calibrator, X):
    calibrator.fit(X, [3, 5])
    assert np.array_equal(calibrator.predict(X), [0, 1])


def test_lc_predict_without_fit_raises_exc(calibrator, X):
    with pytest.raises(NotFittedError):
        calibrator.predict(X)


def test_lc_fit_fits_regressor_with_txt_features(calibrator, X, mocker):
    y = [3, 5]
    txt_features = mk_text_features().fit(X)
    X_transformed = txt_features.transform(X)

    spy = mocker.spy(calibrator.regressor, 'fit')
    calibrator.fit(X, y)
    spy.assert_called_once()
    assert (spy.call_args[0][0].toarray() == X_transformed.toarray()).all()
    assert spy.call_args[0][1] == y
