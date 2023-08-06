from azure.cosmosdb.table.tableservice import TableService

from batch_table_service._batch_table import CustomTableBatch


class BatchTableService(TableService):
    """
    This is the wrapper class managing Azure Table Storage batches.

    The Azure Table service offers structured storage in the form of tables. Tables
    store data as collections of entities. Entities are similar to rows. An entity
    has a primary key and a set of properties. A property is a name, typed-value pair,
    similar to a column. The Table service does not enforce any schema for tables,
    so two entities in the same table may have different sets of properties. Developers
    may choose to enforce a schema on the client side. A table may contain any number
    of entities.

    :ivar object key_encryption_key:
        The key-encryption-key optionally provided by the user. If provided, will be used to
        encrypt/decrypt in supported methods.
        For methods requiring decryption, either the key_encryption_key OR the resolver must be provided.
        If both are provided, the resolver will take precedence.
        Must implement the following methods for APIs requiring encryption:
        wrap_key(key)--wraps the specified key (bytes) using an algorithm of the user's choice. Returns the encrypted key as bytes.
        get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
        get_kid()--returns a string key id for this key-encryption-key.
        Must implement the following methods for APIs requiring decryption:
        unwrap_key(key, algorithm)--returns the unwrapped form of the specified symmetric key using the string-specified algorithm.
        get_kid()--returns a string key id for this key-encryption-key.
    :ivar function key_resolver_function(kid):
        A function to resolve keys optionally provided by the user. If provided, will be used to decrypt in supported methods.
        For methods requiring decryption, either the key_encryption_key OR
        the resolver must be provided. If both are provided, the resolver will take precedence.
        It uses the kid string to return a key-encryption-key implementing the interface defined above.
    :ivar function(partition_key, row_key, property_name) encryption_resolver_functions:
        A function that takes in an entity's partition key, row key, and property name and returns
        a boolean that indicates whether that property should be encrypted.
    :ivar bool require_encryption:
        A flag that may be set to ensure that all messages successfully uploaded to the queue and all those downloaded and
        successfully read from the queue are/were encrypted while on the server. If this flag is set, all required
        parameters for encryption/decryption must be provided. See the above comments on the key_encryption_key and resolver.
    """

    def batch_insert_entities(self, table_name, entities, require_encryption=False, key_encryption_key=None,
                              encryption_resolver=None, timeout=None):
        """
        Creates and commits batches. All entities will be inserted
        Users insert entity operation in batch. See
        :func:`~azure.storage.table.tableservice.TableService.insert_entity` for more
        information on inserts.

        :param str table_name:
            The name of the table used in the operations.
        :param entities:
            The entities to be inserted.
        :type entities: list of dict or :class:`~azure.storage.table.models.Entity`
        :param object key_encryption_key:
            The user-provided key-encryption-key. Must implement the following methods:
            wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
            get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
            get_kid()--returns a string key id for this key-encryption-key.
        :param function(partition_key, row_key, property_name) encryption_resolver:
            A function that takes in an entities partition key, row key, and property name and returns
            a boolean that indicates whether that property should be encrypted.
        :param int timeout:
            The server timeout, expressed in seconds.
        :return:
            A list of the batch responses corresponding to the requests in the batch.
            The items could either be an etag, in case of success, or an error object in case of failure.
        :rtype: list(:class:`~azure.storage.table.models.AzureBatchOperationError`, str)
        """
        return self._handle_batch(
            table_name=table_name,
            entities=entities,
            batch_function=CustomTableBatch.insert_entity,
            require_encryption=require_encryption,
            key_encryption_key=key_encryption_key,
            encryption_resolver=encryption_resolver,
            timeout=timeout,
        )

    def batch_update_entities(self, table_name, entities, require_encryption=False, key_encryption_key=None,
                              encryption_resolver=None, timeout=None, if_match='*'):
        """
        Creates and commits batches. All entities will be updated
        Uses update entity operation in batch. See
        :func:`~azure.storage.table.tableservice.TableService.update_entity` for more
        information on updates.

        :param str table_name:
            The name of the table used in the operations.
        :param entities:
            The entities to be updated.
        :type entities: list of dict or :class:`~azure.storage.table.models.Entity`
        :param object key_encryption_key:
            The user-provided key-encryption-key. Must implement the following methods:
            wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
            get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
            get_kid()--returns a string key id for this key-encryption-key.
        :param function(partition_key, row_key, property_name) encryption_resolver:
            A function that takes in an entities partition key, row key, and property name and returns
            a boolean that indicates whether that property should be encrypted.
        :param int timeout:
            The server timeout, expressed in seconds.
        :param str if_match:
            The client may specify the ETag for the entity on the
            request in order to compare to the ETag maintained by the service
            for the purpose of optimistic concurrency. The update operation
            will be performed only if the ETag sent by the client matches the
            value maintained by the server, indicating that the entity has
            not been modified since it was retrieved by the client. To force
            an unconditional update, set If-Match to the wildcard character (*).
        :return:
            A list of the batch responses corresponding to the requests in the batch.
            The items could either be an etag, in case of success, or an error object in case of failure.
        :rtype: list(:class:`~azure.storage.table.models.AzureBatchOperationError`, str)
        """
        return self._handle_batch(
            table_name=table_name,
            entities=entities,
            batch_function=CustomTableBatch.update_entity,
            require_encryption=require_encryption,
            key_encryption_key=key_encryption_key,
            encryption_resolver=encryption_resolver,
            timeout=timeout,
            if_match=if_match
        )

    def batch_merge_entities(self, table_name, entities, require_encryption=False, key_encryption_key=None,
                             encryption_resolver=None, timeout=None, if_match='*'):
        """
        Creates and commits batches. All entities will be merged
        Uses update entity operation in batch. See
        :func:`~azure.storage.table.tableservice.TableService.merge_entity` for more
        information on merges.

        :param str table_name:
            The name of the table used in the operations.
        :param entities:
            The entities to be merged.
        :type entities: list of dict or :class:`~azure.storage.table.models.Entity`
        :param object key_encryption_key:
            The user-provided key-encryption-key. Must implement the following methods:
            wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
            get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
            get_kid()--returns a string key id for this key-encryption-key.
        :param function(partition_key, row_key, property_name) encryption_resolver:
            A function that takes in an entities partition key, row key, and property name and returns
            a boolean that indicates whether that property should be encrypted.
        :param int timeout:
            The server timeout, expressed in seconds.
        :param str if_match:
            The client may specify the ETag for the entity on the
            request in order to compare to the ETag maintained by the service
            for the purpose of optimistic concurrency. The update operation
            will be performed only if the ETag sent by the client matches the
            value maintained by the server, indicating that the entity has
            not been modified since it was retrieved by the client. To force
            an unconditional update, set If-Match to the wildcard character (*).
        :return:
            A list of the batch responses corresponding to the requests in the batch.
            The items could either be an etag, in case of success, or an error object in case of failure.
        :rtype: list(:class:`~azure.storage.table.models.AzureBatchOperationError`, str)
        """
        return self._handle_batch(
            table_name=table_name,
            entities=entities,
            batch_function=CustomTableBatch.merge_entity,
            require_encryption=require_encryption,
            key_encryption_key=key_encryption_key,
            encryption_resolver=encryption_resolver,
            timeout=timeout,
            if_match=if_match
        )

    def batch_delete_entities(self, table_name, entities, require_encryption=False, key_encryption_key=None,
                              encryption_resolver=None, timeout=None, if_match='*'):
        """
        Delete a list of entities in batch
        :func:`~azure.storage.table.tableservice.TableService.delete_entity` for more
        information on deletes.

        :param entities:
            The entities to be inserted or replaced.
        :type entities: list of dict or :class:`~azure.storage.table.models.Entity`
        :param object key_encryption_key:
            The user-provided key-encryption-key. Must implement the following methods:
            wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
            get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
            get_kid()--returns a string key id for this key-encryption-key.
        :param function(partition_key, row_key, property_name) encryption_resolver:
            A function that takes in an entities partition key, row key, and property name and returns
            a boolean that indicates whether that property should be encrypted.
        :param int timeout:
            The server timeout, expressed in seconds.
        :param str if_match:
            The client may specify the ETag for the entity on the
            request in order to compare to the ETag maintained by the service
            for the purpose of optimistic concurrency. The update operation
            will be performed only if the ETag sent by the client matches the
            value maintained by the server, indicating that the entity has
            not been modified since it was retrieved by the client. To force
            an unconditional update, set If-Match to the wildcard character (*).
        """
        return self._handle_batch(
            table_name=table_name,
            entities=entities,
            batch_function=CustomTableBatch.delete,
            require_encryption=require_encryption,
            key_encryption_key=key_encryption_key,
            encryption_resolver=encryption_resolver,
            timeout=timeout,
            if_match=if_match
        )

    def batch_insert_or_replace_entities(self, table_name, entities, require_encryption=False, key_encryption_key=None,
                                         encryption_resolver=None, timeout=None):
        """
        Creates and commits batches. All entities will be inserted or replaced
        Uses update entity operation in batch. See
        :func:`~azure.storage.table.tableservice.TableService.insert_or_replace_entity` for more
        information on insert or replace operations.

        :param str table_name:
            The name of the table used in the operations.
        :param entities:
            The entities to be inserted or replaced.
        :type entities: list of dict or :class:`~azure.storage.table.models.Entity`
        :param object key_encryption_key:
            The user-provided key-encryption-key. Must implement the following methods:
            wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
            get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
            get_kid()--returns a string key id for this key-encryption-key.
        :param function(partition_key, row_key, property_name) encryption_resolver:
            A function that takes in an entities partition key, row key, and property name and returns
            a boolean that indicates whether that property should be encrypted.
        :param int timeout:
            The server timeout, expressed in seconds.
        :return:
            A list of the batch responses corresponding to the requests in the batch.
            The items could either be an etag, in case of success, or an error object in case of failure.
        :rtype: list(:class:`~azure.storage.table.models.AzureBatchOperationError`, str)
        """
        return self._handle_batch(
            table_name=table_name,
            entities=entities,
            batch_function=CustomTableBatch.insert_or_replace_entity,
            require_encryption=require_encryption,
            key_encryption_key=key_encryption_key,
            encryption_resolver=encryption_resolver,
            timeout=timeout
        )

    def batch_insert_or_merge_entities(self, table_name, entities, require_encryption=False, key_encryption_key=None,
                                       encryption_resolver=None, timeout=None):
        """
        Creates and commits batches. All entities will be inserted or merged
        Uses update entity operation in batch. See
        :func:`~azure.storage.table.tableservice.TableService.insert_or_merge_entity` for more
        information on insert or merge operations.

        :param str table_name:
            The name of the table used in the operations.
        :param entities:
            The entities to be inserted or merged.
        :type entities: list of dict or :class:`~azure.storage.table.models.Entity`
        :param object key_encryption_key:
            The user-provided key-encryption-key. Must implement the following methods:
            wrap_key(key)--wraps the specified key using an algorithm of the user's choice.
            get_key_wrap_algorithm()--returns the algorithm used to wrap the specified symmetric key.
            get_kid()--returns a string key id for this key-encryption-key.
        :param function(partition_key, row_key, property_name) encryption_resolver:
            A function that takes in an entities partition key, row key, and property name and returns
            a boolean that indicates whether that property should be encrypted.
        :param int timeout:
            The server timeout, expressed in seconds.
        :return:
            A list of the batch responses corresponding to the requests in the batch.
            The items could either be an etag, in case of success, or an error object in case of failure.
        :rtype: list(:class:`~azure.storage.table.models.AzureBatchOperationError`, str)
        """
        return self._handle_batch(
            table_name=table_name,
            entities=entities,
            batch_function=CustomTableBatch.insert_or_merge_entity,
            require_encryption=require_encryption,
            key_encryption_key=key_encryption_key,
            encryption_resolver=encryption_resolver,
            timeout=timeout
        )

    def _handle_batch(self, table_name, entities, batch_function, require_encryption=False, key_encryption_key=None,
                      encryption_resolver=None, timeout=None, if_match=None):
        # Sort objects into batches, each batch needs the same "PartitionKey"
        batch_objects = dict()
        for obj in entities:
            batch_objects.setdefault(obj['PartitionKey'], []).append(obj)

        kwargs = dict()
        if if_match:
            kwargs.setdefault('if_match', if_match)
        results = []
        # create batches for every partitionkey
        for values in batch_objects.values():
            # chunk per 100, max batch size
            for object_list in list(_chunks(values, 100)):
                batch = CustomTableBatch(require_encryption=require_encryption, key_encryption_key=key_encryption_key,
                                         encryption_resolver=encryption_resolver)
                # fill batch with objects
                for obj in object_list:
                    batch_function(self=batch, entity=obj, **kwargs)

                results.extend(self.commit_batch(table_name=table_name, batch=batch, timeout=timeout))
        return results


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
