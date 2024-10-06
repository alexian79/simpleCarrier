import skip
import pandas as pd

if __name__ == "__main__":
    sch = skip.Schematic("JX1.kicad_sch")
    for gl in sch.global_label:
        print(gl.value)
        if gl.value.startswith("JX_"):
            gl.value = "JX1_" + gl.value[3:]
            print(gl.value)
    #quit()
    sch.overwrite()
    