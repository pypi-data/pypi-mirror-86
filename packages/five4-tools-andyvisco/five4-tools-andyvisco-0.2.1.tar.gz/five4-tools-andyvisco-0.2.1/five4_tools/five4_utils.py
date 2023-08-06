import pandas as pd
import io

class Datos():
    """[summary]
    Clase que Inicializa las funciones
    """
    def __init__(self, dataset) -> str:
        """[summary]

        Args:
            dataset ([csv]): [path al archivo csv a analizar]
        """
        self.dataset = dataset
    
    def analizarDatosNulos(self):
        """[summary]
        El dataset instanciado en la clase Datos(dataset)
        es analizado y retorna distintos metodos de análisis en función
        de los parámetros

        Returns:
            [list]: [tabla con los resultados del análisis]
        """
        try:
            # self.buf = io.StringIO()
            self.datos = self.dataset
            self.df = pd.read_csv(self.dataset)
            self.contador = 0
            self.contadorx = 0
            self.resultado = str()
            # self.info = self.df.info(buf=self.buf)
            # self.resultTable = self.df.values.tolist()
            self.listaDfs = self.df
            dictColumnas = dict()
            
            for columna in self.listaDfs.columns.tolist():
                if int(self.listaDfs[columna].isnull().sum()) is not 0:
                    dictColumnas[columna]=self.listaDfs[columna].isnull().sum()
            sumaNull = sum(dictColumnas.values())

            self.contador+=1
            self.contadorx+=1

            # ax.bar(dictColumnas.keys(), dictColumnas.values(), label='Nulos')

            self.resultado = str(
                "El df tiene {} columnas de las cuales las siguientes tienen valores nulos: {}".format(
                    len(self.listaDfs.columns.tolist()), 
                    # [str(item) for item in listaDfs[dfAnalizar].columns[listaDfs[dfAnalizar].isna().any()].tolist()]
                    str(dictColumnas)
                    )
                )
        except Exception as ex:
            self.resultado = ex.args
            pass
        return self.resultado

        