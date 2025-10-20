# How to run the application?

## 1. Import the dimensional model
- Run the dimensional model script
- Run the ETL Pipline by executing the load script

## 2. Install notebook dependencies
- Run `pip install -r requirements.txt` to install the dependencies
    - (Optional) Create a virtual environment using `venv` and register the kernel to jupyter using `ipykernel`

## 3. Set up the .env file
-  Create a entry for your mysql instance password `MYSQL_DB_PASSWORD=<your_password>`

## 4. Run the notebook sequentially
- Since some cells rely on declarations in previous cells, please run them sequentially.
