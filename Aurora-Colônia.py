# =============================================================================
# SISTEMA INTELIGENTE DE GERENCIAMENTO — COLÔNIA AURORA SIGER
# Missão: manter a colônia operando de forma autônoma, eficiente e segura.
#
# Conceitos implementados:
#   - Estruturas de dados (listas, dicionários, hierarquias)
#   - Lógica de decisão (if/elif/else encadeado, operadores lógicos)
#   - Modelagem matemática e regressão linear (sem bibliotecas externas)
#   - Análise de eficiência energética
# =============================================================================


# =============================================================================
# SEÇÃO 1 — ESTRUTURAS DE DADOS
# Organização hierárquica de todos os sistemas da colônia.
# =============================================================================

def inicializar_colonia() -> dict:
    """
    Retorna a estrutura hierárquica completa da colônia Aurora Siger.
    Três grandes sistemas: energético, ambiental e operacional.
    """
    return {
        "energetico": {
            "solar": {
                "geracao_atual": 30,
                "status": "ativo",
                "eficiencia": 0.85
            },
            "eolico": {
                "geracao_atual": 15,
                "status": "ativo",
                "eficiencia": 0.78
            },
            "baterias": {
                "carga_atual": 65,
                "capacidade_total": 200,
                "status": "carregando"
            }
        },
        "ambiental": {
            "temperatura_interna": 22,
            "temperatura_externa": -60,
            "velocidade_vento": 11,
            "pressao_atmosferica": 0.6,
            "tempestade_areia": False
        },
        "operacional": {
            "suporte_vida": {
                "oxigenio":      {"nivel": 95, "consumo_hora": 2, "status": "normal"},
                "pressurizacao": {"nivel": 98, "consumo_hora": 3, "status": "normal"},
                "agua":          {"nivel": 80, "consumo_hora": 1, "status": "normal"}
            },
            "habitats": {
                "modulo_a": {"consumo": 12, "status": "ativo", "prioridade": 2},
                "modulo_b": {"consumo":  8, "status": "ativo", "prioridade": 2}
            },
            "laboratorio":  {"consumo": 10, "status": "ativo", "prioridade": 3},
            "comunicacoes": {"consumo":  5, "status": "ativo", "prioridade": 1}
        }
    }


def historico_sensores() -> dict:
    """
    Séries históricas dos últimos 10 ciclos de leitura dos sensores.
    Utilizadas para análise de padrões e regressão linear.
    """
    return {
        "vento":           [6,  7,  8,  9, 10, 11, 12, 13, 14, 15],
        "energia_eolica":  [14, 16, 20, 22, 25, 27, 30, 32, 35, 37],
        "consumo_por_hora":[30, 28, 25, 22, 20, 22, 27, 35, 40, 38],
        "geracao_solar":   [ 0,  0,  5, 15, 28, 35, 38, 30, 18,  5],
        "carga_baterias":  [80, 78, 75, 70, 65, 62, 60, 58, 55, 50]
    }


def calcular_geracao_total(colonia: dict) -> float:
    """Soma a geração de todas as fontes de energia ativas."""
    e = colonia["energetico"]
    geracao = 0.0
    if e["solar"]["status"] == "ativo":
        geracao += e["solar"]["geracao_atual"]
    if e["eolico"]["status"] == "ativo":
        geracao += e["eolico"]["geracao_atual"]
    return geracao


def calcular_consumo_total(colonia: dict) -> float:
    """Percorre a hierarquia e soma o consumo de todos os sistemas ativos."""
    op = colonia["operacional"]
    total = 0.0
    for sistema in op["suporte_vida"].values():
        total += sistema["consumo_hora"]
    for modulo in op["habitats"].values():
        if modulo["status"] == "ativo":
            total += modulo["consumo"]
    if op["laboratorio"]["status"] == "ativo":
        total += op["laboratorio"]["consumo"]
    if op["comunicacoes"]["status"] == "ativo":
        total += op["comunicacoes"]["consumo"]
    return total


def exibir_estado_colonia(colonia: dict) -> None:
    """Imprime o painel de status atual da colônia."""
    print("=" * 55)
    print("        PAINEL DE STATUS — COLÔNIA AURORA SIGER")
    print("=" * 55)

    e = colonia["energetico"]
    print("\n[SISTEMA ENERGÉTICO]")
    print(f"  Solar   : {e['solar']['geracao_atual']} kWh  | Status: {e['solar']['status']}")
    print(f"  Eólico  : {e['eolico']['geracao_atual']} kWh  | Status: {e['eolico']['status']}")
    print(f"  Baterias: {e['baterias']['carga_atual']}%   | Status: {e['baterias']['status']}")

    a = colonia["ambiental"]
    print("\n[SISTEMA AMBIENTAL]")
    print(f"  Temp. interna : {a['temperatura_interna']}°C")
    print(f"  Temp. externa : {a['temperatura_externa']}°C")
    print(f"  Vento         : {a['velocidade_vento']} km/h")
    print(f"  Tempestade    : {'SIM ⚠' if a['tempestade_areia'] else 'Não'}")

    op = colonia["operacional"]
    print("\n[SUPORTE À VIDA]")
    for nome, s in op["suporte_vida"].items():
        print(f"  {nome.capitalize():15}: {s['nivel']}% | {s['status']}")

    geracao = calcular_geracao_total(colonia)
    consumo = calcular_consumo_total(colonia)
    print(f"\n  Geração total : {geracao} kWh")
    print(f"  Consumo total : {consumo} kWh")
    print(f"  Balanço       : {geracao - consumo:+.1f} kWh")
    print("=" * 55)


# =============================================================================
# SEÇÃO 2 — LÓGICA DE DECISÃO
# Regras condicionais para tomada de decisão automática.
# =============================================================================

LIMITES = {
    "energia_critica":    20,
    "energia_baixa":      40,
    "energia_ok":         60,
    "consumo_alto":       50,
    "balanco_excedente":  15,
    "oxigenio_critico":   30,
    "vento_tempestade":   60
}


def classificar_nivel_energia(carga: float) -> str:
    """Classifica o nível da bateria em categorias operacionais."""
    if carga <= LIMITES["energia_critica"]:
        return "CRITICO"
    elif carga <= LIMITES["energia_baixa"]:
        return "BAIXO"
    elif carga <= LIMITES["energia_ok"]:
        return "MODERADO"
    else:
        return "NORMAL"


def analisar_balanco_energetico(geracao: float, consumo: float, carga: float) -> dict:
    """
    Analisa o balanço energético e retorna diagnóstico com alertas e ações.
    Cobre 5 cenários distintos de operação.
    """
    balanco = geracao - consumo
    nivel   = classificar_nivel_energia(carga)
    result  = {"balanco": balanco, "nivel_bateria": nivel, "alertas": [], "acoes": []}

    if balanco < 0 and nivel == "CRITICO":
        result["alertas"].append("🔴 EMERGÊNCIA: consumo supera geração e bateria crítica!")
        result["acoes"].append("Ativar modo de emergência total.")
        result["acoes"].append("Desligar laboratório e habitats não essenciais.")
        result["acoes"].append("Manter apenas suporte à vida e comunicações.")

    elif balanco < 0 and nivel == "BAIXO":
        result["alertas"].append("🟠 ALERTA: consumo maior que geração.")
        result["acoes"].append("Reduzir consumo dos habitats.")
        result["acoes"].append("Suspender laboratório temporariamente.")

    elif balanco >= 0 and nivel == "BAIXO":
        result["alertas"].append("🟡 ATENÇÃO: bateria baixa — carregar com excedente.")
        result["acoes"].append("Direcionar excedente de energia para as baterias.")

    elif balanco > LIMITES["balanco_excedente"]:
        result["alertas"].append("🟢 SUGESTÃO: excedente de energia disponível.")
        result["acoes"].append("Armazenar energia excedente nas baterias.")
        result["acoes"].append("Possível expansão de atividades no laboratório.")

    else:
        result["alertas"].append("✅ Sistema operando dentro dos parâmetros normais.")

    return result


def avaliar_suporte_vida(operacional: dict) -> list:
    """Verifica os níveis críticos do suporte à vida."""
    alertas = []
    for nome, s in operacional["suporte_vida"].items():
        if s["nivel"] <= LIMITES["oxigenio_critico"]:
            alertas.append(f"🔴 CRÍTICO: {nome} em {s['nivel']}% — intervenção imediata!")
        elif s["nivel"] <= 50:
            alertas.append(f"🟠 ATENÇÃO: {nome} em {s['nivel']}% — monitorar.")
    return alertas


def avaliar_condicoes_ambientais(ambiental: dict) -> list:
    """Analisa condições climáticas externas e retorna alertas."""
    alertas = []
    if ambiental["tempestade_areia"]:
        alertas.append("⛈ TEMPESTADE DE AREIA ATIVA — geração solar comprometida.")
        alertas.append("Recolher equipamentos externos imediatamente.")
    if ambiental["velocidade_vento"] >= LIMITES["vento_tempestade"]:
        alertas.append(f"💨 Vento em {ambiental['velocidade_vento']} km/h — risco estrutural.")
    if ambiental["temperatura_interna"] < 18:
        alertas.append(f"🥶 Temp. interna baixa: {ambiental['temperatura_interna']}°C.")
    return alertas


def gerar_relatorio_decisao(colonia: dict, geracao: float, consumo: float) -> None:
    """Integra todas as análises e exibe o relatório de decisões."""
    carga = colonia["energetico"]["baterias"]["carga_atual"]

    print("\n" + "=" * 55)
    print("         RELATÓRIO DE DECISÃO — SISTEMA AURORA")
    print("=" * 55)

    balanco = analisar_balanco_energetico(geracao, consumo, carga)
    print(f"\n[BALANÇO ENERGÉTICO]")
    print(f"  Geração : {geracao} kWh")
    print(f"  Consumo : {consumo} kWh")
    print(f"  Balanço : {balanco['balanco']:+.1f} kWh")
    print(f"  Bateria : {carga}% ({balanco['nivel_bateria']})")
    print("\n  Diagnóstico:")
    for alerta in balanco["alertas"]:
        print(f"    {alerta}")
    if balanco["acoes"]:
        print("\n  Ações recomendadas:")
        for acao in balanco["acoes"]:
            print(f"    → {acao}")

    alertas_vida = avaliar_suporte_vida(colonia["operacional"])
    print(f"\n[SUPORTE À VIDA]")
    if alertas_vida:
        for a in alertas_vida:
            print(f"  {a}")
    else:
        print("  ✅ Todos os sistemas de suporte à vida normais.")

    alertas_amb = avaliar_condicoes_ambientais(colonia["ambiental"])
    print(f"\n[CONDIÇÕES AMBIENTAIS]")
    if alertas_amb:
        for a in alertas_amb:
            print(f"  {a}")
    else:
        print("  ✅ Condições ambientais dentro do esperado.")

    print("=" * 55)


# =============================================================================
# SEÇÃO 3 — PREVISÃO POR REGRESSÃO LINEAR
# Implementação manual do método dos Mínimos Quadrados (sem bibliotecas).
# =============================================================================

def regressao_linear(x: list, y: list) -> tuple:
    """
    Calcula os coeficientes a e b da reta y = a*x + b
    pelo método dos Mínimos Quadrados Ordinários.

        a = (n·Σ(xi·yi) − Σxi·Σyi) / (n·Σxi² − (Σxi)²)
        b = (Σyi − a·Σxi) / n
    """
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Listas com tamanhos incompatíveis ou insuficientes.")

    soma_x  = sum(x)
    soma_y  = sum(y)
    soma_xy = sum(x[i] * y[i] for i in range(n))
    soma_x2 = sum(x[i] ** 2  for i in range(n))

    denom = n * soma_x2 - soma_x ** 2
    if denom == 0:
        raise ValueError("Variação de x é zero — regressão impossível.")

    a = (n * soma_xy - soma_x * soma_y) / denom
    b = (soma_y - a * soma_x) / n
    return a, b


def prever(a: float, b: float, novo_x: float) -> float:
    """Aplica a equação da reta: y = a·x + b"""
    return a * novo_x + b


def calcular_r2(x: list, y: list, a: float, b: float) -> float:
    """
    Coeficiente de determinação R² — mede a qualidade do ajuste.
    R² = 1 indica ajuste perfeito; próximo de 0, modelo fraco.
    """
    media_y     = sum(y) / len(y)
    ss_total    = sum((yi - media_y) ** 2 for yi in y)
    ss_residual = sum((y[i] - prever(a, b, x[i])) ** 2 for i in range(len(x)))
    if ss_total == 0:
        return 1.0
    return 1 - (ss_residual / ss_total)


def analisar_previsoes(historico: dict, vento_futuro: float, hora_futura: int) -> None:
    """
    Executa três previsões por regressão linear e exibe os resultados
    com balanço energético estimado para o período futuro.
    """
    print("\n" + "=" * 55)
    print("         MÓDULO DE PREVISÃO — REGRESSÃO LINEAR")
    print("=" * 55)

    # Previsão 1: Energia eólica × Velocidade do vento
    x1, y1   = historico["vento"], historico["energia_eolica"]
    a1, b1   = regressao_linear(x1, y1)
    r2_1     = calcular_r2(x1, y1, a1, b1)
    prev_eol = prever(a1, b1, vento_futuro)

    print(f"\n[PREVISÃO 1 — Energia Eólica]")
    print(f"  Equação : energia = {a1:.2f} × vento + {b1:.2f}")
    print(f"  R²      : {r2_1:.4f}")
    print(f"  Vento   : {vento_futuro} km/h → Previsão: {prev_eol:.1f} kWh")

    # Previsão 2: Consumo × Hora do dia
    x2, y2    = list(range(len(historico["consumo_por_hora"]))), historico["consumo_por_hora"]
    a2, b2    = regressao_linear(x2, y2)
    r2_2      = calcular_r2(x2, y2, a2, b2)
    prev_cons = max(prever(a2, b2, hora_futura), 0)

    print(f"\n[PREVISÃO 2 — Consumo por Hora]")
    print(f"  Equação : consumo = {a2:.2f} × hora + {b2:.2f}")
    print(f"  R²      : {r2_2:.4f}")
    print(f"  Hora    : {hora_futura} → Previsão: {prev_cons:.1f} kWh")

    # Previsão 3: Geração Solar × Hora do dia
    x3, y3     = list(range(len(historico["geracao_solar"]))), historico["geracao_solar"]
    a3, b3     = regressao_linear(x3, y3)
    r2_3       = calcular_r2(x3, y3, a3, b3)
    prev_solar = max(prever(a3, b3, hora_futura), 0)

    print(f"\n[PREVISÃO 3 — Geração Solar]")
    print(f"  Equação : solar = {a3:.2f} × hora + {b3:.2f}")
    print(f"  R²      : {r2_3:.4f}")
    print(f"  Hora    : {hora_futura} → Previsão: {prev_solar:.1f} kWh")

    # Síntese do balanço previsto
    geracao_prev = max(prev_eol, 0) + prev_solar
    balanco_prev = geracao_prev - prev_cons

    print(f"\n[SÍNTESE — Balanço Previsto para hora {hora_futura}]")
    print(f"  Geração estimada : {geracao_prev:.1f} kWh")
    print(f"  Consumo estimado : {prev_cons:.1f} kWh")
    print(f"  Balanço previsto : {balanco_prev:+.1f} kWh")

    if balanco_prev < 0:
        print("  ⚠ Déficit previsto — preparar contingência energética.")
    elif balanco_prev > 15:
        print("  💡 Excedente previsto — planejar armazenamento nas baterias.")
    else:
        print("  ✅ Equilíbrio energético previsto.")

    print("=" * 55)


# =============================================================================
# SEÇÃO 4 — PONTO DE ENTRADA
# Orquestra o fluxo completo: dados → estado → decisão → previsão
# =============================================================================

def executar_ciclo(vento_previsto: float = 13.0, hora_prevista: int = 8) -> None:
    """Executa um ciclo completo de análise e decisão da colônia."""
    colonia   = inicializar_colonia()
    historico = historico_sensores()
    geracao   = calcular_geracao_total(colonia)
    consumo   = calcular_consumo_total(colonia)

    exibir_estado_colonia(colonia)
    gerar_relatorio_decisao(colonia, geracao, consumo)
    analisar_previsoes(historico, vento_previsto, hora_prevista)


if __name__ == "__main__":
    print("\n🚀 INICIANDO SISTEMA DE GERENCIAMENTO — AURORA SIGER\n")
    executar_ciclo(vento_previsto=13.0, hora_prevista=8)

    # Descomente para testar cenários alternativos:
    # executar_ciclo(vento_previsto=5.0,  hora_prevista=2)   # noite, vento fraco
    # executar_ciclo(vento_previsto=20.0, hora_prevista=5)   # vento forte, madrugada
