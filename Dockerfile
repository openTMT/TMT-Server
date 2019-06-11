FROM opentmt/tmt-server-base

COPY . .

ENV PYTHONUNBUFFERED 0

# 修改本机时间和时区
# 安装必要的必备库
# 修改settings.online.py为settings.py
RUN mv TMTServer/settings.online.py TMTServer/settings.py && \
    pip install -r requestments.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com && \
    cp -f nginx.conf /etc/nginx/nginx.conf

RUN dos2unix entrypoint.sh && chmod +x entrypoint.sh

# 挂载附件
VOLUME /files

EXPOSE 7892

ENTRYPOINT ["./entrypoint.sh"]
