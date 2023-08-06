# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2020
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import datetime
import json
import math
import random
import time
from operator import itemgetter
from pyspark.sql.dataframe import DataFrame

from ibm_wos_utils.fairness.batch.utils import constants
from ibm_wos_utils.fairness.batch.utils.python_util import get
from ibm_wos_utils.fairness.batch.utils.sql_utils import SQLUtils


class BatchUtils():

    @classmethod
    def get_group_counts(cls, data: DataFrame, col_name: str, group_vals: list, fav_label_query: str, data_type) -> dict:
        """
        Returns the counts of the given group with it"s given classes counts.
        :data: The data on which the counts are to be counted.
        :col_name: The column on which the counts are to be done.
        :group_vals: The group values/ranges for which the counts are to be made.
        :fav_label_query: The favourable label query.
        :data_type: The data type of the column
        """
        count_dict = {}
        # Getting the group rows
        if data_type in constants.CATEGORICAL_DATA_TYPES:
            all_groups_query = SQLUtils.get_cat_filter_query(
                col_name, "==", group_vals)
        elif data_type in constants.NUMERICAL_DATA_TYPES:
            all_groups_query = SQLUtils.get_num_filter_query(
                col_name, group_vals)
        all_groups_df = data.filter(all_groups_query)

        # Getting the group counts
        for group in group_vals:
            group_query = ""
            # Getting the query for the current group
            if data_type in constants.CATEGORICAL_DATA_TYPES:
                group_query = SQLUtils.get_cat_filter_query(
                    col_name, "==", [group])
            elif data_type in constants.NUMERICAL_DATA_TYPES:
                group_query = SQLUtils.get_num_filter_query(col_name, [group])

            # Getting applying filter to get current group rows
            group_df = all_groups_df.filter(group_query)
            group_fav_count = group_df.filter(fav_label_query).count()
            group_count = group_df.count()
            count_dict[str(group)] = {
                "fav_count": group_fav_count,
                "total_count": group_count
            }
        return count_dict

    @classmethod
    def calculate_di_variables(cls, data: DataFrame, fairness_attribute: str, inputs: dict, data_type, model_type: str) -> dict:
        """
        Calculates the variables needed for disparate impact calculation on the given fairness attribute.
        :data: The data on which the variables are to be calculated.
        :fairness_attribute: The fairness attribute on which the variables are to be calculated.
        :inputs: The inputs dictionary.
        :data_type: The data type of the fairness attribute column.
        """
        di_vars = {
            "majority": {},
            "minority": {}
        }
        # Getting the majority and minority groups
        majority = get(inputs, "majority.{}".format(fairness_attribute))
        minority = get(inputs, "minority.{}".format(fairness_attribute))
        # Getting the label column and favourable outcomes
        label_column = get(inputs, "class_label")
        fav_classes = get(inputs, "favourable_class")

        # Getting the query for favourable outcome rows
        favorable_count_query = None
        if model_type == constants.REGRESSION_MODEL_TYPE:
            favorable_count_query = SQLUtils.get_num_filter_query(
                label_column, fav_classes)
        else:
            favorable_count_query = SQLUtils.get_cat_filter_query(
                label_column, "==", fav_classes)

        # Getting the counts for majority
        di_vars["majority"] = cls.get_group_counts(
            data, fairness_attribute, majority, favorable_count_query, data_type)

        # Getting the counts for minorities
        di_vars["minority"] = cls.get_group_counts(
            data, fairness_attribute, minority, favorable_count_query, data_type)
        return di_vars

    @classmethod
    def calculate_di_dict(cls, data: DataFrame, inputs: dict, data_types: dict, model_type: str) -> dict:
        """
        Returns a dictionary with disparate impact variables for the given data for all fairness attributes in the given inputs.
        :data: The data on which the disparate impact variables are to be calculated.
        :inputs: The inputs dictionary.
        :data_types: The data types of the fairness attributes.
        :model_type: The model type.
        """
        di_dict = {}
        for fairness_attribute in inputs["fairness_attributes"]:
            data_type = data_types[fairness_attribute] if fairness_attribute in data_types else None
            # Calculating the DI variables on the given data
            di_dict[fairness_attribute] = cls.calculate_di_variables(
                data, fairness_attribute, inputs, data_type, model_type)
        return di_dict

    @classmethod
    def get_inputs_from_monitor_instance(cls, monitor_instance: dict) -> dict:
        """
        Converts the given fairness configuration into the inputs dictionary.
        :monitor_instance: The fairness configuration dictionary.
        """
        inputs = {}
        parameters = get(monitor_instance, "entity.parameters")
        inputs["class_label"] = get(parameters, "class_label")
        inputs["favourable_class"] = get(parameters, "favourable_class")
        inputs["unfavourable_class"] = get(parameters, "unfavourable_class")
        inputs["min_records"] = get(parameters, "min_records")
        majority = {}
        minority = {}
        fairness_attributes = []
        threshold = []
        features = get(parameters, "features")
        if features is not None:
            for feature_details in features:
                feature = get(feature_details, "feature")
                if feature is not None:
                    fairness_attributes.append(feature)
                    threshold.append(get(feature_details, "threshold"))
                    majority[feature] = get(feature_details, "majority")
                    minority[feature] = get(feature_details, "minority")
        inputs["majority"] = majority
        inputs["minority"] = minority
        inputs["threshold"] = threshold
        inputs["fairness_attributes"] = fairness_attributes
        return inputs

    @classmethod
    def get_data_source_from_subscription(cls, subscription: dict, data_source_type: str) -> dict:
        """
        Parses the subscription and returns the given data source type.
        :subscription: The subscription JSON.
        :data_source_type: The data source type to be returned.
        """
        data_source = None
        data_sources = get(subscription, "entity.data_sources")
        for ds in data_sources:
            if ds["type"] == data_source_type:
                data_source = ds
                break
        return data_source

    @classmethod
    def get_data_types(cls, subscription: dict, fairness_attributes: list):
        """
        Parses the subscription JSON and returns the data types of the given fairness attribute.
        :subscription: The subscription JSON.
        :fairness_attributes: The list of fairness attributes.
        """
        data_types = {}

        # Getting the fields array from the output data schema
        fields = get(
            subscription, "entity.asset_properties.output_data_schema.fields")
        for field in fields:
            field_name = field["name"]
            if field_name in fairness_attributes:
                data_types[field_name] = field["type"]

        return data_types
