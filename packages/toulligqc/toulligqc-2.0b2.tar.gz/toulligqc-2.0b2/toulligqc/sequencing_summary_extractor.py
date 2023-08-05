# -*- coding: utf-8 -*-

#                  ToulligQC development code
#
# This code may be freely distributed and modified under the
# terms of the GNU General Public License version 3 or later
# and CeCILL. This should be distributed with the code. If you
# do not have a copy, see:
#
#      http://www.gnu.org/licenses/gpl-3.0-standalone.html
#      http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
#
# Copyright for this code is held jointly by the Genomic platform
# of the Institut de Biologie de l'École Normale Supérieure and
# the individual authors.
#
# For more information on the ToulligQC project and its aims,
# visit the home page at:
#
#      https://github.com/GenomicParisCentre/toulligQC
#
# First author: Lionel Ferrato-Berberian
# Maintainer: Karine Dias
# Since version 0.1

# Extraction of statistics from sequencing_summary.txt file (1D chemistry)

import pandas as pd
import sys
from toulligqc import plotly_graph_generator as pgg
import numpy as np
import re
import os.path


class SequencingSummaryExtractor:
    """
    Extraction of data from sequencing_summary.txt and optional barcoding files.
    The data is extracted from dataframes and placed in the result_dict in the form of key-value pairs
    """

    def __init__(self, config_dictionary):
        """
        Constructor that initialize the values of the config_dictionary and check in the case of 1 argument in 
        sequencing_summary_source if the path points to a file, the others cases are managed in check_conf 
        and _load_sequencing_summary_data methods
        :param config_dictionary: dictionary containing all files or directories paths for sequencing_summary.txt and barcoding files
        """
        self.config_dictionary = config_dictionary
        self.sequencing_summary_source = self.config_dictionary['sequencing_summary_source']
        self.result_directory = config_dictionary['result_directory']
        self.sequencing_summary_files = self.sequencing_summary_source.split('\t')

        self.is_barcode = False
        if config_dictionary['barcoding'] == 'True':
            for f in self.sequencing_summary_files:
                if self._is_barcode_file(f) or self._is_sequencing_summary_with_barcodes(f):
                    self.is_barcode = True

        self.my_dpi = int(self.config_dictionary['dpi'])


    def check_conf(self):
        """
        Check if the sequencing summary source contains a sequencing summary file
        :return: boolean and a string for error message
        """

        if not self.sequencing_summary_files[0]:
            return False, "No file has been defined"

        found = False
        while not found:
            for f in self.sequencing_summary_files:
                try:
                    if self._is_sequencing_summary_file(f) or self._is_sequencing_summary_with_barcodes(f):
                        found = True
                except FileNotFoundError:
                    return False, "No such file or directory " + f
            break

        if not found:
            return False, "No sequencing summary file has been found"
        return True, ""


    def init(self):
        """
        Creation of the dataframe containing all info from sequencing_summary.txt
        :return: Panda's Dataframe object
        """
        self.dataframe_1d = self._load_sequencing_summary_data()
        if self.dataframe_1d.empty:
            raise pd.errors.EmptyDataError("Dataframe is empty")
        
        # Rename 'sequence_length_template' and 'mean_qscore_template'
        self.dataframe_1d.rename(columns={'sequence_length_template': 'sequence_length',
                                           'mean_qscore_template': 'mean_qscore'}, inplace=True)
        
        # Replace all NaN values by 0 to avoid data manipulation errors when columns are not the same length
        self.dataframe_1d = self.dataframe_1d.fillna(0)
        self.channel_df = self.dataframe_1d['channel']
        self.passes_filtering_df = self.dataframe_1d['passes_filtering']
        self.sequence_length_df = self.dataframe_1d['sequence_length']
        self.qscore_df = self.dataframe_1d['mean_qscore']
        self.time_df = self.dataframe_1d['start_time']
        self.duration_df = self.dataframe_1d['duration']

        # Dictionary for storing all pd.Series and pd.Dataframe entries
        self.dataframe_dict = {}

        if self.is_barcode:
            self.barcode_selection = self.config_dictionary['barcode_selection']


    @staticmethod
    def get_name() -> str:
        """
        Get the name of the extractor.
        :return: the name of the extractor
        """
        return 'Basecaller sequencing summary'


    @staticmethod
    def get_report_data_file_id() -> str:
        """
        Get the report.data id of the extractor.
        :return: a string with the name of the ID of the extractor
        """
        return 'basecaller.sequencing.summary.1d.extractor'


    def _describe_dict(self, result_dict: dict, function, entry: str):
        """
        Set statistics for a key like mean, min, max, median and percentiles (without the count value) filled in the _set_result_value dictionary
        :param result_dict:
        :param function: function returning the values to describe
        :param entry: entry to put in result_dict completed with the statistics
        """
        stats = pd.Series.describe(function).drop("count")
        for key, value in stats.iteritems():
            self._set_result_to_dict(result_dict, entry + '.' + key, value)


    def _barcode_frequency(self, dataframe_dict: dict, entry: str, df_filtered) -> pd.Series:
        """
        Count reads by values of barcode_selection, computes sum of counts by barcode_selection, and sum of unclassified counts.
        Regroup all non used barcodes in index "other"
        Compute all frequency values for each number of barcoded reads
        :param dataframe_dict: dictionary filled with Pandas type values
        :param entry: entry about barcoded counts
        :param prefix: key prefix
        :return: Series with all barcodes (used, non used, and unclassified) frequencies
        """
        # Regroup all barcoded read in Series
        all_barcode_count = df_filtered.value_counts()

        # Sort by list of barcode_selection
        count_sorted = all_barcode_count.sort_index()[self.barcode_selection]
        # Replace all NaN values to zero
        count_sorted.fillna(0, downcast='int16', inplace=True)

        # Compute sum of all used barcodes without barcode 'unclassified'
        self.dataframe_dict[entry + '.count'] = sum(count_sorted.drop("unclassified"))
        
        # Replace entry name ie read.pass/fail.barcode with read.pass/fail.non.used.barcodes.count
        non_used_barcodes_count = entry.replace(".barcoded", ".non.used.barcodes.count")

        # Compute all reads of barcodes that are not in the barcode_selection list
        self.dataframe_dict[non_used_barcodes_count] = sum(all_barcode_count) - sum(count_sorted)
        
        # Create Series for all non-used barcode counts and rename index array with "other"
        other_all_barcode_count = pd.Series(self.dataframe_dict[non_used_barcodes_count], index=['other'])
        
        # Append Series of non-used barcode counts to the Series of barcode_selection counts
        count_sorted = count_sorted.append(other_all_barcode_count).sort_index()

        # Compute frequency for all barcode counts and save into dataframe_dict
        for barcode in count_sorted.to_dict():
            frequency_value = count_sorted[barcode] * 100 / sum(count_sorted)
            self.dataframe_dict[entry.replace(".barcoded", ".") + barcode + ".frequency"] =  frequency_value

        return count_sorted


    @staticmethod
    def _count_boolean_elements(dataframe, column_name, boolean: bool) -> int:
        """
        Returns the number of values of a column filtered by a boolean
        :param colum_name: name of the dafatrame column
        :boolean: bool to filter
        """
        return len(dataframe.loc[dataframe[column_name] == bool(boolean)])


    @staticmethod
    def _series_cols_boolean_elements(dataframe, column_name1: str, column_name2: str, boolean: bool) -> pd.Series:
        """
        Returns a Panda's Series object with the number of values of different columns filtered by a boolean
        :param dataframe: dataframe_1d
        :param column_name1: 1st column to filter
        :param column_name2: 2nd column to filter
        :param boolean: access columns of dataframe by boolean array
        """
        return dataframe[column_name1].loc[dataframe[column_name2] == bool(boolean)]


    @staticmethod
    def _sorted_list_boolean_elements_divided(dataframe, column_name1: str, column_name2: str, boolean: bool, denominator: int):
        """
        Returns a sorted list of values of different columns filtered by a boolean and divided by the denominator
        :param dataframe: dataframe_1d
        :param column_name1: 1st column to filter
        :param column_name2: 2nd column to filter
        :param boolean: access columns of dataframe by boolean array
        :param denominator: number to divide by
        """
        return sorted(dataframe[column_name1].loc[dataframe[column_name2] == bool(boolean)] / denominator)


    def _set_result_value(self, dict, key: str, value):
        """
        Set a key, value pair to the result_dict
        :param result_dict:
        :param key: string entry to add to result_dict
        :param value: int, float, list, pd.Series or pd.Dataframe value of the corresponding key
        """
        try:
            dict[self.get_report_data_file_id() + '.' + key] = value
        except TypeError:
            ("Invalid type for key {0} or value {1} ".format(
                type(key), type(value)))


    def _get_result_value(self, result_dict, key: str):
        """
        :param result_dict:
        :param key: string entry to add to result_dict
        Returns the value associated with the result_dict key
        """
        if not (self.get_report_data_file_id() + '.' + key) in result_dict.keys():
            raise KeyError("Key {key} not found").__format__(key)
        return result_dict.get(self.get_report_data_file_id() + '.' + key)


    def _set_result_to_dict(self, result_dict, key: str, function):
        """
        Add a new item in result_dict with _set_result_value method
        :param result_dict:
        :param key: string entry to add to result_dict
        :param function: function returning key's value
        """
        self._set_result_value(result_dict, key, function)


    def extract(self, result_dict):
        """
        Get Phred score (Qscore) and Length details (frequencies, ratios, yield and statistics) per type read (pass or fail)
        :param result_dict:
        """
        # Basecaller analysis
        if 'sequencing.telemetry.extractor.software.analysis' not in result_dict:
            result_dict['sequencing.telemetry.extractor.software.analysis'] = '1d_basecalling'

        # Read count
        self._set_result_to_dict(result_dict, "read.count", len(self.dataframe_1d))

        # 1D pass information : count, length, qscore values and sorted Series
        self._set_result_to_dict(result_dict, "read.pass.count",
                                 self._count_boolean_elements(self.dataframe_1d, 'passes_filtering', True))
        self._set_result_to_dict(result_dict, "read.pass.length",
                                 self._series_cols_boolean_elements(self.dataframe_1d, 'sequence_length',
                                                                    'passes_filtering', True))
        self._set_result_to_dict(result_dict, "read.pass.qscore",
                                 self._series_cols_boolean_elements(self.dataframe_1d, 'mean_qscore',
                                                                    'passes_filtering', True))
        self._set_result_to_dict(result_dict, "read.pass.sorted",
                                 self._sorted_list_boolean_elements_divided(self.dataframe_1d, 'start_time',
                                                                            'passes_filtering', True, 3600))

        # 1D fail information : count, length, qscore values and sorted Series
        self._set_result_to_dict(result_dict, "read.fail.count",
                                 self._count_boolean_elements(self.dataframe_1d, 'passes_filtering', False))
        self._set_result_to_dict(result_dict, "read.fail.length",
                                 self._series_cols_boolean_elements(self.dataframe_1d, 'sequence_length',
                                                                    'passes_filtering', False))
        self._set_result_to_dict(result_dict, "read.fail.qscore",
                                 self._series_cols_boolean_elements(self.dataframe_1d, 'mean_qscore',
                                                                    'passes_filtering', False))
        self._set_result_to_dict(result_dict, "read.fail.sorted",
                                 self._sorted_list_boolean_elements_divided(self.dataframe_1d, 'start_time',
                                                                            'passes_filtering', False, 3600))

        total_reads = self._get_result_value(result_dict, "read.count")

        # Ratios
        self._set_result_value(result_dict, "read.pass.ratio",
                               (self._get_result_value(result_dict, "read.pass.count") / total_reads))
        self._set_result_value(result_dict, "read.fail.ratio",
                               (self._get_result_value(result_dict, "read.fail.count") / total_reads))

        # Frequencies
        self._set_result_value(result_dict, "read.count.frequency", 100)

        read_pass_frequency = (self._get_result_value(
            result_dict, "read.pass.count") / total_reads) * 100
        self._set_result_value(
            result_dict, "read.pass.frequency", read_pass_frequency)

        read_fail_frequency = (self._get_result_value(
            result_dict, "read.fail.count") / total_reads) * 100
        self._set_result_value(
            result_dict, "read.fail.frequency", read_fail_frequency)

        # Read length information
        self.dataframe_dict["sequence.length"] = self.sequence_length_df
        
        # Yield, n50, run time
        self._set_result_value(result_dict, "yield", sum(self.sequence_length_df))

        self._set_result_value(result_dict, "n50", self._compute_n50())
        
        self._set_result_to_dict(
            result_dict, "start.time.sorted", sorted(self.dataframe_1d['start_time'] / 3600))

        self._set_result_value(result_dict, "run.time", max(
            self._get_result_value(result_dict, "start.time.sorted")))

        # Retrieve Qscore column information and save it in mean.qscore entry
        self._set_result_value(result_dict, "mean.qscore",
                               self.qscore_df)

        # Get channel occupancy statistics and store each value into result_dict
        for index, value in self._occupancy_channel().items():
            self._set_result_value(
                result_dict, "channel.occupancy.statistics." + index, value)

        # Get statistics about all reads length and store each value into result_dict
        sequence_length_statistics = self.sequence_length_df.describe()

        for index, value in sequence_length_statistics.items():
            self._set_result_value(
                result_dict, "all.read.length." + index, value)

        # Add statistics (without count) about read pass/fail length in the result_dict
        self._describe_dict(result_dict, self._get_result_value(
            result_dict, "read.pass.length"), "read.pass.length")
        self._describe_dict(result_dict, self._get_result_value(
            result_dict, "read.fail.length"), "read.fail.length")

        # Get Qscore statistics without count value and store them into result_dict
        qscore_statistics = self.dataframe_1d['mean_qscore'].describe().drop(
            "count")

        for index, value in qscore_statistics.items():
            self._set_result_value(
                result_dict, "all.read.qscore." + index, value)

        # Add statistics (without count) about read pass/fail qscore in the result_dict
        self._describe_dict(result_dict, self._get_result_value(
            result_dict, "read.pass.qscore"), "read.pass.qscore")
        self._describe_dict(result_dict, self._get_result_value(
            result_dict, "read.fail.qscore"), "read.fail.qscore")

        if self.is_barcode:
            self._extract_barcode_info(result_dict)


    def _extract_barcode_info(self, result_dict):
        """
        :param result_dict:
        Gather all barcode info for graphs : reads pass/fail and frequency per barcodes
        """
        # Add values unclassified and other to barcode list
        if "unclassified" not in self.barcode_selection:
            self.barcode_selection.append("unclassified")

        # Create keys barcode.arrangement, and read.pass/fail.barcode in dataframe_dict with all values of 
        # column barcode_arrangement when reads are passed/failed
        self.dataframe_dict["barcode.arrangement"] = self.dataframe_1d["barcode_arrangement"]

        # Get barcodes frequency by read type
        series_read_pass_barcode = self._series_cols_boolean_elements(self.dataframe_1d, "barcode_arrangement",
                                                                      "passes_filtering", True)
        
        self.dataframe_dict["read.pass.barcoded"] = self._barcode_frequency(self.dataframe_dict, "read.pass.barcoded",
                                                         series_read_pass_barcode)

        series_read_fail_barcode = self._series_cols_boolean_elements(self.dataframe_1d, "barcode_arrangement",
                                                                      "passes_filtering", False)

        self.dataframe_dict["read.fail.barcoded"] = self._barcode_frequency(self.dataframe_dict, "read.fail.barcoded",
                                                         series_read_fail_barcode)

        read_pass_barcoded_count = self.dataframe_dict["read.pass.barcoded.count"]
        read_fail_barcoded_count = self.dataframe_dict["read.fail.barcoded.count"]

        # Add key "read.pass.barcoded.frequency"
        total_reads = self._get_result_value(result_dict, "read.count")
        self._set_result_value(result_dict, "read.pass.barcoded.frequency",
                               (read_pass_barcoded_count / total_reads) * 100)

        # Add key "read.fail.barcoded.frequency"
        self._set_result_value(result_dict, "read.fail.barcoded.frequency",
                               (read_fail_barcoded_count / total_reads) * 100)

        # Replaces all rows with unused barcodes (ie not in barcode_selection) in column barcode_arrangement with the 'other' value
        self.dataframe_1d.loc[~self.dataframe_1d['barcode_arrangement'].isin(
            self.barcode_selection), 'barcode_arrangement'] = 'other'

        pattern = '(\\d{2})'
        if "other" not in self.barcode_selection:
            self.barcode_selection.append('other')

        # Create dataframes filtered by barcodes and read quality
        for index_barcode, barcode in enumerate(self.barcode_selection):
            barcode_selected_dataframe = self.dataframe_1d[
                self.dataframe_1d['barcode_arrangement'] == barcode]
            barcode_selected_read_pass_dataframe = barcode_selected_dataframe.loc[
                self.dataframe_1d['passes_filtering'] == bool(True)]
            barcode_selected_read_fail_dataframe = barcode_selected_dataframe.loc[
                self.dataframe_1d['passes_filtering'] == bool(False)]
            # search for number of barcode used
            match = re.search(pattern, barcode)
        if match:
            barcode_name = match.group(0)
        else:
            barcode_name = barcode
            # Add all barcode statistics to result_dict based on values of selected dataframes
            self._barcode_stats(result_dict, barcode_selected_dataframe,
                                barcode_selected_read_pass_dataframe, barcode_selected_read_fail_dataframe,
                                barcode_name)

        # Add filtered dataframes (all info by barcode and by length or qscore) to dataframe_dict
        self._barcode_selection_dataframe("sequence_length", "barcode_selection_sequence_length_dataframe",
                                              "length")
        self._barcode_selection_dataframe("mean_qscore", "barcode_selection_sequence_phred_dataframe",
                                              "qscore")


    def _barcode_selection_dataframe(self, df_column_name: str, df_key_name: str, melted_column_name: str):
        """
        Create custom dataframes by grouping all reads per barcodes and per read type (pass/fail) for read length or phred score info
        Reshape the dataframes from wide to long format to display barcode, read type and read length or phred score per read
        These dataframes are used for sequence length and qscore boxplots
        :param key: string name to put in dataframe_dict
        :param df_column_name: name of the dataframe_1d column used for the new barcode_selection_dataframes
        :param melted_column_name: value (qscore or length) to use for renaming column of melted dataframe
        """
        # Count total number of rows
        nrows = self.dataframe_1d.shape[0]
        # Create a new dataframe with 3 columns : 'passes_filtering', 'barcode_arrangement' and the column name parameter
        filtered_df = self.dataframe_1d.filter(
            items=['passes_filtering', df_column_name, 'barcode_arrangement'])

        # Reshape dataframe with new MultiIndex : numbered index of df length + passes filtering index and then shape data by barcode
        barcode_selection_dataframe = filtered_df.set_index([pd.RangeIndex(start=0, stop=nrows), 'passes_filtering'],
                                                            drop=True).pivot(columns="barcode_arrangement")

        # Remove the column parameter index
        barcode_selection_dataframe.columns.droplevel(level=0)

        # Remove sequence_length Multindex to only have barcode_arrangement column labels
        barcode_selection_dataframe.columns = barcode_selection_dataframe.columns.droplevel(
            level=0)

        # Reset index to have all labels in the same level
        barcode_selection_dataframe.reset_index(
            level='passes_filtering', inplace=True)

        # Add final dataframe to dataframe_dict
        self.dataframe_dict[df_key_name] = barcode_selection_dataframe

        # Unpivot dataframe to have only one column of barcodes + passes filtering + melted column name (qscore/length)
        melted_dataframe = pd.melt(
            barcode_selection_dataframe,
            id_vars=['passes_filtering'],
            var_name="barcodes", value_name=melted_column_name)

        # Add melted dataframe to dataframe_dict too
        self.dataframe_dict[df_key_name.replace("_dataframe", "_melted_dataframe")] = melted_dataframe


    def _barcode_stats(self, result_dict, barcode_selected_dataframe, barcode_selected_read_pass_dataframe,
                       barcode_selected_read_fail_dataframe, barcode_name):
        """
        :param result_dict:
        :param prefix: report.data id of the extractor (string)
        :param barcode_selected: barcode filtered dataframes
        Put statistics (with describe method) about barcode length and qscore in result_dict for each selected dataframe : all.read/read.pass and read.fail
        N.b. does not include count statistic for qscore
        """
        df_dict = {'all.read.': barcode_selected_dataframe,
                   'read.pass.': barcode_selected_read_pass_dataframe,
                   'read.fail.': barcode_selected_read_fail_dataframe}

        for df_name, df in df_dict.items():  # df_dict.items = all.read/read.pass/read.fail
            for stats_index, stats_value in df['sequence_length'].describe().items():
                key_to_result_dict = df_name + barcode_name + '.length.' + stats_index
                self._set_result_value(
                    result_dict, key_to_result_dict, stats_value)

            for stats_index, stats_value in df['mean_qscore'].describe().drop('count').items():
                key_to_result_dict = df_name + barcode_name + '.qscore.' + stats_index
                self._set_result_value(
                    result_dict, key_to_result_dict, stats_value)


    def graph_generation(self, result_dict):
        """
        Generation of the different graphs containing in the plotly_graph_generator module
        :return: images array containing the title and the path toward the images
        """
        images_directory = self.result_directory + '/images'
        images = list([pgg.read_count_histogram(result_dict, self.dataframe_dict, 'Read count histogram',
                                                            self.my_dpi, images_directory,
                                                            "Number of reads produced before (Fast 5 in blue) "
                                                            "and after (1D in orange) basecalling. "
                                                            "The basecalled reads are filtered with a 7.5 quality "
                                                            "score threshold in pass (1D pass in green) "
                                                            "or fail (1D fail in red) categories.")])
        images.append(pgg.read_length_multihistogram(result_dict, self.sequence_length_df, 'Read length histogram',
                                                                 self.my_dpi, images_directory,
                                                                 "Size distribution of basecalled reads (1D in orange)."
                                                                 "The basecalled reads are filtered with a 7.5 quality "
                                                                 "score threshold in pass (1D pass in green) "
                                                                 "or fail (1D fail in red) categories."))
        images.append(pgg.yield_plot(result_dict, 'Yield plot of 1D read type',
                                                         self.my_dpi, images_directory,
                                                         "Yield plot of basecalled reads (1D in orange)."
                                                         " The basecalled reads are filtered with a 7.5 quality "
                                                         "score threshold in pass (1D pass in green) "
                                                         "or fail (1D fail in red) categories."))
        images.append(pgg.read_quality_multiboxplot(result_dict, "Read type quality boxplot",
                                                                self.my_dpi, images_directory,
                                                                "Boxplot of 1D reads (in orange) quality."
                                                                "The basecalled reads are filtered with a 7.5 quality "
                                                                "score threshold in pass (1D pass in green) "
                                                                "or fail (1D fail in red) categories."))
        images.append(pgg.allphred_score_frequency(result_dict,
                                                               'Mean Phred score frequency of all 1D read type',
                                                               self.my_dpi, images_directory,
                                                               "The basecalled reads are filtered with a 7.5 quality "
                                                               "score threshold in pass (1D pass in green) "
                                                               "or fail (1D fail in red) categories."))
        channel_count = self.channel_df
        total_number_reads_per_pore = pd.value_counts(channel_count)
        images.append(pgg.plot_performance(total_number_reads_per_pore, 'Channel occupancy of the flowcell',
                                                       self.my_dpi, images_directory,
                                                       "Number of reads sequenced per pore channel."))

        images.append(pgg.all_scatterplot(result_dict, 'Mean Phred score function of 1D read length',
                                                      self.my_dpi, images_directory,
                                                      "The Mean Phred score varies according to the read length."
                                                      "The basecalled reads are filtered with a 7.5 quality "
                                                      "score threshold in pass (1D pass in green) "
                                                      "or fail (1D fail in red) categories."))
        images.append(pgg.sequence_length_over_time(self.time_df, self.dataframe_dict, 'Sequence length over time', self.my_dpi, images_directory,
                                                "Length of reads through run time in hours"))
        images.append(pgg.length_over_time_slider(self.time_df, self.dataframe_dict, 'Sequence length over experiment time with custom number of points', self.my_dpi,
                                                  images_directory, "Custom interpolated scatter plot with sequence length over time"
                                                  ))
        images.append(pgg.phred_score_over_time(self.qscore_df, self.time_df, 'PHRED score over time', self.my_dpi, images_directory,
                                                "Reads PHRED score through run time in hours"))
        images.append(pgg.speed_over_time(self.duration_df, self.sequence_length_df, self.time_df, 'Read speed over time', self.my_dpi, images_directory,
                                          "Speed of reads in base per second through run time in hours"))
        images.append(pgg.nseq_over_time(self.time_df, 'Number of reads over time', self.my_dpi, images_directory, "Number of sequences through run time in hours"))
        
        if self.is_barcode:
            images.append(pgg.barcode_percentage_pie_chart_pass(result_dict, self.dataframe_dict,
                                                                            '1D pass reads percentage of different '
                                                                            'barcodes', self.barcode_selection,
                                                                            self.my_dpi, images_directory,
                                                                            "1D pass read distribution per barcode."))

            images.append(pgg.barcode_percentage_pie_chart_fail(result_dict, self.dataframe_dict,
                                                                            '1D fail reads percentage of different '
                                                                            'barcodes', self.barcode_selection,
                                                                            self.my_dpi, images_directory,
                                                                            "1D fail read distribution per barcode."))

            images.append(pgg.barcode_length_boxplot(result_dict, self.dataframe_dict,
                                                                 '1D reads size distribution for each barcode',
                                                                 self.my_dpi, images_directory,
                                                                 "Read length boxplot per barcode of pass (in green) "
                                                                 "and fail (in red) 1D reads."))

            images.append(pgg.barcoded_phred_score_frequency(self.barcode_selection, self.dataframe_dict,
                                                                         '1D reads Mean Phred score distribution '
                                                                         'for each barcode',
                                                                         self.my_dpi, images_directory,
                                                                         "Read Mean Phred score boxplot per barcode of "
                                                                         "pass (in green) and fail (in red) 1D reads."))
        return images


    def clean(self, result_dict):
        """
        Removing dictionary entries that will not be kept in the report.data file
        :return:
        """
        keys = ["read.pass.length", "read.fail.length",
                "start.time.sorted", "read.pass.sorted", "read.fail.sorted",
                "mean.qscore", "read.pass.qscore", "read.fail.qscore"]

        key_list = []

        for key in keys:
            self._get_result_value(result_dict, key)
            key_list.append(self.get_report_data_file_id() + '.' + str(key))

        if self.is_barcode:
            key_list.extend([(k, v) for k, v in self.dataframe_dict.items()])

        result_dict['unwritten.keys'].extend(key_list)
        self.dataframe_dict = None


    def _occupancy_channel(self):
        """
        Statistics about the channels of the flowcell
        :return: pd.Series object containing statistics about the channel occupancy without count value
        """
        total_reads_per_channel = pd.value_counts(self.channel_df)
        return pd.DataFrame.describe(total_reads_per_channel)


    def _load_sequencing_summary_data(self):
        """
        Load sequencing summary dataframe with or without barcodes
        :return: a Pandas Dataframe object
        """
        # Initialization
        files = self.sequencing_summary_files

        summary_dataframe = None
        barcode_dataframe = None

        sequencing_summary_columns = ['channel', 'start_time',
                                      'passes_filtering',
                                      'sequence_length_template',
                                      'mean_qscore_template',
                                      'duration']

        sequencing_summary_datatypes = {
            'channel': np.int16,
            'start_time': np.float,
            'passes_filtering': np.bool,
            'sequence_length_template': np.int16,
            'mean_qscore_template': np.float,
            'duration' : np.float}

        # If barcoding files are provided, merging of dataframes must be done on read_id column
        barcoding_summary_columns = ['read_id', 'barcode_arrangement']

        barcoding_summary_datatypes = {
            'read_id': object,
            'barcode_arrangement': object
        }

        try:
            # If 1 file and it's a sequencing_summary.txt
            if len(files) == 1 and self._is_sequencing_summary_file(files[0]):
                return pd.read_csv(files[0], sep="\t", usecols=sequencing_summary_columns, dtype=sequencing_summary_datatypes)

            # If 1 file and it's a sequencing_summary.txt with barcode info, load column barcode_arrangement
            elif len(files) == 1 and self._is_sequencing_summary_with_barcodes(files[0]):
                sequencing_summary_columns.append('barcode_arrangement')
                sequencing_summary_datatypes.update(
                    {'barcode_arrangement': object})

                return pd.read_csv(files[0], sep="\t", usecols=sequencing_summary_columns,
                                   dtype=sequencing_summary_datatypes)

            # If multiple files, check if there's a barcoding one and a sequencing one :
            for f in files:

                # check for presence of barcoding files
                if self._is_barcode_file(f):
                    dataframe = pd.read_csv(
                        f, sep="\t", usecols=barcoding_summary_columns, dtype=barcoding_summary_datatypes)
                    if barcode_dataframe is None:
                        barcode_dataframe = dataframe
                    # if a barcoding file has already been read, append the 2 dataframes
                    else:
                        barcode_dataframe = barcode_dataframe.append(
                            dataframe, ignore_index=True)

                # check for presence of sequencing_summary file, if True add column read_id for merging with barcode dataframe
                else:
                    if self._is_sequencing_summary_file(f):
                        sequencing_summary_columns.append('read_id')
                        sequencing_summary_datatypes.update(
                            {'read_id': object})

                        dataframe = pd.read_csv(f, sep="\t", usecols=sequencing_summary_columns,
                                                dtype=sequencing_summary_datatypes)
                        if summary_dataframe is None:
                            summary_dataframe = dataframe
                        else:
                            summary_dataframe = summary_dataframe.append(
                                dataframe, ignore_index=True)

            if barcode_dataframe is None:
                # If no barcodes in files, no merged dataframes on column 'read_id'
                return summary_dataframe.drop(columns=['read_id'])
            else:
                dataframes_merged = pd.merge(
                    summary_dataframe, barcode_dataframe, on='read_id', how='left')
                # delete column read_id after merging
                del dataframes_merged['read_id']

                return dataframes_merged

        except IOError:
            raise FileNotFoundError("Sequencing summary file not found")



    def _compute_n50(self):
        """Compute N50 value of total sequence length"""
        data = self.sequence_length_df.dropna().values
        data.sort()
        half_sum = data.sum()/2
        cum_sum = 0
        for v in data:
            cum_sum += v
            if cum_sum >= half_sum:
                return int(v)
        

    @staticmethod
    def _is_barcode_file(filename):
        """
        Check if input is a barcoding summary file i.e. has the column barcode_arrangement
        :param filename: path of the file to test
        :return: True if the filename is a barcoding summary file
        """
        try:
            with open(filename, 'r') as f:
                header = f.readline()
            return header.startswith('read_id') and 'barcode_arrangement' in header
        except FileNotFoundError:
            "No barcoding file was found"


    @staticmethod
    def _is_sequencing_summary_file(filename):
        """
        Check if input is a sequencing summary file i.e. first word is "filename" and does not have column 'barcode_arrangement'
        :param filename: path of the file to test
        :return: True if the file is indeed a sequencing summary file
        """
        try:
            with open(filename, 'r') as f:
                header = f.readline()
            return header.startswith('filename') and not 'barcode_arrangement' in header
        except IOError:
            raise FileNotFoundError


    @staticmethod
    def _is_sequencing_summary_with_barcodes(filename):
        """
        Check if the sequencing summary has also barcode information :
        - check for presence of columns "filename" and "barcode_arrangement"
        :param filename: path of the file to test
        :return: True if the filename is a sequencing summary file with barcodes
        """
        try:
            with open(filename, 'r') as f:
                header = f.readline()
                return header.startswith('filename') and 'barcode_arrangement' in header
        except IOError:
            raise FileNotFoundError
