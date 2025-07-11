from pynput import keyboard

# Konstantaĵoj
MAPAĴOJ = {
    "cx": "ĉ",
    "gx": "ĝ",
    "hx": "ĥ",
    "jx": "ĵ",
    "sx": "ŝ",
    "ux": "ŭ",
    "Cx": "Ĉ",
    "Gx": "Ĝ",
    "Hx": "Ĥ",
    "Jx": "Ĵ",
    "Sx": "Ŝ",
    "Ux": "Ŭ",
}
KLAVAR_KONTROLILO = keyboard.Controller()

# Helpanta[j] variablo[j]
tajpitaj_literoj: str = ""


def _ricevu_mapaĵo() -> str | None:
    """
    Ĉi tiu metodo simple revenigas mapadon, bazitan sur la lastaj tajpitaj literoj en tajpitaj_literoj. Ekz.:
    "suficx" -> "ĉ"
    "teksto" -> None
    "Hx"     -> "Ĥ"
    La rezulto baziĝas sur la mapado trovita en la dikto MAPAĴOJ supre.
    """
    global tajpitaj_literoj, MAPAĴOJ

    # Kontrolu ĉu ni havas almenaŭ du aliajn literojn skribitajn antaŭe
    if len(tajpitaj_literoj) < 1:
        return None

    # Akiru la mapaĵon
    for key in MAPAĴOJ:
        if tajpitaj_literoj.endswith(key):
            return MAPAĴOJ.get(key, None)

    # Se nenio valida estis trovita, revenigu None
    return None


def on_press(key) -> None:
    """
    Ĉi tiu metodo estas vokita tuj kiam la uzanto premas klavon.
    Ĝi faras la jenajn aferojn:
    1. Ricevas uzantajn enigojn
    2. Aktualigas la tajpitaj_literoj literaron, donita nova vorto, ĝi estos purigita
    3. Akiras eblan Esperantan literon
    4. Skribas la Esperantan literon
    """
    global tajpitaj_literoj, KLAVAR_KONTROLILO
    # Traktas uzantajn enigojn
    try:
        litero = key.char
    except:
        if str(key) != "Key.space":
            return
        litero = " "

    # Aktualigu tajpitaj_literoj
    if litero == " ":
        ## Purigu la registritajn klavojn kaj revenu, tuj kiam ni havas novan vorton
        tajpitaj_literoj = ""
        return
    ## Aldonu al la listo de tajpitaj literoj
    if tajpitaj_literoj == None:
        return
    try:
        tajpitaj_literoj += litero
    except TypeError:
        # This error occurs when we hit Shift+Tab for instance
        # If it occurs, we do not want to crash, but simply continue
        # the execution
        pass

    # Akiru eblan Esperantan karakteron por skribi
    esperanta_teksto = _ricevu_mapaĵo()
    if esperanta_teksto == None:
        return

    # Skribu Esperantan literon
    KLAVAR_KONTROLILO.tap(keyboard.Key.backspace)
    KLAVAR_KONTROLILO.tap(keyboard.Key.backspace)
    KLAVAR_KONTROLILO.tap(esperanta_teksto)


def ĉef():
    with keyboard.Listener(on_press=on_press) as aŭskultilo:
        aŭskultilo.join()


if __name__ == "__main__":
    ĉef()
