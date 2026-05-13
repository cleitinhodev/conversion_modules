def number_to_string_money(
        value: float,
        minimum: float | int | None = None,
        maximum: float | int | None = None,
        decimal: int = 2,
        coin: str = "$",
        coin_position: str = "first",
        decimal_separator: str = ".",
        thousand_separator: str = ","
) -> str:
    """
    en - Function responsible for converting an integer or floating-point number to
    monetary values customized by the user, inserting separators, currency symbol and
    number of decimal places. Also giving the possibility to select the minimum and maximum quantity
    of the value in question.

    pt-br - Função responsável por realizar conversão de um número inteiro ou de ponto flutuante para
    valores monetários personalizados pelo próprio usuário, inserindo separadores, símbolo da moeda e
    quantidade de casas decimais. Também dando a possibilidade de selecionar quantidade mínima e máxima
    do valor em questão.

    :param value: Value that will be converted to money
        (Valor que será convertido para dinheiro).
    :param minimum: Minimum value allowed
        (Valor mínimo permitido).
    :param maximum: Maximum value allowed
        (Valor máximo permitido).
    :param decimal: Number of decimal places
        (Quantidade de casas decimais).
    :param coin: Currency symbol
        (Símbolo da moeda).
    :param coin_position: Position where the currency symbol should be placed
        ('first' or 'last') Posição onde símbolo da moeda deve ficar ('primeiro' ou 'último').
    :param decimal_separator: Decimal separator when there are cents
        (separador decimal quando houver centavos).
    :param thousand_separator: A thousands separator that scores points every 3 digits
        (separador de milhar que pontua a cada 3 números).
    :return: Returns a String with the converted monetary value. Example: $ 4,321.56
        (Retorna uma String com o valor monetário já convertido. Exemplo: $ 4.321,56).
    """

    ### Verification of entered values (Verificação de valores inseridos)

    if decimal_separator == thousand_separator:
        raise ValueError(
            "Separators should not be identical."
        )

    if coin_position not in ("first", "last"):
        raise ValueError(
            "coin_position must be 'first' or 'last'"
        )

    if not isinstance(decimal, int):
        raise TypeError(
            "decimal must be an integer"
        )

    if decimal < 0:
        raise ValueError(
            "decimal must be >= 0"
        )

    if (
            minimum is not None and
            maximum is not None and
            minimum > maximum
    ):
        raise ValueError(
            "minimum cannot be greater than maximum"
        )

    ### Number validation (Validação de numero)
    try:
        number = float(value)

    except (TypeError, ValueError):
        if coin_position == "first":
            return f"{coin} --{decimal_separator}--"

        return f"--{decimal_separator}-- {coin}"

    ### Validation of permitted amounts (Validação de quantias permitidas)

    if minimum is not None:
        minimum = float(minimum)
        if number < minimum:
            number = minimum

    if maximum is not None:
        maximum = float(maximum)
        if number > maximum:
            number = maximum

    ### Conversion (Conversão)

    format_number = f"{abs(number):,.{decimal}f}"

    format_number = (
        format_number
        .replace(",", "__TEMP__")
        .replace(".", decimal_separator)
        .replace("__TEMP__", thousand_separator)
    )

    signal = "-" if number < 0 else ""

    if coin_position == "first":
        return f"{coin} {signal}{format_number}"

    return f"{signal}{format_number} {coin}"

def string_money_to_number(
        value: str,
        decimal: bool = False
) -> int | float:
    """
    en: It receives a value formatted as a monetary value and attempts to convert it to an
    integer or floating-point number.
    Ex - $ 1,234.56 -> 123456 ou 1234.56

    pt-br: Recebe um valor formatado em forma de dinheiro e tenta converter para número inteiro ou ponto flutuante.
    Ex - R$ 1.234,56 -> 123456 ou 1234.56

    :param value: String value that will be converted. (Valor em string que será convertido.)
    :param decimal: Indicates whether the value includes cents or not. (True: Yes, False: No)
        (Indica se o valor tem centavos ou não. (Verdadeiro: Sim, Falso: Não))
    :return: Returns a converted numeric value (integer, floating-point).
        (Retorna um valor numérico já convertido. (inteiro, ponto-flutuante))
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    if not isinstance(decimal, bool):
        raise TypeError("decimal must be a boolean")

    # Mantém apenas números, ponto e vírgula
    filtered = "".join(c for c in value if c.isdigit() or c in ",.")

    if decimal:

        # Detecta último separador decimal
        last_dot = filtered.rfind(".")
        last_comma = filtered.rfind(",")

        decimal_separator = None

        if last_dot > last_comma:
            decimal_separator = "."
            thousands_separator = ","
        else:
            decimal_separator = ","
            thousands_separator = "."

        filtered = filtered.replace(thousands_separator, "")
        filtered = filtered.replace(decimal_separator, ".")

        try:
            return float(filtered)
        except ValueError:
            return 0.0

    else:
        filtered = "".join(c for c in filtered if c.isdigit())

        try:
            return int(filtered)
        except ValueError:
            return 0

