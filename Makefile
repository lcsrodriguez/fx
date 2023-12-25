all:
	@echo "Installing the requirements"
	@python3 -m pip3 install -r requirements.txt

init:
	@echo "Creating output folders..."
	@mkdir -p "out"
	@mkdir -p "out/csv"
	@mkdir -p "out/parquet"

install:
	@echo "Installing the requirements"
	@python3 -m pip3 install -r requirements.txt

clean:
	@echo "Cleaning output folders..."
	@rm -rf out/csv/*.csv
	@rm -rf out/parquet/*.parquet
