import os
import fitz  # PyMuPDF

# import io
# from PIL import Image


input_path = 'PDFs'
output_path = 'Texts'
os.makedirs(output_path, exist_ok=True)

folders = [os.path.join(input_path, name) for name in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, name))]

for folder in folders:
    current_output_path = os.path.join(output_path, folder)
    os.makedirs(current_output_path)
    
    print(f"Subcarpeta: {folder}")
    
    pdf_files = [file for file in os.listdir(folder) if file.endswith('.pdf')]
    
    for file in pdf_files:
        pdf_path = os.path.join(folder, file)
        print(f" - Archivo PDF: {pdf_path}")

        doc = fitz.open(pdf_path)

        text = ''
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text("text")  # Modo de extracción de texto
            print(f"Texto de la página {page_num + 1}:\n{text}\n")

        # Crear un objeto file para escribir en el archivo
        file = open(f'{current_output_path}/{file}.txt', 'w')

        # Escribir texto en el archivo
        file.write(text)

        # Cerrar el archivo
        file.close()

        # # Abre el PDF
        # pdf_path = "tu_documento.pdf"
        # doc = fitz.open(pdf_path)

        # # Recorre cada página
        # for page_num in range(doc.page_count):
            # page = doc[page_num]
            # images = page.get_images(full=True)  # Extrae todas las imágenes

            # # Procesa cada imagen
            # for img_index, img in enumerate(images):
                # xref = img[0]
                # base_image = doc.extract_image(xref)
                # image_bytes = base_image["image"]
                # image_ext = base_image["ext"]
                # image_rect = page.get_image_rects(xref)[0]  # Rectángulo de la imagen

                # # Extrae la imagen
                # image = Image.open(io.BytesIO(image_bytes))
                # image.save(f"pagina_{page_num + 1}_imagen_{img_index + 1}.{image_ext}")

                # # Intenta extraer el texto cercano
                # # Filtra los bloques de texto que están cerca de la imagen
                # text_near_image = ""
                # for block in page.get_text("blocks"):
                    # block_rect = fitz.Rect(block[:4])
                    # if block_rect.intersects(image_rect):
                        # text_near_image += block[4] + " "

                # print(f"Imagen en la página {page_num + 1}, imagen {img_index + 1}: Descripción potencial -> {text_near_image.strip()}")
