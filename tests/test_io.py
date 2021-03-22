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
from qualle.io import train_input_from_tsv
from qualle.models import TrainInput


def test_train_input_from_tsv(mocker):
    m = mocker.mock_open(
        read_data='title0\tconcept0:1,concept1:0.5\tconcept1,concept3\n'
                  'title1\tconcept2:1,concept3:0.5\tconcept3'
    )
    mocker.patch('qualle.io.open', m)

    assert train_input_from_tsv('dummypath') == TrainInput(
        docs=['title0', 'title1'],
        predicted_concepts=[
            ['concept0', 'concept1'], ['concept2', 'concept3']
        ],
        true_concepts=[['concept1', 'concept3'], ['concept3']]
    )
