from app.config import Config
import uuid
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail


class EmailManager:
    sg = sendgrid.SendGridAPIClient(apikey=Config.sendgrid_api_key)

    @classmethod
    def send_mail(cls, from_email, to_email, subject, content):
        """
        E-mail을 전송합니다.
            from_email: 전송자
            to_email: 수신자
            subject: 제목
            content: 내용
        """
        from_email = Email(from_email)
        to_email = Email(to_email)
        content = Content("text/plain", content)
        mail = Mail(from_email, subject, to_email, content)
        response = cls.sg.client.mail.send.post(request_body=mail.get())

        return response.status_code % 100 == 2

    @classmethod
    def get_uuid_content(cls):
        """
        UUID를 만들고 이에 해당하는 E-mail 제목 및 본문을 만듭니다.
        """
        generated_uuid = str(uuid.uuid4())

        # TODO(@harrydrippin): UUID에 대한 중복 검사 및 재생성 로직
        subject = "[5월, 소프트웨어에 물들다] 가입 인증 메일입니다."
        content = """
        안녕하세요, 5월 소프트웨어에 물들다 운영진입니다.

        다음 링크를 클릭하시면 E-mail을 인증할 수 있습니다. 감사합니다.
        http://somul.kr/verify?key=%s
        """.format(generated_uuid)
        return subject, content, generated_uuid