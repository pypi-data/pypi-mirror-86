from .route import Route
from .exceptions import InvalidRoute


class RequestBase:
    """OBRequest Base.

    Parameters
    ----------
    base_url : str
        Base URL.
    actions : dict, optional
        Actions to call at status codes, by default None
    kwargs
        Paramters to phrase.
    """

    def __init__(self, client,
                 base_url: str,
                 actions: dict = None,
                 **kwargs) -> None:
        if base_url[:-1] != "/":
            base_url += "/"

        client_params = {}
        for name, value in kwargs.items():
            if name.startswith("_") and not name.startswith("__"):
                client_params[name] = value

        self.init_client = client(
            **client_params
        )

        for name, value in kwargs.items():
            if name.startswith("__"):
                if isinstance(value, Route):
                    value._process(
                        base_url,
                        self.init_client,
                        actions,
                    )

                    setattr(
                        self,
                        name[2:],
                        value
                    )
                else:
                    raise InvalidRoute()
