from time import sleep

from glimpse_generators.unreal_guardian import UnrealGuardian
from glimpse_generators.unrealcv_fix import Client


class UnrealDiedException(Exception):
    pass


class UnrealException(Exception):
    pass


class UnrealCVWrapper(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self, *args, **kwargs):
        try:
            return super().connect(*args, **kwargs)
        except ConnectionError:
            raise UnrealDiedException()

    def request(self, *args, **kwargs):
        try:
            response = super().request(*args, **kwargs)
        except ConnectionError:
            raise UnrealDiedException()
        print("Unreal CV Wrapper: request params", args, kwargs, "response", response)

        if "error" in response:
            raise UnrealException(response)

        return response


class UnrealClientWrapper:
    def __init__(self, host, port, unreal_binary_path):
        self.guardian = UnrealGuardian(unreal_binary_path)
        self.host = host
        self.port = port
        self.client = None

        self._initialize_client()

    def _initialize_client(self):
        for _ in range(3):
            try:
                for i in range(11):
                    print(f"Trying to connect to UnrealCV server on port {self.port + i}")
                    self.client = UnrealCVWrapper((self.host, self.port + i))
                    connection_result = self.client.connect()

                    if connection_result:
                        break

                    sleep(3)
                else:
                    raise ConnectionError("Failed to connect to UnrealCV server; is it running?")


                self.client.request('vget /unrealcv/status')
                self.client.request('vset /cameras/spawn')
                self.client.request('vset /camera/1/rotation -90 0 0')
                return
            except UnrealDiedException:
                self.guardian.reset()

    def request(self, *args, **kwargs):
        if not self.guardian.is_alive:
            self.guardian.reset()
            self._initialize_client()
            raise UnrealDiedException()
        try:
            return self.client.request(*args, **kwargs)
        except UnrealDiedException as e:
            self.guardian.reset()
            self._initialize_client()
            raise e

    def disconnect(self):
        self.client.disconnect()
        self.guardian.close()
