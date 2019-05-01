from RAKE.rake import Rake
rake = Rake()
dst_file_path = 'D:\TREC_v2.txt'
with open(dst_file_path,'r') as f:
    next(f)
    text =  next(f)
print(text)
print(rake.run(text))
