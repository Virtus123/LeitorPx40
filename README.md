# Leitor Px40

Driver Windows em Python que lê dados de um leitor **RFID/Arduino via porta serial** e injeta o valor como entrada de teclado — útil para integrar leitores de cartão/tag com sistemas que não possuem SDK nativo.

## Como funciona

1. Detecta automaticamente a porta serial do Arduino (CH340/USB)
2. Lê linhas no formato `DECIMAL:12345`
3. Digita o valor no campo ativo do Windows (com Enter opcional)
4. Roda na bandeja do sistema (system tray)

## Requisitos

- Windows 10+
- Python 3.10+
- Leitor/Arduino enviando dados seriais a 115200 baud

## Instalação

```bash
pip install pyserial pystray pillow keyboard
```

## Uso

```bash
python px40driver.pyw
```

O ícone aparece na bandeja. Para encerrar, clique com o botão direito → **Sair**.

## Configuração

Edite as constantes no início de `px40driver.pyw`:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `BAUDRATE` | `115200` | Velocidade serial |
| `SERIAL_KEYWORD` | `DECIMAL:` | Prefixo da linha lida |
| `AUTO_ENTER` | `True` | Pressiona Enter após digitar |

## Autor

[Vitor Yuri Fernandes](https://github.com/Virtus123)
