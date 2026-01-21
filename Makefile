cleaup:
	@echo "pulisco tutti i file di cache e vecchi pdf generati"
	rm -f tex/*.aux tex/*.log tex/*.xdv tex/*.out tex/*.pdf

compile:
	@echo "Compilo le carte delle magie..."
	latexmk -f -xelatex -cd tex/cards.tex tex/printable.tex
