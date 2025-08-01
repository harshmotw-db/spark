#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest

import pandas as pd
import numpy as np

from pyspark import pandas as ps
from pyspark.testing.pandasutils import PandasOnSparkTestCase
from pyspark.testing.utils import is_ansi_mode_test, ansi_mode_not_supported_message
from pyspark.pandas.tests.data_type_ops.testing_utils import OpsTestBase


class NumMulDivTestsMixin:
    @property
    def float_pser(self):
        return pd.Series([1, 2, 3], dtype=float)

    @property
    def float_psser(self):
        return ps.from_pandas(self.float_pser)

    def test_mul(self):
        pdf, psdf = self.pdf, self.psdf
        for col in self.numeric_df_cols:
            pser, psser = pdf[col], psdf[col]
            self.assert_eq(pser * pser, psser * psser, check_exact=False)
            self.assert_eq(pser * pser.astype(bool), psser * psser.astype(bool), check_exact=False)
            self.assert_eq(pser * True, psser * True, check_exact=False)
            self.assert_eq(pser * False, psser * False, check_exact=False)

            if psser.dtype in [int, np.int32]:
                self.assert_eq(pser * pdf["string"], psser * psdf["string"])
            else:
                self.assertRaises(TypeError, lambda: psser * psdf["string"])

            self.assert_eq(pser * pdf["bool"], psser * psdf["bool"], check_exact=False)

            self.assertRaises(TypeError, lambda: psser * psdf["datetime"])
            self.assertRaises(TypeError, lambda: psser * psdf["date"])
            self.assertRaises(TypeError, lambda: psser * psdf["categorical"])

    def test_truediv(self):
        pdf, psdf = self.pdf, self.psdf
        for col in self.numeric_df_cols:
            pser, psser = pdf[col], psdf[col]
            if psser.dtype in [float, int, np.int32]:
                self.assert_eq(pser / pser, psser / psser)
                self.assert_eq(pser / pser.astype(bool), psser / psser.astype(bool))
                self.assert_eq(pser / True, psser / True)
                self.assert_eq(pser / False, psser / False)

            for n_col in self.non_numeric_df_cols:
                if n_col == "bool":
                    self.assert_eq(pdf["float"] / pdf[n_col], psdf["float"] / psdf[n_col])
                else:
                    self.assertRaises(TypeError, lambda: psser / psdf[n_col])

    def test_floordiv(self):
        pdf, psdf = self.pdf, self.psdf
        pser, psser = pdf["float"], psdf["float"]
        self.assert_eq(pser // pser, psser // psser)
        self.assert_eq(pser // pser.astype(bool), psser // psser.astype(bool))
        self.assert_eq(pser // True, psser // True)
        self.assert_eq(pser // False, psser // False)

        for n_col in self.non_numeric_df_cols:
            if n_col == "bool":
                self.assert_eq(pdf["float"] // pdf["bool"], psdf["float"] // psdf["bool"])
            else:
                for col in self.numeric_df_cols:
                    psser = psdf[col]
                    self.assertRaises(TypeError, lambda: psser // psdf[n_col])


class NumMulDivTests(
    NumMulDivTestsMixin,
    OpsTestBase,
    PandasOnSparkTestCase,
):
    pass


if __name__ == "__main__":
    from pyspark.pandas.tests.data_type_ops.test_num_mul_div import *  # noqa: F401

    try:
        import xmlrunner

        testRunner = xmlrunner.XMLTestRunner(output="target/test-reports", verbosity=2)
    except ImportError:
        testRunner = None
    unittest.main(testRunner=testRunner, verbosity=2)
