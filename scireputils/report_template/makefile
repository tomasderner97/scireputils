build:
	pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=output -aux-directory=auxiliary -include-directory=classfiles -include-directory=latex latex/main.tex

open:
	cmd /c start output/main.pdf

all: build open