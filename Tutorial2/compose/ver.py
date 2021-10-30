from pkg_resources import get_distribution as v
    


modulos = "pydantic,uvicorn,fastapi,sqlalchemy,mysql-connector-python"

for i in modulos.split(","):
    print("{}=={}".format(i,v(i).version))