def checker(bytes_chain: bytes, ratio: float = 0.25, print_stat: bool = False) -> bool:
    """
    This test gonna check if the bytes input are readable by Humain
    Args:
        bytes_chain (bytes): The bytes to check
        ratio (float): Return True if the most significant bit ratio is under ration
        print_stat (bool): If True print the percent

    Returns:
        bool: True if bytes input are readable by Humain else False
    """
    header = [1 for byte in bytes_chain if byte > 127]
    internal_ratio = len(header) / len(bytes_chain)
    if print_stat:
        print(internal_ratio)
    if internal_ratio <= ratio:
        return True


def get_ascii_stat(bytes_chain: bytes) -> float:
    """
    This test gonna check if the bytes input are readable by Humain
    Args:
        bytes_chain (bytes): The bytes to check
        ratio (float): Return True if the most significant bit ratio is under ration
        print_stat (bool): If True print the percent

    Returns:
        bool: True if bytes input are readable by Humain else False
    """
    header = [1 for byte in bytes_chain if byte > 31 and byte < 127]
    return len(header) / len(bytes_chain)


def ascii_stoper(bytes_chain: bytes, ratio: float = 0.75, print_stat: bool = False) -> bool:
    """
    This test gonna check if the bytes input are readable by Humain
    Args:
        bytes_chain (bytes): The bytes to check
        ratio (float): Return True if the most significant bit ratio is under ration
        print_stat (bool): If True print the percent

    Returns:
        bool: True if bytes input are readable by Humain else False
    """
    header = [1 for byte in bytes_chain if byte > 31 and byte < 127]
    internal_ratio = len(header) / len(bytes_chain)
    if print_stat:
        print(internal_ratio)
    if internal_ratio >= ratio:
        return True