from app.config import Config
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail
from app.database.models import VerifyEmail
import uuid


class EmailManager:
    sg = sendgrid.SendGridAPIClient(apikey=Config.sendgrid_api_key)

    @classmethod
    def send_verify_email(cls, to_email, uuid):
        """
        인증 메일을 전송합니다.
        """
        from_email = "somul.may@gmail.com"
        subject, content = cls.get_uuid_content(uuid, Config.server_host)
        return cls._send_mail(from_email, to_email, subject, content)

    @classmethod
    def _send_mail(cls, from_email, to_email, subject, content):
        """
        E-mail을 전송합니다.
            from_email: 전송자
            to_email: 수신자
            subject: 제목
            content: 내용
        """
        from_email = Email(from_email)
        to_email = Email(to_email)
        mail = Mail(from_email, subject, to_email, content)
        response = cls.sg.client.mail.send.post(request_body=mail.get())

        return response.status_code % 100 == 2

    @classmethod
    def get_unique_uuid(cls):
        """
        중복 검사가 완료된 UUID를 반환합니다.
        """
        while True:
            gen_uuid = str(uuid.uuid4())
            duplicated_email\
                = VerifyEmail.query.filter_by(key=gen_uuid).first()
            if duplicated_email is None:
                break

        return gen_uuid

    @classmethod
    def get_uuid_content(cls, uuid, host):
        """
        UUID를 만들고 이에 해당하는 E-mail 제목 및 본문을 만듭니다.
        """
        subject = "5월, 소프트웨어에 물들다 - 가입 인증 메일입니다."
        content = Content("text/plain", """
        소프트웨어에 물들다(이하 소물)에 참여해주신 여러분들 환영합니다.

        본 메일은 소물 참여신청을 확인하기 위한 인증 메일입니다.
        아래 링크를 클릭 하시면 인증이 마무리됩니다.
        소물에 참여주신 모든 분들께 다시 한번 감사의 말씀을 드립니다.

        http://{host}/verify?key={uuid}
        """.format(uuid=uuid, host=host))
        return subject, content
