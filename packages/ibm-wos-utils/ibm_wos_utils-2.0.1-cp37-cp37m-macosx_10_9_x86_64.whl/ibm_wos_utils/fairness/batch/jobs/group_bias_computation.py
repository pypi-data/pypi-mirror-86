# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2020
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import json
import os
import sys
import time
import uuid
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

from ibm_wos_utils.fairness.batch.utils.batch_utils import BatchUtils
from ibm_wos_utils.fairness.batch.utils.python_util import get
from ibm_wos_utils.joblib.jobs.aios_spark_job import AIOSBaseJob


class GroupBiasComputationJob(AIOSBaseJob):

    def __init__(self, arguments, job_name):
        """
        Constructor for the job class.
        :arguments: The arguments to the Spark job.
        """
        super().__init__(arguments)
        self.name = job_name

    def calculate_group_bias(self, data: DataFrame, inputs: dict, data_types: dict, model_type: str) -> dict:
        """
        The Spark job which calculates the disparate impact ratio and publishes the fairness metrics for the payload and their corresponding perturbed data.
        :data: The spark data frame containing the payload data.
        :inputs: The inputs dictionary.
        :data_types: The dictionary containing data types of all the fairness attributes.
        :model_type: The model type.
        """
        # First calculating the disparate impact on the payload data
        di_dict = BatchUtils.calculate_di_dict(
            data, inputs, data_types, model_type)
        return di_dict

    def run_job(self) -> None:
        """
        The entry point method for the Spark job.
        """
        start_time = time.time()

        try:
            # Reading the inputs from the argument list
            subscription = self.arguments["subscription"]
            monitor_instance = self.arguments["monitor_instance"]
            output_file_path = self.arguments["output_file_path"]

            if self.storage_type != "hive":
                raise Exception("Only Hive storage type is supported.")

            # Getting the inputs dictionary
            inputs = BatchUtils.get_inputs_from_monitor_instance(
                monitor_instance)

            # Getting the payload logging data source
            pl_data_source = BatchUtils.get_data_source_from_subscription(
                subscription, "payload")

            # Reading data from Hive table
            self.spark.catalog.setCurrentDatabase(
                get(pl_data_source, "database_name"))
            df_spark = self.spark.sql(
                "select * from {}".format(get(pl_data_source, "table_name")))

            # Getting the model type and the data types of the fairness attributes
            model_type = get(subscription, "entity.asset.problem_type")
            data_types = BatchUtils.get_data_types(
                subscription, inputs["fairness_attributes"])

            di_dict = self.calculate_group_bias(
                df_spark, inputs, data_types, model_type)
            end_time = time.time()
            time_taken = end_time - start_time

            # Building the output JSON
            output_json = {
                "job_output": [
                    {
                        "data_name": "payload",
                        "counts": di_dict,
                        "time_taken": time_taken
                    }
                ]
            }

            # Write to HDFS
            output_file_name = "{}.json".format(self.name)
            output_path = "{}/{}".format(output_file_path, output_file_name)
            self.save_data(path=output_path, data_json=output_json)
        except Exception as ex:
            self.save_exception_trace(str(ex))
            raise ex
        finally:
            # Stopping the spark session
            if self.spark is not None:
                self.spark.stop()
