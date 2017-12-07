from pyes import exceptions, ES
import json


def main():
    config = json.load(open('config.json', 'r'))
    conn = connect_to_es(config)
    create_index(conn)


def connect_to_es(config):
    """
    Attempts connection to an existing instance of elasticsearch.

    :param config: global configuration dictionary
    :return: connection object
    """

    addr_port = '{}:{}'.format(config['host'], config['port'])
    conn = ES(addr_port)
    return conn


def create_index(conn):
    """
    Attempts to create an index.

    :param conn: connection object
    :return: True if successful, else False
    """

    try:
        conn.indices.delete_index("test-index")
        print('index deleted')

    except TypeError:
        print('index not found')

    try:
        # conn.indices.create_index("test-index")
        print('index created')
        return True

    except exceptions.IndexAlreadyExistsException:
        print('could not create index')

    return False


if __name__ == '__main__':
    main()
