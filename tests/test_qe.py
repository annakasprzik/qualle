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

from qualle.quality_estimation import RecallPredictor, RecallPredictorInput, \
    LabelCalibrationFeatures


class DummyRegressor:

    def fit(self, *args):
        # Empty because no functionality required
        pass

    def predict(self, X):
        return X[:, 0] * X[:, 1]


@pytest.fixture
def X():
    return RecallPredictorInput(
        label_calibration=np.array([3, 1, 1], dtype="int32"),
        no_of_pred_labels=np.array([2, 1, 5], dtype="int32")
    )


@pytest.fixture
def predictor():
    return RecallPredictor(DummyRegressor())


def test_rp_predict(predictor, X):
    y = np.array([0.8, 1., 4])
    predictor.fit(X, y)

    assert np.array_equal(
        predictor.predict(X),
        np.array([3 * (3 - 2), 1 * (1 - 1), 1 * (1 - 5)])
    )


def test_rp_fit_fits_pipeline(predictor, X, mocker):
    y = np.array([0.8, 1., 4])

    spy = mocker.spy(predictor.pipeline, 'fit')
    predictor.fit(X, y)

    spy.assert_called_once_with(X, y)


def test_calibration_features_transform(X):
    lf = LabelCalibrationFeatures()
    assert np.array_equal(
        lf.transform(X), np.array([[3, 1], [1, 0], [1, -4]])
    )
