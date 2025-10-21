# # -*- coding: utf-8 -*-
# Copyright (C) 2025 taboo-hacker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from zipfile import ZipFile

def extract_txt_from_zip(zip_path):
    with (ZipFile(zip_path, 'r') as zip_ref):
        txt_files = [f for f in zip_ref.namelist() if f.endswith('.txt')]
        txt_files.remove("Vip╙├╗º▒╪╢┴.txt")
        if txt_files:
            txt_file = txt_files[0]
            return zip_ref.read(txt_file).decode('gbk')
    return None