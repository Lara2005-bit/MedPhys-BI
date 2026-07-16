# Description: This file contains the class to map the periodicity of the tests for each equipment.

class TestsPeriodicity():
    def __init__(self) -> None:
        self.list_tests_gcventri_periodicity = self._set_gcventri_tests()
        self.list_tests_gcinfinia_periodicity = self._set_gcinfinia_tests()
        self.list_tests_gcdiscovery_periodicity = self._set_gcdiscovery_tests()
        self.list_tests_pet_periodicity = self._set_pet_tests()
        self.list_tests_curiometro_periodicity = self._set_curiometro_tests()
        self.list_tests_gm_periodicity = self._set_gm_tests()
        self.list_tests_ct_periodicity = self._set_ct_tests()
        self.list_tests_gp_periodicity = self._set_gp_tests()
        
    def _set_gcventri_tests(self):
        list_tests_gcventri_periodicity = {
            'Resolução e linearidade espacial intrínsecas': 'Mensal',
            'Centro de rotção (COR)': 'Mensal',
            'Uniformidade com alta densidade de contagens': 'Mensal',
            'Resolução energética (Tc-99m)': 'Semestral',
            'Resolução energética (Tl-201)': 'Semestral',
            'Taxa de máxima contagem': 'Semestral',
            'Resolução íntrinseca para fontes multi-energéticas(Tl-201)': 'Semestral',
            'Co-registro espacial para fontes multi-energéticas (Tl-201)': 'Semestral',
            'Teste de angulação dos furos': 'Semestral',
            'Sensibilidade (Tc-99m)': 'Semestral',
            'Sensibilidade (Ga-67)': 'Semestral',
            'Uniformidade extrínseca': 'Semestral',
            'Desempenho geral SPECT': 'Semestral',
            'Uniformidade para radionuclídeos diferentes de TC-99m (Tl-201)': 'Anual',
            'Janelas energéticas assimétricas': 'Anual',
            'Resolução e linearidade espacial extrínsecas- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínsecas- Quantitativo': 'Anual'
        }
        return list_tests_gcventri_periodicity

    def _set_gcinfinia_tests(self):
        list_tests_gcinfinia_periodicity = {
            'Resolução e linearidade espacial intrínsecas': 'Mensal',
            'COR (LEHR)': 'Mensal',
            'COR (HEGP)': 'Mensal',
            'COR (MEGP)': 'Mensal',
            'Uniformidade com alta densidade de contagens': 'Mensal',
            'Resolução energética (Tc-99m)': 'Semestral',
            'Resolução energética (Tl-201)': 'Semestral',
            'Resolução energética (Ga-67)': 'Semestral',
            'Resolução energética (I-131)': 'Semestral',
            'Taxa máxima de contagem': 'Semestral',
            'Resolução instrínseca para fontes multi-energéticas (I-131)': 'Semestral',
            'Resolução intrínseca para fontes multi-energéticas (Ga-67)': 'Semestral',
            'Resolução intrínseca para fontes multi-energéticas (Tl-201)': 'Semestral',
            'Co-registro espacial para fontes multi-energéticas (Ga-67)': 'Semestral',
            'Co-registro espacial para fontes multienergéticas (Tl-201)': 'Semestral',
            'Teste de angulação dos furos (LEHR)': 'Semestral',
            'Teste de angulação dos furos (HEGP)': 'Semestral',
            'Teste de angulação dos furos (MEGP)': 'Semestral',
            'Sensibilidade (Tc-99m)': 'Semestral',
            'Sensibilidade (Ga-67)': 'Semestral',
            'Sensibilidade (I-131)': 'Semestral',
            'Uniformidade extrínseca (LEHR)': 'Semestral',
            'Uniformidade extrínseca (HEGP)': 'Semestral',
            'Uniformidade extrínseca (MEGP)': 'Semestral',
            'Velocidade da mesa': 'Semestral',
            'Desempenho geral SPECT': 'Semestral',
            'Uniformidade para radionuclídeos diferentes de Tc-99m (I-131)': 'Anual',
            'Uniformidade para radionuclídeos diferentes de Tc-99m (Ga-67)': 'Anual',
            'Uniformidade para radionuclídeos diferentes de Tc-99m (Tl-201)': 'Anual',
            'Janelas energéticas assimétricas': 'Anual',
            'Resolução e linearidade espacial extrínsecas (LEHR)- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínsecas (HEGP)- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca (MEGP)- Qualitativo': 'Anual',
            'Resoução e linearidade espacial extrínseca (LEHR)- Quantitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca (HEGP)- Quantitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca (MEGP)- Quantitativo': 'Anual'
        }
        return list_tests_gcinfinia_periodicity

    def _set_gcdiscovery_tests(self):
        list_tests_gcdiscovery_periodicity = {
            'Resolução e linearidade espacial intrínsecas': 'Mensal',
            'COR (LEHR)': 'Mensal',
            'COR (HEGP)': 'Mensal',
            'COR (MEGP)': 'Mensal',
            'Uniformidade com alta densidade de contagens': 'Mensal',
            'Resolução energética (Tc-99m)': 'Semestral',
            'Resolução energética (Tl-201)': 'Semestral',
            'Resolução energética (Ga-67)': 'Semestral',
            'Resolução energética (I-131)': 'Semestral',
            'Taxa máxima de contagem': 'Semestral',
            'Resolução instrínseca para fontes multi-energéticas (I-131)': 'Semestral',
            'Resolução intrínseca para fontes multi-energéticas (Ga-67)': 'Semestral',
            'Resolução intrínseca para fontes multi-energéticas (Tl-201)': 'Semestral',
            'Co-registro espacial para fontes multi-energéticas (Ga-67)': 'Semestral',
            'Co-registro espacial para fontes multienergéticas (Tl-201)': 'Semestral',
            'Teste de angulação dos furos (LEHR)': 'Semestral',
            'Teste de angulação dos furos (HEGP)': 'Semestral',
            'Teste de angulação dos furos (MEGP)': 'Semestral',
            'Sensibilidade (Tc-99m)': 'Semestral',
            'Sensibilidade (Ga-67)': 'Semestral',
            'Sensibilidade (I-131)': 'Semestral',
            'Uniformidade extrínseca (LEHR)': 'Semestral',
            'Uniformidade extrínseca (HEGP)': 'Semestral',
            'Uniformidade extrínseca (MEGP)': 'Semestral',
            'Velocidade da mesa': 'Semestral',
            'Desempenho geral SPECT': 'Semestral',
            'Uniformidade para radionuclídeos diferentes de Tc-99m (I-131)': 'Anual',
            'Uniformidade para radionuclídeos diferentes de Tc-99m (Ga-67)': 'Anual',
            'Uniformidade para radionuclídeos diferentes de Tc-99m (Tl-201)': 'Anual',
            'Janelas energéticas assimétricas': 'Anual',
            'Resolução e linearidade espacial extrínsecas (LEHR)- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínsecas (HEGP)- Qualitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca (MEGP)- Qualitativo': 'Anual',
            'Resoução e linearidade espacial extrínseca (LEHR)- Quantitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca (HEGP)- Quantitativo': 'Anual',
            'Resolução e linearidade espacial extrínseca (MEGP)- Quantitativo': 'Anual'
        }
        return list_tests_gcdiscovery_periodicity
    
    def _set_pet_tests(self):
        list_tests_pet_periodicity = {
            'Atualização do ganho': 'Semanal',
            'Uniformidade/Verificação da calibração do sistema': 'Mensal',
            'Atualização da correção da sincronização de coincidência (CTC)': 'Trimestral',
            'Calibração cruzada e Normalização (PET 3D WCC)': 'Trimestral',
            'Estabelecimento  de nova linha de base do PET DQA': 'Trimestral',
            'Sensibilidade': 'Trimestral',
            'Corregistro PET-CT': 'Trimestral',
            'Resolução espacial (tranversal e axial)': 'Semestral',
            'Fração de espalhamento': 'Anual',
            'Desempenho da taxa de contagem (NECR)': 'Anual',
            'Taxa de eventos verdadeiros, aleatórios e espalhados': 'Anual',
            'Acurácia: Exatidão nas correções de perda de contagens e eventos aleatórios': 'Anual',
            'Desempenho geral do sistema e Exatidão das correções de espalhamento e atenuação': 'Anual'
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

    def _set_ct_tests(self):
        list_tests_ct_periodicity = {
            'Valores, Uniformidade e Ruído dos nº CT': 'Semanal',
            'Resolução espacial': 'Anual',
            'Avaliação da resolução de baixo contraste em TC': 'Anual',
            'Verificação de ausência de artefatos na imagem': 'Anual',
            'Exatidão do indicador da tensão do tubo': 'Anual',
            'Exatidão do indicador do deslocamento da mesa': 'Anual',
            'Coincidência entre os indicadores luminosos': 'Anual',
            'Alinhamento entre os sistemas de Lasers (externo e do PET-CT)*': 'Anual',
            'Exatidão da espessura do corte': 'Anual',
            'Compensação dos sistemas de modulação de corrente para diferentes espessuras': 'Anual',
            'Valores representativos de dose': 'Anual',
            'Exatidão do indicador de dose em CT': 'Anual',
            'Levantamento radiométrico': 'Quadrienal'
        }
        return list_tests_ct_periodicity
    
    def _set_gp_tests(self):
        list_tests_gp_periodicity = {
            'Repetibilidade': 'Semestral'
        }
        return list_tests_gp_periodicity

    def full_list(self):
        return {**self.list_tests_gcventri_periodicity,
                **self.list_tests_gcinfinia_periodicity,
                **self.list_tests_gcdiscovery_periodicity,
                **self.list_tests_pet_periodicity,
                **self.list_tests_curiometro_periodicity,
                **self.list_tests_gm_periodicity,
                **self.list_tests_ct_periodicity,
                **self.list_tests_gp_periodicity}

    def map_gcventri_periodicity(self, name):
        return self.list_tests_gcventri_periodicity[name]

    def map_gcinfinia_periodicity(self, name):
        return self.list_tests_gcinfinia_periodicity[name]
        
    def map_gcdiscovery_periodicity(self, name):
        return self.list_tests_gcdiscovery_periodicity[name]
        
    def map_pet_periodicity(self, name):
        return self.list_tests_pet_periodicity[name]

    def map_curiometro_periodicity(self, name):
        return self.list_tests_curiometro_periodicity[name]

    def map_gm_periodicity(self, name):
        return self.list_tests_gm_periodicity[name]

    def map_ct_periodicity(self, name):
        return self.list_tests_ct_periodicity[name]

    def map_gp_periodicity(self, name):
        return self.list_tests_gp_periodicity[name]
