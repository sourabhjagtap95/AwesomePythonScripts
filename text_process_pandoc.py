import pandoc

in_file = open("example.md", "r").read()
pandoc.write(in_file, file="example.pdf", format="pdf")
