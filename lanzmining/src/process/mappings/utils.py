def as_rpattern(kws: list[str]) -> str:
    pattern = r"|".join(f"({kw})" for kw in kws)
    return pattern
