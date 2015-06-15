import subprocess

with open("_build/latex/pi3d_book.tex", "r") as f:
  tx = f.read().splitlines()

txnew = []
flg1 = True
for l in tx:
  if l == "" and flg1:
    txnew += ["\\usepackage{wrapfig}",""]
    flg1 = False # just do this once before first blank line
  elif "includegraphics{" in l and "hfill" in l:
    fname = l.split("{")[2].split("}")[0]
    if l.startswith("{\\hfill"): # i.e. right justify
      fl_type = "R"
    else:
      fl_type = "L"
    txnew += ["\\begin{wrapfigure}{" + fl_type + "}{0.35\\textwidth}",
              "\\includegraphics[width = 0.3\\textwidth]{" + fname + "}",
              "\\end{wrapfigure}"]
  else:
    txnew += [l]
    
txnew = "\n".join(txnew)
with open("_build/latex/pi3d_book.tex", "w") as fo:
  fo.write(txnew)

subprocess.Popen(["pdflatex", "pi3d_book"], cwd="/home/jill/pi3d_book/_build/latex")
