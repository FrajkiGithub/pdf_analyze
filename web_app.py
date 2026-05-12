import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from PIL import Image

def mm_from_pt(pt):
    return round(pt * 25.4 / 72)

def process_files(uploaded_files):
    data = []
    total_area_m2 = 0.0
    total_pages_count = 0

    for file in uploaded_files:
        filename = file.name
        lower_name = filename.lower()

        if lower_name.endswith('.pdf'):
            file_bytes = file.read()
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            num_pages = len(doc)
            total_pages_count += num_pages
            
            for i, page in enumerate(doc, start=1):
                rect = page.rect
                w = mm_from_pt(rect.width)
                h = mm_from_pt(rect.height)
                area = (w * h) / 1000000
                total_area_m2 += area
                
                data.append({
                    "file": filename,
                    "page": i,
                    "total_pages": num_pages,
                    "width_mm": w,
                    "height_mm": h,
                    "width_px": None,
                    "height_px": None,
                    "area_m2": area
                })
            doc.close()

        elif lower_name.endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
            img = Image.open(file)
            width_px, height_px = img.size
            dpi = img.info.get('dpi', (72, 72))
            if dpi[0] == 0 or dpi[1] == 0:
                dpi = (72, 72)
            
            w_mm = round(width_px * 25.4 / dpi[0])
            h_mm = round(height_px * 25.4 / dpi[1])
            area = (w_mm * h_mm) / 1000000
            total_area_m2 += area
            total_pages_count += 1
            
            data.append({
                "file": filename,
                "page": 1,
                "total_pages": 1,
                "width_mm": w_mm,
                "height_mm": h_mm,
                "width_px": width_px,
                "height_px": height_px,
                "area_m2": area
            })

    return data, total_area_m2, total_pages_count

def main():
    st.set_page_config(page_title="Souborový analyzátor", layout="wide")

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden !important; display: none !important;}
                header {visibility: hidden !important; display: none !important;}
                .block-container {padding-top: 0rem !important; padding-bottom: 0rem !important;}
                [data-testid="stMetric"] {text-align: left !important;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Vyberte PDF nebo obrázky (lze nahrát více souborů najednou)", 
        type=["pdf", "png", "jpg", "jpeg", "tif", "tiff"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        with st.spinner('Zpracovávám soubory...'):
            data, total_area, total_pages = process_files(uploaded_files)

        if data:
            df = pd.DataFrame(data)
            
            st.success("Hotovo!")
            
            # Výpočet celkové velikosti souborů v MB
            total_size_bytes = sum(file.size for file in uploaded_files)
            total_size_mb = total_size_bytes / (1024 * 1024)
            
            # Rozvržení metrik vlevo s mezerami (4 údaje a 1 mezera napravo)
            m1, m2, m3, m4, spacer = st.columns([1, 1, 1, 1, 2])
            m1.metric(label="Počet souborů", value=len(uploaded_files))
            m2.metric(label="Počet stran celkem", value=total_pages)
            m3.metric(label="Celková velikost", value=f"{total_size_mb:.2f} MB".replace('.', ','))
            m4.metric(label="Celková plocha", value=f"{total_area:.2f} m²".replace('.', ','))
            
            df_display = df.copy()
            last_file = None
            for i in range(len(df_display)):
                current_file = df_display.at[i, 'file']
                if current_file == last_file:
                    df_display.at[i, 'file'] = ""
                else:
                    last_file = current_file

            # Konfigurace sloupců pro automatické nastavení šířky sloupce file
            st.dataframe(
                df_display, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "file": st.column_config.TextColumn("file", width="large")
                }
            )

            df_csv = df.copy()
            total_row = {"file": "CELKEM", "area_m2": total_area}
            df_csv = pd.concat([df_csv, pd.DataFrame([total_row])], ignore_index=True)
            
            csv_data = df_csv.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')

            st.download_button(
                label="📥 Stáhnout výsledky jako _sizes.csv",
                data=csv_data,
                file_name="_sizes.csv",
                mime="text/csv",
            )

if __name__ == "__main__":
    main()
