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

from pyspark.ml.tests.test_regression import RegressionTestsMixin
from pyspark.testing.connectutils import ReusedConnectTestCase


# TODO(SPARK-52764): Re-enable this test after fixing the flakiness.
@unittest.skip("Disabled due to flakiness, should be enabled after fixing the issue")
class RegressionParityTests(RegressionTestsMixin, ReusedConnectTestCase):
    pass


if __name__ == "__main__":
    from pyspark.ml.tests.connect.test_parity_regression import *  # noqa: F401

    try:
        import xmlrunner  # type: ignore[import]

        testRunner = xmlrunner.XMLTestRunner(output="target/test-reports", verbosity=2)
    except ImportError:
        testRunner = None
    unittest.main(testRunner=testRunner, verbosity=2)
