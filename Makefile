install:
	pip install -r requirements.txt

run:
	docker-compose up --build

dashboard:
	streamlit run streamlit_app/dashboard.py

test:
	pytest tests/
# tools
lint:
	flake8 src
	