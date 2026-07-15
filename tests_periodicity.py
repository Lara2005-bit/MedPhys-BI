# Description: This file contains the class to map the periodicity of the tests for each equipment.

class TestsPeriodicity():
    def __init__(self) -> None:
        self.list_tests_gc_periodicity = self._set_gc_tests()
        self.list_tests_pet_periodicity = self._set_pet_tests()
        self.list_tests_curiometro_periodicity = self._set_curiometro_tests()
        self.list_tests_gm_periodicity = self._set_gm_tests()
        self.list_tests_gp_periodicity = self._set_gp_tests()
        
    def _set_gc_tests(self):
        list_tests_gc_periodicity = {
            'Uniformidade intrínseca para alta densidade de contagem': 'Mensal',
            'Resolução e linearidade espacial intrínseca': 'Mensal',
            'Centro de rotação LEHR': 'Mensal',
            'Centro de rotação MEGP': 'Mensal',
            'Centro de rotação HEGP': 'Mensal',
            'Resolução energética Tc-99m': 'Semestral',
            'Resolução energética Tl-201': 'Semestral',
            'Resolução energética Ga-67': 'Semestral',
            'Resolução energética I-131': 'Semestral',
            'Taxa máxima de contagem': 'Semestral',
            'Resolução espacial íntriseca para fontes multi-energética I-131': 'Semestral',
            'Resolução espacial íntriseca para fontes multi-energética Ga-67': 'Semestral',
            'Resolução espacial íntriseca para fontes multi-energética Tl-201': 'Semestral',
            'Corregistro espacial para fontes multi-energéticas Ga-67': 'Semestral',
            'Corregistro espacial para fontes multi-energéticas Tl-201': 'Semestral',
            'Sensibilidade planar Tc-99m': 'Semestral',
            'Sensibilidade planar Ga-67': 'Semestral',
            'Sensibilidade planar I-131': 'Semestral',
            'Sensibilidade planar Tl-201': 'Semestral',
            'Uniformidade extrínseca para alta densidade de contagem LEHR': 'Semestral',
            'Uniformidade extrínseca para alta densidade de contagem MEGP': 'Semestral',
            'Uniformidade extrínseca para alta densidade de contagem HEGP': 'Semestral',
            'Verificação da angulação dos furos LEHR': 'Semestral',
            'Verificação da angulação dos furos MEGP': 'Semestral',
            'Verificação da angulação dos furos HEGP': 'Semestral',
            'Velocidade da mesa em varreduras de corpo inteiro': 'Semestral',
            'Desempenho geral da câmara SPECT': 'Semestral',
            'Uniformidade íntrinseca para I-131': 'Anual',
            'Uniformidade íntrinseca para Ga-67': 'Anual',
            'Uniformidade íntrinseca para Tl-201': 'Anual',
            'Uniformidade intrínseca com janelas energéticas assimétricas': 'Anual',
            'Resolução e linearidade espacial extrínseca LEHR- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca MEGP- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca HEGP- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca LEHR- Quantitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca MEGP- Quantitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca HEGP- Quantitativo': 'Anual',
            'Teste de angulação dos furos (LEHR)': 'Semestral', 
            'Teste de angulação dos furos (HEGP)': 'Semestral', 
            'Teste de angulação dos furos (MEGP)': 'Semestral',
            'Uniformidade com alta densidade de contagens (VENTRI)': 'Mensal'
        }
        return list_tests_gc_periodicity
    
    def _set_pet_tests(self):
        list_tests_pet_periodicity = {
            'Uniformidade e verificação da calibração do sistema PET-CT': 'Mensal',
            'Alinhamento entre sistemas de laser PET/CT':'Sem periodicidade definida',
            'Normalização e calibração cruzada': 'Trimestral',
            'Resolução espacial (transversal e axial)': 'Semestral',
            'Sensibilidade': 'Trimestral',
            'Corregistro das imagens de PET e CT': 'Semestral',
            'Desempenho da taxa de contagens (NECR), taxa de eventos aleatórios, espalhados e verdadeiros, fração de espalhamento e exatidão das correções de eventos aleatórios e de perda de contagens': 'Anual',
            'Desempenho geral e exatidão das correções de atenuação e espalhamento': 'Anual',
            'Atualização dos ganhos': 'Semanal',
            'Atualização da Correção da Sincronização de Coincidência (CTC)': 'Trimestral',
            'Estabelecimento de nova linha de base do PET DQA': 'Trimestral',
            'Fração de espelhamento': 'Anual'
        }
        return list_tests_pet_periodicity
    
    def _set_curiometro_tests(self):
        list_tests_curiometro_periodicity = {
            'Reprodutibilidade': 'Mensal',
            'Precisão e exatidão': 'Semestral',
            'Linearidade F-18': 'Semestral',
            'Linearidade Tc-99m': 'Semestral',
            'Geometria': 'Anual'
        }
        return list_tests_curiometro_periodicity
    
    def _set_gm_tests(self):
        list_tests_gm_periodicity = {
            'Reprodutibilidade': 'Mensal'
        }
        return list_tests_gm_periodicity
    
    def _set_gp_tests(self):
        list_tests_gp_periodicity = {
            'Repetibilidade': 'Semestral'
        }
        return list_tests_gp_periodicity

    def full_list(self):
        return {**self.list_tests_gc_periodicity,
                **self.list_tests_pet_periodicity,
                **self.list_tests_curiometro_periodicity,
                **self.list_tests_gm_periodicity,
                **self.list_tests_gp_periodicity}

    def map_gc_periodicity(self, name):
        return self.list_tests_gc_periodicity[name]

    def map_pet_periodicity(self, name):
        return self.list_tests_pet_periodicity[name]

    def map_curiometro_periodicity(self, name):
        return self.list_tests_curiometro_periodicity[name]

    def map_gm_periodicity(self, name):
        return self.list_tests_gm_periodicity[name]

    def map_gp_periodicity(self, name):
        return self.list_tests_gp_periodicity[name]
