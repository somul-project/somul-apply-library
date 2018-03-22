# 소프트웨어에 물들다: 도서관 신청 시스템

## 배포 가이드

배포를 시도하는 모든 분들은 적합한 PEM 파일을 보유하고 계셔야 하며, 각 컴퓨터의 bash에서 아래 코드가 한 번 실행되었어야 합니다.

```
cat ~/.ssh/id_rsa.pub | sudo ssh -i <PEM_FILE_NAME>.pem ubuntu@18.219.223.174 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## Code Climate
PR날릴때마다 Checks 항목에 codeclimate가 Lint 결과를 보여줍니다. <br/>
CodeClimate 클라우드 환경에서 수행합니다. <br/>
https://codeclimate.com/ <br/>
<br/>
로컬 설치가이드 <br/>
https://github.com/codeclimate/codeclimate#packages <br/>

Mac OS via homebrew(https://brew.sh/)
```
brew tap codeclimate/formulae
brew install codeclimate
```

로컬 실행
```
codeclimate analyze
```


결과 예시
``` 
== app/database/__init__.py (2 issues) ==
7: Line too long (81 > 79 characters) [pep8]
11: Expected 2 blank lines, found 1 [pep8]

== app/database/models.py (1 issue) ==
5: Expected 2 blank lines, found 1 [pep8]

== wsgi.py (1 issue) ==
4: No newline at end of file [pep8]
```