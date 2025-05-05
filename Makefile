.PHONY: api streamlit dev install

# Run Flask API
api:
	. .venv/bin/activate && python src/main.py

# Run Streamlit dashboard
streamlit:
	. .venv/bin/activate && streamlit run streamlit_app/dashboard.py

# Instructions for dev mode
dev:
	@echo "Open 2 terminals:"
	@echo "  make api       # to start the backend"
	@echo "  make streamlit # to start the frontend"

install:
	pip install -r requirements.txt

run:
	docker-compose up --build

test:
	pytest tests/

synth_data:
	python src/synthetic_data.py

# tools
lint:
	flake8 src tests streamlit_app

clear_docker:
	docker image prune

deep_clear_docker:
	docker system prune -a --volumes
