# Definindo as calculadoras de IMC, TMB e Porcentagem de Gordura
import math
from datetime import datetime

def calculaIMC(peso, altura):
    imc = (peso / (altura ** 2))*10000
    return round(imc, 2)

# fórmula de Harris-Benedict para cálculo de TMB (Taxa Metabólica Basal)
def calculaTMB(peso, altura, idade, sexo, atividade):
    if sexo == "masculino":
        tmb = 66.47 + (13.75 * peso) + (5.0 * altura) - (6.76 * idade)
    else:
        tmb = 655.1 + (9.56 * peso) + (1.85 * altura) - (4.68 * idade)

    if atividade == "Sedentário":
        tmb *= 1.2
    elif atividade == "Atividade Ligeira":
        tmb *= 1.375
    elif atividade == "Atividade Moderada":
        tmb *= 1.55
    elif atividade == "Atividade Intensa":
        tmb *= 1.725
    elif atividade == "Atividade Muito Intensa":
        tmb *= 1.9

    return tmb

# fórmula de estimativa de gordura corporal do Departamento de Defesa dos EUA
def calculaPercentGorduraMASC(alturaCM, cinturaCM, pescocoCM):
    try:
        alturaM = alturaCM / 100
        diferença_cintura_pescoco = cinturaCM - pescocoCM
        
        # Verifica se a diferença é positiva
        if diferença_cintura_pescoco <= 0:
            raise ValueError("A circunferência da cintura deve ser maior que a do pescoço.")
        
        # Calcula a gordura corporal
        gordura_corporal = 86.010 * math.log10(diferença_cintura_pescoco) - 70.041 * math.log10(alturaM) + 36.76
        return round(gordura_corporal / 10, 2)
    
    except ValueError as e:
        # Captura erros específicos relacionados ao cálculo
        print(f"Erro de valor: {e}")
        return None
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"Ocorreu um erro inesperado: {e}")
        return None

def calculaPercentGorduraFem(alturaCM, cinturaCM, pescocoCM, quadrilCM):
    try:
        alturaM = alturaCM / 100
        diferença_cintura_quadril_pescoco = cinturaCM + quadrilCM - pescocoCM
        
        # Verifica se a diferença é positiva
        if diferença_cintura_quadril_pescoco <= 0:
            raise ValueError("A soma da circunferência da cintura e quadril deve ser maior que a do pescoço.")
        
        # Calcula a gordura corporal
        gordura_corporal = 163.205 * math.log10(diferença_cintura_quadril_pescoco) - 97.684 * math.log10(alturaM) - 78.387
        return round(gordura_corporal / 10, 2)
    
    except ValueError as e:
        # Captura erros específicos relacionados ao cálculo
        print(f"Erro de valor: {e}")
        return None
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"Ocorreu um erro inesperado: {e}")
        return None
    
def calcular_idade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    data_atual = datetime.now()
    idade = data_atual.year - data_nascimento.year
    if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade

def classificaIMC(imc):
    if imc < 16.9:
        return "Muito abaixo do peso"
    elif 17 <= imc <= 18.4:
        return "Abaixo do peso"
    elif 18.5 <= imc <= 24.9:
        return "Peso normal"
    elif 25 <= imc <= 29.9:
        return "Acima do peso"
    elif 30 <= imc <= 34.9:
        return "Obesidade grau I"
    elif 35 <= imc <= 40:
        return "Obesidade grau II"
    elif imc > 40:
        return "Obesidade grau III"
    else:
        return "Erro: IMC fora dos limites conhecidos"
    
    

