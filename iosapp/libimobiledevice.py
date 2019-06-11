import json, re, time, random
from paramiko.client import SSHClient, AutoAddPolicy
import plistlib
import io
from django.conf import settings

MAC_HOST_IP = "9.6.3.6"
MAC_PORT = 22
MAC_USERNAME = "root"
MAC_PASSWORD = "root"
WORK_DIR = '/Users/root/Pictures/TMT/'
DOMAIN = settings.DOMAIN


class Libimobiledevice:
    def __init__(self):
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh_client.connect(MAC_HOST_IP, port=MAC_PORT, username=MAC_USERNAME, password=MAC_PASSWORD, timeout=3)
        self.ssh_dict = {}

    def device_list(self):
        result = self.execute_some_command("idevice_id -l")
        if result.strip():
            return result.strip().split('\n')
        else:
            return []

    def screenshot(self, uuid):
        result = self.execute_some_command(f"cd {WORK_DIR};idevicescreenshot -u {uuid} {uuid}.png")
        result = result.replace('Screenshot saved to ', '').strip()
        return WORK_DIR + result

    def screenshot_device_info_then_upload(self, uuid, to):
        remote_file_path = self.screenshot(uuid)
        try:
            device_info = self.device_info(uuid)
        except:
            device_info = None
        file_info = self.curl_upload_file(to, remote_file_path,
                                          json.dumps(device_info, ensure_ascii=False).replace('"', '\\"'))

        try:
            file_info = json.loads(file_info).get('data')
        except:
            file_info = None
        return {
            "device_info": device_info,
            "file_info": file_info,
        }

    def syslog_start(self, uuid):
        if uuid not in self.device_list():
            return False
        ssh = self.ssh_client.invoke_shell()
        ssh.send(f"cd {WORK_DIR};idevicesyslog -u {uuid}>{uuid}.txt\n")
        self.ssh_dict[uuid] = ssh
        return True

    def syslog_stop(self, uuid):
        self.ssh_dict[uuid].send(chr(3))
        return WORK_DIR + uuid + '.txt'

    def syslog_device_info_then_upload(self, uuid, to):
        remote_file_path = self.syslog_stop(uuid)
        try:
            device_info = self.device_info(uuid)
        except:
            device_info = None
        file_info = self.curl_upload_file(to, remote_file_path,
                                          json.dumps(device_info, ensure_ascii=False).replace('"', '\\"'))

        try:
            file_info = json.loads(file_info).get('data')
        except:
            file_info = None
        return {
            "device_info": device_info,
            "file_info": file_info,
        }

    def device_info(self, uuid):
        result = self.execute_some_command(f"ideviceinfo -u {uuid}")
        result += self.execute_some_command(f"ideviceinfo -u {uuid} -q com.apple.disk_usage.factory")
        result += self.execute_some_command(f"ideviceinfo -u {uuid} -q com.apple.mobile.battery")
        # print(result)
        return {
            "DeviceName": re.findall('DeviceName: (.*?)\n', result, re.I)[0],
            "ProductType": re.findall('ProductType: (.*?)\n', result, re.I)[0],
            "ProductVersion": re.findall('ProductVersion: (.*?)\n', result, re.I)[0],
            "BatteryCurrentCapacity": re.findall('BatteryCurrentCapacity: (.*?)\n', result, re.I)[0],
            "BatteryIsCharging": re.findall('BatteryIsCharging: (.*?)\n', result, re.I)[0],
            "TotalDataCapacity": re.findall('TotalDataCapacity: (.*?)\n', result, re.I)[0],
            "TotalDataAvailable": re.findall('TotalDataAvailable: (.*?)\n', result, re.I)[0],
        }

    def execute_some_command(self, command):
        stdin, stdout, stderr = self.ssh_client.exec_command(f"bash -lc '{command}'", timeout=10)
        return stdout.read().decode()

    def ssh_logout(self):
        self.ssh_client.close()

    def curl_upload_file(self, username, filepath, device_info):
        result = self.execute_some_command(
            f'curl {DOMAIN}/api/tmt/files/ -F "file=@{filepath}" -F "username={username}" -F "device_info={device_info}"')
        if result:
            return result
        else:
            return "{}"

    def upload_file(self, local_file_path, remote_file_path):
        """
        上传文件
        """
        # 创建sftp对象上传文件
        sftp = self.ssh_client.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        sftp.close()

    def download_file(self, remote_file_path, local_file_path):
        """
        下载文件
        """
        # 创建sftp对象下载文件
        sftp = self.ssh_client.open_sftp()
        sftp.get(remote_file_path, local_file_path)
        sftp.close()


if __name__ == '__main__':
    libi = Libimobiledevice()
    print(libi.device_list())
    print(libi.screenshot_device_info_then_upload('c633c1c3a4335ec335da0e8892dbd975241fdd50'))

    # print(libi.syslog_start('c633c1c3a4335ec335da0e8892dbd975241fdd50'))
    # time.sleep(5)
    # print(libi.syslog_stop('c633c1c3a4335ec335da0e8892dbd975241fdd50'))
    # print(libi.device_info('c633c1c3a4335ec335da0e8892dbd975241fdd50'))
