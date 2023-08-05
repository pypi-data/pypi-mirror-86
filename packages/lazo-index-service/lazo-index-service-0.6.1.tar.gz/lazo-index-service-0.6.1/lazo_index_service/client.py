import grpc
from lazo_index_service.errors import lazo_client_exception

from lazo_index_service.lazo_index_pb2 import \
    ColumnIdentifier, ColumnValue, DataPath, Dataset, LazoSketchData, Value
from lazo_index_service.lazo_index_pb2_grpc import LazoIndexStub


class LazoIndexClient:
    """
    Index textual and categorical columns using a Lazo server.
    """

    def __init__(self, host='localhost', port=50051):
        channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = LazoIndexStub(channel)

    @staticmethod
    def make_column_value(value, dataset_id, column_name):
        return ColumnValue(
            value=value,
            column_identifier=ColumnIdentifier(
                dataset_id=dataset_id,
                column_name=column_name
            )
        )

    @staticmethod
    def make_value(value):
        return Value(value=value)

    @staticmethod
    def make_data_path(data_url, dataset_id, column_name_list):
        column_identifiers = list()
        for column_name in column_name_list:
            column_identifiers.append(
                ColumnIdentifier(
                    dataset_id=dataset_id,
                    column_name=column_name
                )
            )
        return DataPath(
            url=data_url,
            column_identifiers=column_identifiers
        )

    @staticmethod
    def make_lazo_sketch_data(number_permutations, hash_values, cardinality):
        return LazoSketchData(
            number_permutations=number_permutations,
            hash_values=hash_values,
            cardinality=cardinality
        )

    @staticmethod
    def make_dataset(dataset_id, column_name_list):
        return Dataset(
            dataset_id=dataset_id,
            column_names=column_name_list
        )

    def generate_stream_column_value(
        self, column_values, dataset_id, column_name,
    ):
        for value in column_values:
            yield self.make_column_value(
                str(value),
                str(dataset_id),
                str(column_name),
            )

    def generate_stream_value(self, column_values):
        for value in column_values:
            yield self.make_value(str(value))

    @lazo_client_exception
    def index_data(self, column_values, dataset_id, column_name):
        """
        Sketch a stream of values, and index it.

        :param column_values: array of string values
        :param dataset_id: the id of the dataset
        :param column_name: column name for indexing
        :return: a tuple with number of permutations, hash_values,
            and the cardinality of the Lazo sketch
        """

        lazo_sketch_data = self.stub.IndexData(
            self.generate_stream_column_value(
                column_values, dataset_id, column_name
            )
        )

        return (
            lazo_sketch_data.number_permutations,
            lazo_sketch_data.hash_values,
            lazo_sketch_data.cardinality
        )

    def index_data_path(self, data_path, dataset_id, column_name_list):
        """
        Sketch columns from a file, and index them.

        :param data_path: path to dataset
        :param dataset_id: the id of the dataset
        :param column_name_list: list of column names for indexing
        :return: a list of tuples with number of permutations, hash_values,
            and the cardinality of the Lazo sketch
        """

        return self.index_data_url(
            'file://' + data_path,
            dataset_id,
            column_name_list,
        )

    @lazo_client_exception
    def index_data_url(self, data_url, dataset_id, column_name_list):
        """
        Sketch columns from a file, and index them.

        :param data_url: URL of dataset
        :param dataset_id: the id of the dataset
        :param column_name_list: list of column names for indexing
        :return: a list of tuples with number of permutations, hash_values,
            and the cardinality of the Lazo sketch
        """

        lazo_sketch_data_list = self.stub.IndexDataPath(
            self.make_data_path(data_url, dataset_id, column_name_list)
        )

        results = []
        for lazo_sketch_data in lazo_sketch_data_list.lazo_sketch_data:
            results.append(
                (
                    lazo_sketch_data.number_permutations,
                    lazo_sketch_data.hash_values,
                    lazo_sketch_data.cardinality
                )
            )
        return results

    @lazo_client_exception
    def get_lazo_sketch_from_data(
        self, column_values, dataset_id, column_name,
    ):
        """
        Sketch a stream of values, don't index it.

        :param column_values: array of string values
        :param dataset_id: the id of the dataset
        :param column_name: column name for indexing
        :return: a tuple with number of permutations, hash_values,
            and the cardinality of the Lazo sketch
        """

        lazo_sketch_data = self.stub.GetLazoSketchFromData(
            self.generate_stream_column_value(
                column_values, dataset_id, column_name
            )
        )

        return (
            lazo_sketch_data.number_permutations,
            lazo_sketch_data.hash_values,
            lazo_sketch_data.cardinality
        )

    def get_lazo_sketch_from_data_path(
        self, data_path, dataset_id, column_name_list,
    ):
        """
        Sketch columns from a file, don't index them.

        :param data_path: path to dataset
        :param dataset_id: the id of the dataset
        :param column_name_list: list of column names for indexing
        :return: a list of tuples with number of permutations, hash_values,
            and the cardinality of the Lazo sketch
        """

        return self.get_lazo_sketch_from_data_url(
            'file://' + data_path,
            dataset_id,
            column_name_list,
        )

    @lazo_client_exception
    def get_lazo_sketch_from_data_url(
        self, data_url, dataset_id, column_name_list,
    ):
        """
        Sketch columns from a file, don't index them.

        :param data_url: URL of dataset
        :param dataset_id: the id of the dataset
        :param column_name_list: list of column names for indexing
        :return: a list of tuples with number of permutations, hash_values,
            and the cardinality of the Lazo sketch
        """

        lazo_sketch_data_list = self.stub.GetLazoSketchFromDataPath(
            self.make_data_path(data_url, dataset_id, column_name_list)
        )

        results = []
        for lazo_sketch_data in lazo_sketch_data_list.lazo_sketch_data:
            results.append(
                (
                    lazo_sketch_data.number_permutations,
                    lazo_sketch_data.hash_values,
                    lazo_sketch_data.cardinality
                )
            )
        return results

    @lazo_client_exception
    def remove_sketches(self, dataset_id, column_name_list):
        """
        Removes sketches corresponding to the input dataset
        from both the index and the storage.

        :param dataset_id: the id of the dataset
        :param column_name_list: list of column names for removing
        :return: True if success
        """

        ack = self.stub.RemoveSketches(
            self.make_dataset(dataset_id, column_name_list)
        )
        return ack.ack

    @lazo_client_exception
    def query_data(self, column_values):
        """
        Queries the Lazo index with a stream of values.

        :param column_values: array of string values for querying
        :return: a list of tuples containing the dataset identifier, the column
            name, and the maximum containment threshold.
        """

        lazo_query_results = self.stub.QueryData(
            self.generate_stream_value(column_values)
        )

        results = []
        for query_result in lazo_query_results.query_results:
            results.append((
                query_result.column.dataset_id,
                query_result.column.column_name,
                query_result.max_threshold
            ))

        return results

    def query_data_path(self, data_path, dataset_id, column_name_list):
        """
        Queries the Lazo index with columns from a file.

        :param data_path: path to dataset
        :param dataset_id: the id of the dataset
        :param column_name_list: list of column names for querying
        :return: a list of list of tuples containing the dataset identifier,
            the column name, and the maximum containment threshold.
        """

        return self.query_data_url(
            'file://' + data_path,
            dataset_id,
            column_name_list,
        )

    @lazo_client_exception
    def query_data_url(self, data_url, dataset_id, column_name_list):
        """
        Queries the Lazo index with columns from a file.

        :param data_url: URL of dataset
        :param dataset_id: the id of the dataset
        :param column_name_list: list of column names for querying
        :return: a list of list of tuples containing the dataset identifier,
            the column name, and the maximum containment threshold.
        """

        lazo_query_results_list = self.stub.QueryDataPath(
            self.make_data_path(data_url, dataset_id, column_name_list)
        )

        results = []
        for lazo_query_results in lazo_query_results_list.column_query_results:
            column_query_results = []
            for query_result in lazo_query_results.query_results:
                column_query_results.append((
                    query_result.column.dataset_id,
                    query_result.column.column_name,
                    query_result.max_threshold
                ))
            results.append(column_query_results)

        return results

    @lazo_client_exception
    def query_lazo_sketch_data(
        self, number_permutations, hash_values, cardinality,
    ):
        """
        Queries the Lazo index with sketches.

        :param number_permutations: the number of hashes in the sketch
        :param hash_values: the hash values of the sketch
        :param cardinality: the cardinality of the sketch
        :return: a list of list of tuples containing the dataset identifier,
            the column name, and the maximum containment threshold.
        """

        lazo_query_results = self.stub.QueryLazoSketchData(
            self.make_lazo_sketch_data(
                number_permutations,
                hash_values,
                cardinality,
            )
        )

        results = []
        for query_result in lazo_query_results.query_results:
            results.append((
                query_result.column.dataset_id,
                query_result.column.column_name,
                query_result.max_threshold
            ))

        return results
