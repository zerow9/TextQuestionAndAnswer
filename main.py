import reader.docxs as doc
import reader.excel as excel
import reader.tree as f
import reader.mysql as mysql
import reader.tree as tree

# 这是测试一个文件夹里面所有的数据
if __name__ == '__main__':
    files = f.dirs("text")
    for file in files:
        file_name = file.split("\\")[-1]
        trees = None
        if file.endswith(".docx"):
            trees = doc.reader_doc(file)
        if file.endswith(".xls"):
            trees = excel.read_excel(file)
        mysql.ergodic_tree(trees, file_name)

