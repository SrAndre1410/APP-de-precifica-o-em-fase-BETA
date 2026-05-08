def calcular_preco(custo_ingredientes, embalagem, mao_obra, margem_lucro):
    custo_total = custo_ingredientes + embalagem + mao_obra

    lucro = custo_total * (margem_lucro / 100)

    preco_venda = custo_total + lucro

    return custo_total, lucro, preco_venda