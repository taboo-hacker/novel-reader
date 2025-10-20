# -*- coding: utf-8 -*-

from zipfile import ZipFile

def extract_txt_from_zip(zip_path):
    with (ZipFile(zip_path, 'r') as zip_ref):
        txt_files = [f for f in zip_ref.namelist() if f.endswith('.txt')]
        txt_files.remove("Vip╙├╗º▒╪╢┴.txt")
        if txt_files:
            txt_file = txt_files[0]
            return zip_ref.read(txt_file).decode('gbk')
    return None