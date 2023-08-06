from CRM_PricingTools.segmentation import SegmentData
from CRM_PricingTools.segmentation_prueba import SegmentData_2
import pandas as pd


class PrintData:
    
    def __init__(self, df) -> None:
        """Contructor

        Args:
            df (DataFrame): Pandas Dataframe
        """

        self.dataframe = df.copy()

    
    def print_uplift_test_canal(self, df):
        """
        Funcion para printear los resultados del uplift en el metodo info_nodo_filtrado() 
        """
        segment_data = SegmentData(df)
        return (str(round(segment_data.calculate_uplift_test_canal(df) * 100, 3)).replace(".",",")+ "%" )

    def print_new_uplift_test_canal(self, df):
        """
        Funcion para printear los resultados del uplift en el metodo info_nodo_filtrado() 
        """
        segment_data = SegmentData_2(df)
        return (str(round(segment_data.calculate_test_canal_otro_uplift(df) * 100, 3)).replace(".",",")+ "%" )

    def print_rate_weight(self, df_filtered, df):
        """
        Funcion para printear el peso de un df filtrado respecto al total correspondiente
        """
        return (str(round(len(df_filtered) / len(df) * 100 ,3)).replace(".",",") + "%")

    def comunicados_canal(df, canal):
        """
        Funcion intermedia para calcular la tasa de respuesta para los dos canales,
        canal: se lo pasamos a los metodos comunicados_sms y comunicados_email dentro de sus propios metodos
        """
        return (str(round(len(df[(df['CANAL_FINAL']==canal) & (df['sn_conv_digital']==1)]) / len(df[df['CANAL_FINAL']==canal]) * 100, 3)).replace(".",",") + "%")

    def calculate_comunicados_sms(self,df):
        """
        Funcion para calcular la tasa de respuesta para el canal de SMS
        """
        return PrintData.comunicados_canal(df, 'SMS')
        
    def calculate_comunicados_email(self,df):
        """
        Funcion para calcular la tasa de respuesta para el canal de email
        """
        return PrintData.comunicados_canal(df, 'EMAILING')

