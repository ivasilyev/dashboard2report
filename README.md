# `dashboard2report`

Repo containing basic code modules for automated creation of integrated reports.

Supported import sources:
* Grafana
* InfluxDB
* PostgreSQL

Supported export formats:
* Microsoft Word

## Preparation

```shell script
pip install -r "requirements.txt"

cp "secret.template.json" "secret.json"
cp "config.template.json" "config.json"

cp "main.py" "production-your-project.py"

chmod +x "production-your-project.py"
```

## Start

```shell script
export GF_PANEL_WIDTH=1920
export GF_PANEL_HEIGHT=1080
export TIMEZONE=Europe/Moscow

python "production-your-project.py" -d $GF_DASHBOARD -s $START_TS -e $END_TS -o test
```
