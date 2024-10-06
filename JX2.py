import skip
import pandas as pd

def strip_column_names(table, extra_rename_mapping={}):
    rename_mapping = {}
    for col_name in table.columns:
        print(col_name)
        rename_mapping[col_name] = col_name.strip()
    table.rename(columns=rename_mapping, inplace=True)
    table.rename(columns=extra_rename_mapping, inplace=True)

if __name__ == "__main__":
    sch = skip.Schematic("JX2.kicad_sch")
    print(dir(sch))
    #print(sch.symbol.JX2)
    pinout_file = "../AES-ZU3EGES-1-SOM-G-pinout.xlsx"
    table = pd.read_excel(pinout_file, sheet_name=1)
    #print(table.columns)
    strip_column_names(table, {"JX2 Pin Number" : "JX2 row1", "Unnamed: 3" : "JX2 row2"})
    #print(table.columns)
    df_jx2_row1 = pd.DataFrame({
        "JX2 pin" : table["JX2 row1"][:70].astype(dtype=int),
        "Zynq": table["Zynq Pin Number"][:70],
        "Net name": table["UltraZed-EG Net Name"][:70]
    })
    df_jx2_row2 = pd.DataFrame({
        "JX2 pin" : table["JX2 row2"][:70].astype(dtype=int),
        "Zynq": table["Zynq Pin Number.1"][:70],
        "Net name": table["UltraZed-EG Net Name.1"][:70]
    })
    #print(df_jx2_row1)
    #print(df_jx2_row2)

    print(dir(sch.global_label))
    #glabel = sch.global_label.new()
    #print(dir(glabel))
    #glabel.move(100, 100)
    #sch.overwrite()
    for df in (df_jx2_row1, df_jx2_row2):
        for index, row in df.iterrows():
            pin_n, _, net = row
            #print(pin, net)
            glabel = sch.global_label.new()
            pin = sch.symbol.JX2.pin["n%i"%pin_n]
            print(pin.location.value)
            x, y, rot = pin.location.value
            if pin_n < 70:
                glabel.move(x-20, y)
            else:
                glabel.move(x+20, y, 0)
                #glabel.move(x+20, y, 180)
            print(glabel.at)
            glabel.value = net
            kwire = sch.wire.new()
                
            # start it on the location of the K pin, using named attribs here
            kwire.start_at(pin)
            kwire.end_at(glabel)
    sch.overwrite()
    