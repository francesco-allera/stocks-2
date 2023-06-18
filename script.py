import os
import shutil

cartella = os.path.dirname(__file__)
cartella_csv = cartella + '/csv'
cartella_js = cartella + '/js'
nomi_file_csv = []

for nome_file in os.listdir(cartella_csv):
   if os.path.splitext(nome_file)[1] == '.csv':
      nomi_file_csv.append(os.path.splitext(nome_file)[0])

with open('stocks.js', 'w') as file_stocks:
   str = ',\n\t'.join(nomi_file_csv)
   file_stocks.write('const stocks = {\n\t' + str + '\n};')

string_html_stocks = '<script defer src="./stocks.js"></script>'

with open('index.html', 'r') as file_html:
   contenuto_html = file_html.readlines()

   for i, el in enumerate(contenuto_html):
      if '</title>' in el:
         indice_titolo = i
         index_html_title = el
      if 'src="./stocks.js"' in el:
         indice_script_js = i

   contenuto_html = contenuto_html[:indice_titolo + 1] + contenuto_html[indice_script_js:]

   for i, nome in enumerate(nomi_file_csv):
      contenuto_html.insert(indice_titolo + i + 1, f'\t<script defer src="./js/{nome}.js"></script>\n')

with open('index.html', 'w') as file_html:
   file_html.writelines(contenuto_html)

if os.path.exists(cartella_js):
   shutil.rmtree(cartella_js)
os.makedirs('js')

for nome_file in nomi_file_csv:
   with open('./csv/' + nome_file + '.csv', 'r') as file_csv, open('./js/' + nome_file + '.js', 'w') as file_js:
      reverse_file_csv = file_csv.readlines()[1:][::-1]

      file_js.write('const ' + nome_file + ' = [\n')

      for line in reverse_file_csv:
         arr = line.split(',')

         arr[1] = arr[1].replace('$','')
         while arr[1].endswith('0'):
            arr[1] = arr[1][:-1]
         if arr[1].endswith('.'):
            arr[1] = arr[1][:-1]

         date = arr[0].split('/')

         if int(date[2]) < 2014:
            continue

         if date[0].startswith('0'):
            date[0] = date[0][1]
         if date [1].startswith('0'):
            date[1] = date[1][1]

         file_js.write('\t{\n' + '\t\tyy: ' + date[2] + ',\n' + '\t\tmm: ' + date[0] + ',\n' + '\t\tdd: ' + date[1] + ',\n' + '\t\tclose: ' + arr[1] + '\n' + '\t},\n')

      file_js.write('];')
