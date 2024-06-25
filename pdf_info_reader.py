import os
import PyPDF2
import csv
from tqdm import tqdm

# Aby zainstalować wszystkie wymagane biblioteki: pip install -r <sciezka_do_folderu>\requirements.txt
# Pasek postępu będzie pokazywał procent ukończonej pracy.
# Na linijce 75 zaczyna się funkcja odpowiadająca za zczytywanie z CSV, możliwe że będzie potrzeba dostosować lub całkowicie usunąć.

# Folder z plikami pdf:
folder_path = 'D:\\User\\folder_z_pdf' # Wstawiając ścieżkę np: 'folder\plik.pdf' - trzeba ręcznie zmienić na: 'folder/plik.pdf' 
# Plik csv z UUiD szukanych plików:
csvUUiD = 'D:\\User\\plikzUUiD.csv'
# Plik csv do którego będą zapisywane informacje:
output_file = 'D:\\User\\plik_z_wynikami.csv'

def extract_signature_info(fields):
    '''Zczytywanie informacji na temat podpisu - Czy jest, a jeżeli jest to czy z profilu zaufanego czy certyfikowany'''
    if fields:
        for _, field_info in fields.items():
            if field_info.get('/FT') == '/Sig':
                sign_type = 'profil_zaufany' if "podpisu zaufanego" in str(field_info.get('/V', {})) else 'certyfikowany'            
                return True, sign_type         
    return False, '' 

def extract_orientation(page_info):
    '''Zczytywanie orientacji pdf'a vertical/horizontal'''
    rotation = page_info.get('/Rotate',0)
    return 'vertical' if rotation in [0, 180] else 'horizontal'

def extract_form_info(pdf_reader):
    '''Zczytywanie informacji na temat formularza - czy jest formularzem i czy zablokowany'''
    try:
        acro_form_obj = pdf_reader.trailer['/Root']['/AcroForm']
        form_fields = acro_form_obj['/Fields']
        form = any(field.get_object().get('/FT') != '/Sig' for field in form_fields)
        if form:
            fields_obj = form_fields[0].get_object()
            form_state = 'zablokowany' if fields_obj.get('/Ff', 0) & 0x1 else 'otwarty'
        else:
            form_state = ''
        return form, form_state
    except KeyError:
        return False, ''

def process_pdf(file_path, filename):
    '''Sprawdza czy plik jest zaszyfrowany i ściąga wszystkie informacje'''
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if pdf_reader.is_encrypted:
                return [filename, '', '', '', '', '', '', 'Błąd: Plik chroniony hasłem']
            else:
                form, form_state = extract_form_info(pdf_reader)
                sign, sign_type = extract_signature_info(pdf_reader.get_fields())
                num_pages = len(pdf_reader.pages)
                orientation = extract_orientation(pdf_reader.pages[0])
                return [filename, num_pages, orientation, form, form_state, sign, sign_type, '']
    except Exception as e:
        return [filename, '', '', '', '', '', '', f'Błąd: {str(e)}']
    
def get_pdf_info(folder_path, pdf_id_set):
    '''Ściąga listę plików pdf z wybranego folderu, sprawdza czy nazwy plików są w csv i używa funkcji process_pdf w celu uzyskania informacji o plikach'''
    pdf_info = []
    files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    for filename in tqdm(files, desc="Pasek postępu"):
        file_path = os.path.join(folder_path, filename)
        if filename in pdf_id_set:
            pdf_info.append(process_pdf(file_path, filename))
        else:
            pdf_info.append([filename, '', '', '', '', '', '', 'Brak pliku o takim UUiD'])
    return pdf_info

def read_pdf_uuids(csv_filename):
    '''Zczytywanie nazw plików pdf z pliku csv'''
    with open(csv_filename, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',') # Zczytuje z CSV, w której kolumny są rozdzielone przecinkami
        next(csv_reader) # Pomija pierwszy wiersz - zakłada, że istnieją nazwy kolumn
        return {row[2].replace('"', '') for row in csv_reader} # Zakłada, że UUiD znajduje się w 3 kolumnie pliku csv

if __name__ == '__main__':
    pdf_UUiDs = read_pdf_uuids(csvUUiD)
    pdf_info = get_pdf_info(folder_path, pdf_UUiDs)

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['UUID', 'LiczbaStron', 'OrientacjaV', 'CzyFormularz', 'StatusFormularza', 'Podpis', 'TypPodpisu', 'Błąd'])
        for info in pdf_info:
            writer.writerow(info)