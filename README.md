# 소프트웨어에 물들다: 도서관 신청 시스템

## 배포 가이드

배포를 시도하는 모든 분들은 적합한 PEM 파일을 보유하고 계셔야 하며, 각 컴퓨터의 bash에서 아래 코드가 한 번 실행되었어야 합니다.

```
cat ~/.ssh/id_rsa.pub | sudo ssh -i <PEM_FILE_NAME>.pem ubuntu@<SERVER_HOST> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys"
```


## Database migration 가이드

migrations 스크립트를 수행하려면 터미널에서 아래 명령어 실행
```
export FLASK_APP=wsgi.py
flask db upgrade
```
