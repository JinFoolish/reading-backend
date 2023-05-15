FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制本地代码到容器中
COPY . .

# 安装依赖
RUN pip install -r requirements.txt

# 复制gunicorn配置文件
COPY gunicornconf.py .

# 安装gunicorn
RUN pip install gunicorn

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--config", "gunicornconf.py", "main:app"]