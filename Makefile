install:
	pip install -r requirements.txt

test:
	python -m pytest -v

run:
	streamlit run app.py

docker-build:
	docker build -t supertrader .

docker-run:
	docker-compose up

diagram:
	docker run --rm -v $(PWD)/docs:/data minlag/mermaid-cli -i architecture.mmd -o architecture.png
