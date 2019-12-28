# R53-DDNS
AWS Route53 DDNS

## Installation

- Install modules

```bash
git clone https://github.com/RyohAkiyoshi/r53-ddns.git
npm install -g serverless
```

- Edit env file

```bash
cp env/dev.yml.sample env/dev.yml
vi env/dev.yml
cp env/prod.yml.sample env/prod.yml
vi env/prod.yml
```

- Deploy Lambda and API Gateway

```bash
sls deploy -v --stage dev
```

- Cron

```bash
crontab -e
```

```
0 * * * * R53_DDNS_API_KEY=<API_KEY> /path/to/repo/r53-ddns/update.sh
```
