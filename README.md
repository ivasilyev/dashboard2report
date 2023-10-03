# `dashboard2report`

Repo containing basic code modules for automated creation of integrated reports.

Supported import sources:
* Grafana
* InfluxDB
* PostgreSQL

Supported export formats:
* Microsoft Word

## Setup

```shell script
pip install -r "requirements.txt"

cp "secret.template.json" "secret.json"
cp "config.template.json" "config.json"

cp "main.py" "production-your-project.py"

chmod +x "production-your-project.py"
```

## Configuration

### Review the Grafana dashboard URL

```text
https://grafana.example.org:3000/d/abc123456/dashboard_name?orgId=1&host=All&from=1672520400000&to=1672524000000
```

### (Optional) Access Grafana API JSON to get detailed datasource queries

```text
https://grafana.example.org:3000/api/dashboards/uid/abc123456
```

### Fill the mandatory `secret.json` & `config.json` files

## Debug run

```shell script
export GF_PANEL_WIDTH=1920
export GF_PANEL_HEIGHT=1080
export TIMEZONE="Europe/Moscow"
export LOGGING_LEVEL=0

python "production-your-project.py" \
    --dashboard "abc123456" \
    --start 1672520400000 \
    --end 1672524000000 \
    --parent "https://confluence.example.org/pages/viewpage.action?pageId=1234567890" \
    --target_name "Test result page" \
    --output "test" \
> out.log \
2>&1
```
