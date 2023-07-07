# dashboard2report
Repo for automated creation of reports based on such sources as Grafana

## Preparation

```shell script
sudo pip install -r "requirements.txt"

cp "secret.template.json" "secret.json"
cp "config.template.json" "config.json"

cp "main.py" "production-your-project.py"

chmod +x "production-your-project.py"
```
