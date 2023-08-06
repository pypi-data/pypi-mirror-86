def _buscarSeparador(ds):
    lstSeparadores = [',', ';', ' ', '.']
    _file = ""
    _separadores = {}
    _separadoresSort = []
    _separadorReturn = ""
    try:
        with open(ds, encoding="utf8") as f:
            _file = f.read()
            for separador in lstSeparadores:
                _separadores[str(separador)] = len(_file.split(str(separador)))
            _separadoresSort = sorted(_separadores.values(), reverse=True)[0]
            for elemento, valor in _separadores.items():
                if valor == _separadoresSort:
                    _separadorReturn = elemento
        return _separadorReturn
    except Exception as ex:
        return False


def buscarSeparadorAuto(ds):
    return True