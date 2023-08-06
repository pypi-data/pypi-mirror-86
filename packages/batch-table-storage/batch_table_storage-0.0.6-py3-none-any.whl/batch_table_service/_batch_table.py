from azure.cosmosdb.table import TableBatch


class CustomTableBatch(TableBatch):
    def delete(self, entity, if_match='*'):
        self.delete_entity(partition_key=entity['PartitionKey'], row_key=entity['RowKey'], if_match=if_match)
