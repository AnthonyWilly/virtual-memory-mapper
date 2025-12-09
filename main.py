def byteCalculator(valueStr):
    valueStr = valueStr.strip().lower()
    units = {"gb": 1024**3, "mb": 1024**2, "kb": 1024, "b": 1}
    
    for unit, multiplier in units.items():
        if valueStr.endswith(unit):
            try:
                number_part = valueStr[:-len(unit)]
                return int(number_part) * multiplier
            except ValueError:
                continue
    try:
        return int(valueStr)
    except ValueError:
        return 0

#Entradas
virtualMemoryStr = "64KB"   # Ex: 64KB de espaço de endereçamento total
physicalMemoryStr = "32KB"  # Ex: 32KB de RAM real
pageSizeStr = "4KB"         # Tamanho da página

# Converter para bytes
virtualMemorySize  = byteCalculator(virtualMemoryStr)
physicalMemorySize = byteCalculator(physicalMemoryStr)
pageSize = byteCalculator(pageSizeStr)

# Calcular quantos Pages e Frames cabem
numPages = virtualMemorySize // pageSize 
numFrames = physicalMemorySize // pageSize
#O sistema considera que as pageframes tem o mesmo tamanho das pages

print(f"---------- Sistema -----------")
print(f"Memória Virtual: {virtualMemorySize} bytes ({numPages} páginas)")
print(f"Memória Física:  {physicalMemorySize} bytes ({numFrames} quadros)")
print(f"Tamanho da Página: {pageSize} bytes")
print("-" * 30)

# Mapeia Page Number : Frame Number 
pageTable = {
    0: 3,
    1: 4,
    2: 1,
    3: None, # Page Fault, não está na memória
    4: 0,
    5: 2,
}

# Validação da Tabela
maxIndexNaTabela = max(pageTable.keys()) if pageTable else 0

if maxIndexNaTabela >= numPages:
    raise Exception(f"ERRO: A tabela define a página {maxIndexNaTabela}, mas o limite é {numPages-1} (total de {numPages} páginas).")

#Lógica da tradução
try:
    input_val = input(f"Endereço virtual (0 - {virtualMemorySize-1}): ")
    virtualAddress = int(input_val)
    
    if virtualAddress >= virtualMemorySize or virtualAddress < 0:
         print(f"ERRO: Endereço fora dos limites da memória virtual.")
    else:
        pageNumber = virtualAddress // pageSize
        offset     = virtualAddress % pageSize

        print(f"Página Virtual: {pageNumber}")
        print(f"Offset: {offset}")

        #Como não tem um kernel implementado, em caso de Page Fault ou Segmentation Fault, se deve mapear o page manualmente na tabela
        if pageNumber not in pageTable:
            print("SEGMENTATION FAULT!.") #Página não alocada na tabela
        elif pageTable[pageNumber] is None:
            print("PAGE FAULT!") # Página não está na memória
        else:
            frameNumber = pageTable[pageNumber]
            physicalAddress = (frameNumber * pageSize) + offset
            print(f"Endereço Físico: {physicalAddress} (Frame: {frameNumber})")

except ValueError:
    print("ERRO: Por favor, digite um número inteiro válido.")
