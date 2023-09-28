import subprocess
import logging

logger = logging.getLogger(__name__)


FIRST_PART = "Passwords or encryption keys are required to access the wireless network '"
SECOND_PART = "'."

def main():
    agent = subprocess.Popen(["nmcli", "agent", "secret"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    password = None
    while True:
        line = agent.stdout.readline()
        if not line:
            break
        decoded_line = line.decode("utf-8").strip()
        if decoded_line.startswith(FIRST_PART) and decoded_line.endswith(SECOND_PART):
            network_name = decoded_line[len(FIRST_PART):-len(SECOND_PART)]
            logger.info("Password request for: %s", network_name)
            password = "75-add1t1on-SALT-express-82!\n"
            agent.stdin.write(password.encode("utf-8"))
            agent.stdin.flush()
        else:
            if password:
                decoded_line = decoded_line.replace(password.strip(), "********")
            logger.info(decoded_line)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
