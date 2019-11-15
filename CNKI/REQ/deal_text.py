raw_file = open('./cnki_data.txt', mode='r+', encoding='utf-8')
new_file = open('./cnki_full.txt', mode='w+', encoding='utf-8')
new_file.write("kw\tc_no\tname\tinventor\tapplicant\tsource_from\tapply_date\tpub_date\tlink\n")

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        data = eval(line.replace("\n", ""))
        kw = data['kw']
        c_no = data['c_no']
        name = data['name']
        inventor = data['inventor']
        applicant = data['applicant']
        source_from = data['source_from']
        apply_date = data['apply_date']
        pub_date = data['pub_date']
        link = data['link']

        new_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (kw, c_no, name, inventor, applicant, source_from, apply_date, pub_date, link))

raw_file.close()
new_file.close()
