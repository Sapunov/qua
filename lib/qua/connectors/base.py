class BaseConnector:

    def get_objects_to_index(self):

        raise NotImplementedError('`get_objects_to_index()` must be implemented')

    def get_object_data(self, uri):

        raise NotImplementedError('`get_object_data(uri)` must be implemented')
