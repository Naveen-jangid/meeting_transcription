"""Create Elasticsearch indices with mappings."""
from db.es import CAPTIONS_MAPPING


def bootstrap(es_client=None) -> None:
    # Placeholder to demonstrate where index creation would happen.
    _ = CAPTIONS_MAPPING


if __name__ == "__main__":
    bootstrap()
