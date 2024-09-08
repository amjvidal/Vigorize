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
    
    
def classifica_percentual_gordura(percentual_gordura, sexo, idade):
    # Para homens
    if sexo == 'masculino':
        if 20 <= idade <= 29:
            if percentual_gordura < 5.2:
                return "Muito magro"
            elif 5.3 <= percentual_gordura <= 9.3:
                return "Magro"
            elif 9.4 <= percentual_gordura <= 14.0:
                return "Muito bom"
            elif 14.01 <= percentual_gordura <= 17.5:
                return "Saudável"
            elif 17.6 <= percentual_gordura <= 20.6:
                return "Sobrepeso"
            elif 20.7 <= percentual_gordura <= 24.2:
                return "Gordo"
            else:
                return "Muito gordo"
        
        elif 30 <= idade <= 39:
            if percentual_gordura < 9.2:
                return "Muito magro"
            elif 9.3 <= percentual_gordura <= 14.0:
                return "Magro"
            elif 14.1 <= percentual_gordura <= 17.5:
                return "Muito bom"
            elif 17.6 <= percentual_gordura <= 20.6:
                return "Saudável"
            elif 20.7 <= percentual_gordura <= 24.2:
                return "Sobrepeso"
            elif 24.3 <= percentual_gordura <= 29.9:
                return "Gordo"
            else:
                return "Muito gordo"
        
        elif 40 <= idade <= 49:
            if percentual_gordura < 11.5:
                return "Muito magro"
            elif 11.6 <= percentual_gordura <= 16.1:
                return "Magro"
            elif 16.2 <= percentual_gordura <= 18.2:
                return "Muito bom"
            elif 18.3 <= percentual_gordura <= 22.3:
                return "Saudável"
            elif 22.4 <= percentual_gordura <= 24.2:
                return "Sobrepeso"
            elif 24.3 <= percentual_gordura <= 29.9:
                return "Gordo"
            else:
                return "Muito gordo"
        
        elif 50 <= idade <= 59:
            if percentual_gordura < 12.9:
                return "Muito magro"
            elif 13.0 <= percentual_gordura <= 18.1:
                return "Magro"
            elif 18.2 <= percentual_gordura <= 22.0:
                return "Muito bom"
            elif 22.1 <= percentual_gordura <= 25.0:
                return "Saudável"
            elif 25.1 <= percentual_gordura <= 28.4:
                return "Sobrepeso"
            elif 28.5 <= percentual_gordura <= 33.9:
                return "Gordo"
            else:
                return "Muito gordo"
        
        elif idade >= 60:
            if percentual_gordura < 13.0:
                return "Muito magro"
            elif 13.1 <= percentual_gordura <= 18.5:
                return "Magro"
            elif 18.6 <= percentual_gordura <= 22.0:
                return "Muito bom"
            elif 22.1 <= percentual_gordura <= 25.0:
                return "Saudável"
            elif 25.1 <= percentual_gordura <= 28.4:
                return "Sobrepeso"
            elif 28.5 <= percentual_gordura <= 33.9:
                return "Gordo"
            else:
                return "Muito gordo"

    # Para mulheres
    elif sexo == 'feminino':
        if 20 <= idade <= 29:
            if percentual_gordura < 10.7:
                return "Muito magra"
            elif 10.8 <= percentual_gordura <= 17.0:
                return "Magra"
            elif 17.1 <= percentual_gordura <= 20.5:
                return "Muito bom"
            elif 20.6 <= percentual_gordura <= 23.8:
                return "Saudável"
            elif 23.9 <= percentual_gordura <= 27.6:
                return "Sobrepeso"
            elif 27.7 <= percentual_gordura <= 35.5:
                return "Gorda"
            else:
                return "Muito gorda"
        
        elif 30 <= idade <= 39:
            if percentual_gordura < 13.3:
                return "Muito magra"
            elif 13.4 <= percentual_gordura <= 18.4:
                return "Magra"
            elif 18.5 <= percentual_gordura <= 21.4:
                return "Muito bom"
            elif 21.5 <= percentual_gordura <= 24.9:
                return "Saudável"
            elif 25.0 <= percentual_gordura <= 29.6:
                return "Sobrepeso"
            elif 29.7 <= percentual_gordura <= 36.7:
                return "Gorda"
            else:
                return "Muito gorda"
        
        elif 40 <= idade <= 49:
            if percentual_gordura < 16.1:
                return "Muito magra"
            elif 16.2 <= percentual_gordura <= 21.4:
                return "Magra"
            elif 21.5 <= percentual_gordura <= 25.1:
                return "Muito bom"
            elif 25.2 <= percentual_gordura <= 28.3:
                return "Saudável"
            elif 28.4 <= percentual_gordura <= 32.8:
                return "Sobrepeso"
            elif 32.9 <= percentual_gordura <= 36.7:
                return "Gorda"
            else:
                return "Muito gorda"
        
        elif 50 <= idade <= 59:
            if percentual_gordura < 18.8:
                return "Muito magra"
            elif 18.9 <= percentual_gordura <= 25.1:
                return "Magra"
            elif 25.2 <= percentual_gordura <= 29.1:
                return "Muito bom"
            elif 29.2 <= percentual_gordura <= 32.8:
                return "Saudável"
            elif 32.9 <= percentual_gordura <= 36.6:
                return "Sobrepeso"
            elif 36.7 <= percentual_gordura <= 40.5:
                return "Gorda"
            else:
                return "Muito gorda"
        
        elif idade >= 60:
            if percentual_gordura < 19.1:
                return "Muito magra"
            elif 19.2 <= percentual_gordura <= 25.0:
                return "Magra"
            elif 25.1 <= percentual_gordura <= 29.9:
                return "Muito bom"
            elif 30.0 <= percentual_gordura <= 32.8:
                return "Saudável"
            elif 32.9 <= percentual_gordura <= 36.7:
                return "Sobrepeso"
            elif 36.8 <= percentual_gordura <= 40.5:
                return "Gorda"
            else:
                return "Muito gorda"
    
    else:
        return "Erro: sexo desconhecido"

