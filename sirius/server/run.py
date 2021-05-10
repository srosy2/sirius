from read_data import TextData
from preprocess_words import PrepareText
from predict_topics import ClosenessTermsDocs
import shutil
import os
import pathlib

# file_path = '/home/sirius/Рабочий стол/ontology'
#
# os.chdir(file_path)


def load_term(id):
    main_path = str(pathlib.Path().absolute())#"/home/sirius/DELETEME/sirius/server"
    if id == 1:
        file = 'tpu.txt'
    else:
        file = 'gpn.txt'

    try:
        os.remove('/'.join([main_path, 'termin_train', 'result.txt']))
    except FileNotFoundError:
        pass

    shutil.copy('/'.join([main_path, 'termins', file]), '/'.join([main_path, 'termin_train']))
    os.rename('/'.join([main_path, 'termin_train', file]), '/'.join([main_path, 'termin_train', 'result.txt']))


def read_data(path, type):

    train_data = TextData(path)
    if type == 'txt':
        train_data.get_txt_text()
    else:
        train_data.get_text()

    return train_data.topic_text


def prepare_label(content):
    return [int(text.split('$')[1].strip()) for text in content.split('\n')[:-1]]


def prepare_content(txt, content):
    return {
        txt: '  .  '.join([text.split('$')[0].strip() for text in content.split('\n')])}


def preprocess_label(content, type):
    if type == 'txt':
        label = prepare_label(content['result.txt'])
    else:
        label = list(content.keys())
    return label


def run(doc_path: dict, term_path: dict, id_file):
    print('load content ...')
    load_term(id_file)
    content_text = read_data(term_path['path'], term_path['type_file'])
    content_doc = read_data(doc_path['path'], doc_path['type_file'])
    label = preprocess_label(content_text, term_path['type_file'])
    index = preprocess_label(content_doc, doc_path['type_file'])


    if term_path['type'] == 'term':
        content_text = prepare_content('result.txt', content_text['result.txt'])
    if doc_path['type'] == 'term':
        content_doc = prepare_content('result.txt', content_text['result.txt'])

    print('prepare text ...')
    prepare_text = PrepareText(content_text)
    prepare_text.prepare_text()

    print('prepare doc ...')
    prepare_doc = PrepareText(content_doc)
    prepare_doc.prepare_text()

    print('get doc tokens ...')
    docs = prepare_doc.tokens_part
    termins = prepare_text.tokens_part

    clos_term_doc = ClosenessTermsDocs(termins, docs)

    print('transform docs to vec ...')
    doc_to_vec = clos_term_doc.doc_to_vec(clos_term_doc.docs)
    print('transform terms to vec ...')
    term_to_vec = clos_term_doc.term_to_vec(clos_term_doc.terms)

    print('create closeness array ...')
    clos_array = clos_term_doc.closeness_matrix(doc_to_vec, term_to_vec)

    print('save array ...')
    clos_term_doc.write_array(clos_array, index, label, 'doc_term.csv')


if __name__ == "__main__":
    run({'path': 'train_data', 'type_file': 'doc', 'type': 'doc'}, {'path': 'termin_train',
                                                                    'type_file': 'txt', 'type': 'term'}, 0)
