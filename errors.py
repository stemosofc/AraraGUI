class NoSerialAvaible(Exception):
    """Raised when Arara aren't avaible"""

    def __init__(self, message="Arara não conectada ao computador"):
        self.message = message
        super().__init__(self.message)


class DisconnectDevice(Exception):
    """Raised when the Arara disconnect from computer"""

    def __init__(self, message="Arara desconectada durante o processo de upload"):
        self.message = message
        super().__init__(self.message)


class NotOpenCOM4(Exception):
    """Raised when other program is using COM port"""

    def __init__(self, message="Não foi possível abrir a porta COM, certifique-se que outro "
                               "programa não está a utilizando"):
        self.message = message
        super().__init__(self.message)


class FatalError(Exception):
    """Raised when a fatal error ocurred"""

    def __init__(self, message="Um erro fatal ocorreu"):
        self.message = message
        super().__init__(self.message)


class WrongBootMode(Exception):
    """Raised when Arara isn't in download mode"""

    def __init__(self, message="Arara não foi colocada em modo de download"):
        self.message = message
        super().__init__(self.message)


class WrongPath(Exception):

    def __init__(self, message="Não existe esse arquivo ou diretório"):
        self.message = message
        super().__init__(self.message)
