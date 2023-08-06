import ssl

import pika


def build_connection_parameters(
        *,
        username: str,
        password: str,
        host: str,
        port: int,
        virtual_host: str = None,
        ssl_context: ssl.SSLContext = None,
) -> pika.ConnectionParameters:
    """
    Build the connection parameters for RabbitMQ

    :param username:                the username to use to connect to the RabbitMQ server
    :param password:                the password to use to connect to the RabbitMQ server
    :param host:                    the host to connect to
    :param port:                    the port to use when connecting
    :param virtual_host:            the virtual host to use (default is None)
    :param ssl_context:             the SSL context to use (default is None, to use no encryption)
    :return:                        the connection parameters
    """

    credentials = pika.PlainCredentials(username, password)
    extra_params = {}

    # pika does not accept None as default argument, so we must not pass anything if the argument is not there
    if virtual_host is not None:
        extra_params["virtual_host"] = virtual_host
    if ssl_context is not None:
        extra_params["ssl_options"] = pika.SSLOptions(ssl_context)

    return pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=credentials,
        **extra_params
    )
