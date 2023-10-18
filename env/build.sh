runuser -u red -c 'poetry export --output requirements.txt --without-hashes'
docker build -f env/Dockerfile -t armann/telegate:latest .
docker stop telegate
docker rm telegate
mkdir -p /opt/containers/telegate/data
cp -f env/docker-compose.yml  /opt/containers/telegate/
cp -f /home/red/telegate/telegate.env  /opt/containers/telegate/data/
chown -R cont:cont /opt/containers/telegate
chmod -R g+rw /opt/containers/telegate
docker compose -f /opt/containers/telegate/docker-compose.yml up -d --force-recreate
